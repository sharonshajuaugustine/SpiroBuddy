"""File storage for the document vault: check the upload, then keep it somewhere private.

validate_upload() is the gate (spec §8.10):
  * jpg, png, webp or pdf only, at most 10 MB;
  * the type comes from the file's first bytes (magic bytes) – never from its name;
  * SVG, HTML, XML and scripts are refused even when renamed to .png or .pdf;
  * every image is decoded and re-encoded from its pixels, which drops EXIF (GPS, phone
    model...) and anything hidden after the picture; photos are turned the right way up first;
  * images also get a 320 px PNG thumbnail.

save / load / delete keep the bytes under a random key such as docs/202610/<32 hex>.png:
  * on Supabase (only when the active store is Supabase): the private bucket "documents",
    through the Storage REST API with the service key – the browser never sees a storage key;
  * otherwise: backend/data/uploads/ (git-ignored).
The server streams a file only after its own permission check (routes_documents.py).
"""
from __future__ import annotations

import io
import logging
import re
import secrets

from . import service
from .config import UPLOAD_DIR, env, now_local, supabase_bucket

log = logging.getLogger("spirobuddy.storage")

MAX_BYTES = 10 * 1024 * 1024
EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "application/pdf": "pdf"}
MAX_PIXELS = 64_000_000        # refuse absurd pictures (a "decompression bomb")
MAX_SIDE = 3000                # longer photos are scaled down; plenty for reading a prescription
THUMB_SIDE = 320

_KEY_RE = re.compile(r"^[a-z0-9_-]{1,32}/\d{6}/[0-9a-f]{32}\.(jpg|png|webp|pdf)$")
_PREFIX_RE = re.compile(r"^[a-z0-9_-]{1,32}$")
_MARKUP = (b"<svg", b"<html", b"<!doctype", b"<?xml", b"<script", b"<body", b"<head", b"<iframe",
           b"<?php", b"<%", b"javascript:")
_PDF_MARKUP = (b"<html", b"<!doctype", b"<script", b"<svg", b"<iframe", b"<body")   # a web page dressed as a PDF
_PDF_ACTIVE = (b"/JavaScript", b"/Launch")      # a PDF that runs code or starts a program
_BAD_DECLARED = ("svg", "html", "xml", "javascript", "ecmascript", "x-sh", "x-msdownload", "x-php")


class StorageError(RuntimeError):
    """The file could not be saved, read or removed (for example Supabase Storage is down)."""


# ----------------------------------------------------------------------------- validation

def _sniff(data: bytes) -> str | None:
    """The real type from the first bytes, or None if it is not one of our four."""
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    if data[:5] == b"%PDF-":
        return "application/pdf"
    return None


def _looks_like_markup(head: bytes) -> bool:
    h = head.lstrip(b"\xef\xbb\xbf\xff\xfe \t\r\n\x00").lower()
    return h.startswith((b"<", b"#!")) or any(m in h for m in _MARKUP)


def _clean_image(data: bytes, mime: str) -> tuple[bytes, bytes]:
    """Decode, turn upright, rebuild from the pixels only, re-encode. -> (image, png thumbnail)"""
    from PIL import Image, ImageOps

    fmt = {"image/jpeg": "JPEG", "image/png": "PNG", "image/webp": "WEBP"}[mime]
    try:
        with Image.open(io.BytesIO(data), formats=[fmt]) as probe:
            w, h = probe.size
            if w < 1 or h < 1 or w * h > MAX_PIXELS:
                raise ValueError("This picture is too large. Please take the photo again at a normal size.")
            probe.verify()                              # catches a cut-off or damaged file
        img = Image.open(io.BytesIO(data), formats=[fmt])
        if fmt == "JPEG":
            img.draft("RGB", (MAX_SIDE, MAX_SIDE))      # decode big photos at a smaller size
        img.load()                                      # an animation keeps its first frame only
        img = ImageOps.exif_transpose(img)              # apply the camera's rotation, then forget it
        alpha = fmt != "JPEG" and (img.mode in ("RGBA", "LA") or "transparency" in img.info)
        img = img.convert("RGBA" if alpha else "RGB")
        if max(img.size) > MAX_SIDE:
            img.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        clean = Image.frombytes(img.mode, img.size, img.tobytes())    # pixels only: no EXIF, no text chunks
    except ValueError:
        raise
    except Exception:
        raise ValueError("This picture can't be opened. Please take the photo again.")
    out = io.BytesIO()
    if fmt == "JPEG":
        clean.save(out, "JPEG", quality=88, optimize=True)
    elif fmt == "PNG":
        clean.save(out, "PNG", compress_level=6)
    else:
        clean.save(out, "WEBP", quality=88)
    thumb = clean.copy()
    thumb.thumbnail((THUMB_SIDE, THUMB_SIDE), Image.LANCZOS)
    tout = io.BytesIO()
    thumb.save(tout, "PNG", optimize=True)
    return out.getvalue(), tout.getvalue()


def validate_upload(data: bytes, filename: str, declared_mime: str | None) -> tuple[str, bytes, bytes | None]:
    """-> (mime, cleaned_bytes, thumbnail_png_or_None). Raises ValueError(plain reason) on a bad file.

    The file name and the declared type are never trusted: the type comes from the magic bytes.
    Images come back re-encoded (no EXIF); a PDF comes back unchanged with no thumbnail.
    The PDF check is a best effort (a PDF can't be re-encoded here): right header, an end
    marker, no web-page markup at the start and no JavaScript or Launch action."""
    if not isinstance(data, (bytes, bytearray)) or not data:
        raise ValueError("The file is empty.")
    data = bytes(data)
    if len(data) > MAX_BYTES:
        raise ValueError("The file is larger than 10 MB. Please send a smaller photo or PDF.")
    declared = (declared_mime or "").lower()
    if any(b in declared for b in _BAD_DECLARED):
        raise ValueError("Only photos (JPG, PNG, WebP) and PDF files are accepted.")
    head = data[:1024]
    mime = _sniff(data)
    if mime is None:
        if _looks_like_markup(head):
            raise ValueError("This is a web page, SVG or script, not a photo or PDF.")
        raise ValueError("Only photos (JPG, PNG, WebP) and PDF files are accepted.")
    if mime == "application/pdf":
        if any(m in head.lower() for m in _PDF_MARKUP):
            raise ValueError("This PDF has web-page code inside and can't be accepted.")
        if b"%%EOF" not in data[-2048:]:
            raise ValueError("This PDF looks cut off or damaged. Please send it again.")
        if any(m in data for m in _PDF_ACTIVE):
            raise ValueError("This PDF contains a script and can't be accepted.")
        return mime, data, None
    cleaned, thumb = _clean_image(data, mime)
    if len(cleaned) > MAX_BYTES:
        raise ValueError("The file is larger than 10 MB. Please send a smaller photo or PDF.")
    return mime, cleaned, thumb


# ----------------------------------------------------------------------------- where files live

def _supabase() -> tuple[str, str] | None:
    """(url, service key) when the active store is Supabase, else None (= local folder)."""
    try:
        if service.store().name != "supabase":
            return None
    except Exception:
        return None
    url, key = env("SUPABASE_URL").rstrip("/"), env("SUPABASE_SERVICE_ROLE_KEY")
    return (url, key) if url and key else None


def backend_name() -> str:
    return "supabase" if _supabase() else "local"


def _request(method: str, path: str, **kw):
    """The ONE place that talks to Supabase Storage (tests replace it). path starts with "/"."""
    import httpx
    url, key = _supabase() or ("", "")
    headers = {"Authorization": f"Bearer {key}", "apikey": key, **(kw.pop("headers", None) or {})}
    return httpx.request(method, f"{url}/storage/v1{path}", headers=headers, timeout=30.0, **kw)


def _check_key(path: str) -> str:
    if not isinstance(path, str) or not _KEY_RE.match(path):
        raise ValueError("not a storage key")           # also stops ../ tricks
    return path


def new_key(mime: str, *, prefix: str, like: str | None = None) -> str:
    """A random key: <prefix>/<yyyymm>/<32 hex>.<ext>. With like=<another key> the month and the
    random part are copied, so a thumbnail sits beside its document (thumbs/<same>.png)."""
    if mime not in EXT:
        raise ValueError("unsupported file type")
    if not _PREFIX_RE.match(prefix or ""):
        raise ValueError("bad storage prefix")
    if like:
        _, month, name = _check_key(like).split("/")
        return f"{prefix}/{month}/{name.rsplit('.', 1)[0]}.{EXT[mime]}"
    return f"{prefix}/{now_local():%Y%m}/{secrets.token_hex(16)}.{EXT[mime]}"


def save(data: bytes, mime: str, *, prefix: str, like: str | None = None) -> str:
    """Store the bytes and return their key. Pass bytes that validate_upload() has cleaned."""
    key = new_key(mime, prefix=prefix, like=like)
    if _supabase():
        try:
            r = _request("POST", f"/object/{supabase_bucket()}/{key}", content=bytes(data),
                         headers={"Content-Type": mime, "x-upsert": "false"})
        except Exception as e:
            raise StorageError(f"could not reach file storage: {type(e).__name__}")
        if r.status_code >= 300:
            raise StorageError(f"file storage refused the upload (HTTP {r.status_code})")
        return key
    target = UPLOAD_DIR / key
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(bytes(data))
    return key


def load(path: str) -> bytes:
    """The stored bytes. FileNotFoundError if the key doesn't exist."""
    key = _check_key(path)
    if _supabase():
        try:
            r = _request("GET", f"/object/authenticated/{supabase_bucket()}/{key}")
        except Exception as e:
            raise StorageError(f"could not reach file storage: {type(e).__name__}")
        if r.status_code in (400, 404):
            raise FileNotFoundError(key)
        if r.status_code >= 300:
            raise StorageError(f"file storage refused the download (HTTP {r.status_code})")
        return r.content
    target = UPLOAD_DIR / key
    if not target.is_file():
        raise FileNotFoundError(key)
    return target.read_bytes()


def delete(path: str) -> None:
    """Remove the stored bytes. A key that is already gone is not an error."""
    key = _check_key(path)
    if _supabase():
        try:
            r = _request("DELETE", f"/object/{supabase_bucket()}/{key}")
        except Exception as e:
            raise StorageError(f"could not reach file storage: {type(e).__name__}")
        if r.status_code >= 300 and r.status_code not in (400, 404):
            raise StorageError(f"file storage refused the delete (HTTP {r.status_code})")
        return
    try:
        (UPLOAD_DIR / key).unlink()
    except FileNotFoundError:
        pass


def ensure_bucket() -> None:
    """Called at start-up; never raises. Local: make the uploads folder. Supabase: create the
    private bucket (so the founder has nothing to set up); "already exists" is fine."""
    try:
        if not _supabase():
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            return
        bucket = supabase_bucket()
        r = _request("POST", "/bucket", json={"id": bucket, "name": bucket, "public": False,
                                              "file_size_limit": MAX_BYTES})
        if r.status_code < 300:
            log.info("created the private storage bucket %r", bucket)
        elif r.status_code in (400, 409) and "exist" in (r.text or "").lower():
            pass                                            # already there
        else:
            log.warning("could not create the storage bucket %r (HTTP %s)", bucket, r.status_code)
    except Exception as e:
        log.warning("storage bucket check failed: %s", type(e).__name__)
