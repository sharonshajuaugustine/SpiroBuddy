"""Prescription review totals include both image and clinician-text AI drafts."""
from backend.app import ai_register


def test_notepad_and_image_drafts_share_review_denominators(monkeypatch):
    rows = [
        dict(purpose="rx_notepad", ok=True, decision="edited", lines_total=4,
             lines_edited=2, lines_removed=1),
        dict(purpose="rx_extract", ok=True, decision="rejected", lines_total=2,
             lines_edited=0, lines_removed=2),
        dict(purpose="rx_notepad", ok=True, decision=None),
        # A failed call does not become a successful draft even with stray review data.
        dict(purpose="rx_notepad", ok=False, decision="approved", lines_total=100),
        # Document metadata suggestions never enter prescription review percentages.
        dict(purpose="doc_suggest", ok=True, decision="edited", lines_total=100,
             lines_edited=100),
    ]
    requests = []

    def events(hospital_id, limit):
        requests.append((hospital_id, limit))
        return rows

    monkeypatch.setattr(ai_register, "events_for", events)
    result = ai_register.stats(17)
    assert requests == [(17, 0)]
    assert result["drafts"] == 3
    assert result["reviewed"] == 2
    assert result["lines_total"] == 6
    assert result["lines_edited"] == 2
    assert result["lines_removed"] == 3
    assert result["lines_edited_pct"] == 33.3
    assert result["lines_removed_pct"] == 50.0
    assert result["rejected_pct"] == 50.0
    assert result["calls"] == 5
    assert result["failed"] == 1
    assert result["by_purpose"] == {
        "rx_notepad": {"calls": 3, "ok": 2, "failed": 1},
        "rx_extract": {"calls": 1, "ok": 1, "failed": 0},
        "doc_suggest": {"calls": 1, "ok": 1, "failed": 0},
    }


def test_unreviewed_notepad_has_zero_review_percentages(monkeypatch):
    monkeypatch.setattr(ai_register, "events_for", lambda *args, **kwargs: [
        dict(purpose="rx_notepad", ok=True),
        dict(purpose="rx_notepad", ok=False),
    ])
    result = ai_register.stats()
    assert result["drafts"] == 1
    assert result["reviewed"] == 0
    assert result["lines_total"] == 0
    assert result["lines_edited_pct"] == 0.0
    assert result["lines_removed_pct"] == 0.0
    assert result["rejected_pct"] == 0.0
