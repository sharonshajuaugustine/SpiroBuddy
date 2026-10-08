/*
  SpiroBuddy – serial firmware (CONTRACT A in docs/ARCHITECTURE.md)
  ------------------------------------------------------------------
  Reads a VL53L1X or VL53L0X laser distance sensor about 30 times a second
  and prints one line per reading over USB serial at 115200 baud:

      D,<millis>,<distance_mm>      a reading
      S,READY,VL53L1X               status: sensor is running (sent at start-up)
      E,<text>                      an error (sensor not found, timeout, ...)

  The browser may send "B\n" to make the device beep (ignored if no buzzer).
  Extra (harmless, not used by the app yet): "I\n" re-sends the S,READY line.

  Works on:  Seeed XIAO ESP32-C3, generic ESP32 DevKit, Arduino Uno / Nano.
  Libraries: "VL53L1X" by Pololu  OR  "VL53L0X" by Pololu (Library Manager).
             Only the one you select below has to be installed.

  Wiring, setup and troubleshooting: docs/HARDWARE.md
*/

// ===================== 1. CHOOSE YOUR SENSOR (one line) =====================
#define SENSOR_VL53L1X
// #define SENSOR_VL53L0X

// ===================== 2. OPTIONAL SETTINGS ================================
// VL53L1X only: narrow the field of view so the sensor sees the disc, not the
// chamber walls. 16 = full view (~27 deg), 8 = ~20 deg, 4 = narrowest (~15 deg).
// Smaller = narrower but weaker signal. Allowed 4..16.
#define VL53L1X_ROI_SIZE   8
#define VL53L1X_ROI_CENTER 199   // 199 = centre of the sensor (Pololu default)

// Readings above this are treated as "nothing in front of the sensor".
#define MAX_VALID_MM 2000

// Arduino Uno/Nano: turn OFF the chip's own 5 V pull-ups on SDA/SCL so a
// 3.3 V-only sensor module is not pulled up to 5 V. The module's own pull-ups
// are then used (almost every breakout board has them). Set to 0 to disable.
#define AVR_DISABLE_INTERNAL_PULLUPS 1

// ===================== 3. BOARD PINS (auto-selected) =======================
// -1 means "not connected" – the feature is simply switched off.
#if defined(ARDUINO_XIAO_ESP32C3)
  #define BOARD_NAME     "XIAO_ESP32C3"
  // Plain GPIO numbers so the #if checks below work (D4 = GPIO6, etc.).
  #define I2C_SDA_PIN    6       // pin D4
  #define I2C_SCL_PIN    7       // pin D5
  #define XSHUT_PIN      10      // pin D10: sensor on/off (optional wire)
  #define BUZZER_PIN     4       // pin D2: passive piezo +
  #define STATUS_LED_PIN -1      // XIAO C3 has no user LED
#elif defined(ARDUINO_ARCH_ESP32)
  #define BOARD_NAME     "ESP32"
  #define I2C_SDA_PIN    21
  #define I2C_SCL_PIN    22
  #define XSHUT_PIN      -1
  #define BUZZER_PIN     25
  #define STATUS_LED_PIN 2       // blue LED on most DevKit boards
#elif defined(ARDUINO_ARCH_AVR)
  #define BOARD_NAME     "AVR"   // Uno / Nano: SDA = A4, SCL = A5 (fixed)
  #define XSHUT_PIN      -1
  #define BUZZER_PIN     8
  #define STATUS_LED_PIN 13
#else
  #define BOARD_NAME     "OTHER" // uses the board's default I2C pins
  #define XSHUT_PIN      -1
  #define BUZZER_PIN     -1
  #define STATUS_LED_PIN -1
#endif

// ===================== CODE (no need to edit below) ========================
#include <Wire.h>

#if defined(SENSOR_VL53L1X) && defined(SENSOR_VL53L0X)
  #error "Choose only ONE sensor: SENSOR_VL53L1X or SENSOR_VL53L0X"
#elif defined(SENSOR_VL53L1X)
  #include <VL53L1X.h>
  VL53L1X sensor;
  #define SENSOR_NAME "VL53L1X"
#elif defined(SENSOR_VL53L0X)
  #include <VL53L0X.h>
  VL53L0X sensor;
  #define SENSOR_NAME "VL53L0X"
#else
  #error "Choose a sensor: #define SENSOR_VL53L1X or SENSOR_VL53L0X"
#endif

const unsigned long BAUD             = 115200;
const uint16_t      PERIOD_MS        = 33;    // ~30 readings per second
const uint16_t      I2C_TIMEOUT_MS   = 500;
const unsigned long RETRY_MS         = 2000;  // retry sensor start-up every 2 s
const uint8_t       MAX_TIMEOUTS     = 5;     // then restart the sensor
const unsigned long NO_TARGET_MSG_MS = 2000;  // rate-limit "no target" errors

bool          sensorOk        = false;
unsigned long lastInitTry     = 0;
unsigned long lastDataMs      = 0;
unsigned long lastNoTargetMsg = 0;
uint8_t       timeoutsInRow   = 0;

char    cmdBuf[8];
uint8_t cmdLen = 0;

// ---------- small helpers ----------
void setLed(bool on) {
#if STATUS_LED_PIN >= 0
  digitalWrite(STATUS_LED_PIN, on ? HIGH : LOW);
#endif
}

void beep(unsigned int freq, unsigned long ms) {
#if BUZZER_PIN >= 0
  tone(BUZZER_PIN, freq, ms);
#endif
}

void printReady() {
  Serial.println(F("S,READY," SENSOR_NAME));
}

// ---------- sensor start-up ----------
bool initSensor() {
#if XSHUT_PIN >= 0
  // Power-cycle the sensor through XSHUT so it starts from a clean state.
  pinMode(XSHUT_PIN, OUTPUT);
  digitalWrite(XSHUT_PIN, LOW);
  delay(10);
  digitalWrite(XSHUT_PIN, HIGH);
  delay(10);
#endif

  sensor.setTimeout(I2C_TIMEOUT_MS);
  if (!sensor.init()) return false;

#if defined(SENSOR_VL53L1X)
  sensor.setDistanceMode(VL53L1X::Short);         // best below 1.3 m, bright rooms
  sensor.setMeasurementTimingBudget(33000);       // 33 ms per reading
  sensor.setROISize(VL53L1X_ROI_SIZE, VL53L1X_ROI_SIZE);
  sensor.setROICenter(VL53L1X_ROI_CENTER);
  sensor.startContinuous(PERIOD_MS);
#else
  sensor.setMeasurementTimingBudget(33000);       // 33 ms per reading
  sensor.startContinuous();                        // back-to-back readings
#endif
  return true;
}

void tryInit() {
  lastInitTry = millis();
  if (initSensor()) {
    sensorOk      = true;
    timeoutsInRow = 0;
    lastDataMs    = millis();
    setLed(true);
    printReady();
  } else {
    sensorOk = false;
    Serial.println(F("E,SENSOR_NOT_FOUND"));
  }
}

// ---------- handle one reading ----------
void handleTimeout() {
  Serial.println(F("E,TIMEOUT"));
  if (++timeoutsInRow >= MAX_TIMEOUTS) {
    Serial.println(F("E,SENSOR_LOST_RESTARTING"));
    sensorOk = false;
    setLed(false);
    lastInitTry = 0;   // retry straight away
  }
}

void sendReading(uint16_t mm, bool valid) {
  if (valid && mm > 0 && mm <= MAX_VALID_MM) {
    Serial.print(F("D,"));
    Serial.print(millis());
    Serial.print(',');
    Serial.println(mm);
  } else if (millis() - lastNoTargetMsg > NO_TARGET_MSG_MS) {
    lastNoTargetMsg = millis();
    Serial.println(F("E,NO_TARGET"));
  }
}

void pollSensor() {
#if defined(SENSOR_VL53L1X)
  // Non-blocking: only read when a new result is ready.
  if (sensor.dataReady()) {
    uint16_t mm = sensor.read(false);
    lastDataMs = millis();
    timeoutsInRow = 0;
    uint8_t st = sensor.ranging_data.range_status;
    bool valid = (st == VL53L1X::RangeValid) ||
                 (st == VL53L1X::RangeValidMinRangeClipped);
    sendReading(mm, valid);
  } else if (millis() - lastDataMs > I2C_TIMEOUT_MS) {
    lastDataMs = millis();
    handleTimeout();
  }
#else
  uint16_t mm = sensor.readRangeContinuousMillimeters();  // waits ~33 ms
  if (sensor.timeoutOccurred()) {
    handleTimeout();
    return;
  }
  timeoutsInRow = 0;
  sendReading(mm, mm < 8000);   // ~8190 means "nothing in range"
#endif
}

// ---------- commands from the browser ----------
void handleCommand(const char *cmd) {
  if (strcmp(cmd, "B") == 0) {
    beep(2000, 120);
  } else if (strcmp(cmd, "I") == 0) {
    if (sensorOk) printReady();
    else Serial.println(F("E,SENSOR_NOT_FOUND"));
  }
  // anything else: ignored
}

void readCommands() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\n' || c == '\r') {
      if (cmdLen > 0) {
        cmdBuf[cmdLen] = '\0';
        handleCommand(cmdBuf);
        cmdLen = 0;
      }
    } else if (cmdLen < sizeof(cmdBuf) - 1) {
      cmdBuf[cmdLen++] = c;
    } else {
      cmdLen = 0;   // too long: throw it away
    }
  }
}

// ---------- Arduino entry points ----------
void setup() {
  Serial.begin(BAUD);
  // Native-USB boards (XIAO C3): wait up to 1.5 s for the PC, never forever.
  unsigned long t0 = millis();
  while (!Serial && millis() - t0 < 1500) { delay(10); }

#if STATUS_LED_PIN >= 0
  pinMode(STATUS_LED_PIN, OUTPUT);
#endif
  setLed(false);

#if defined(ARDUINO_ARCH_ESP32)
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
#else
  Wire.begin();
  #if defined(ARDUINO_ARCH_AVR) && AVR_DISABLE_INTERNAL_PULLUPS
  digitalWrite(SDA, LOW);   // switch off the internal 5 V pull-ups
  digitalWrite(SCL, LOW);
  #endif
#endif
  Wire.setClock(400000);    // 400 kHz I2C (supported by both sensors)

  Serial.println(F("S,BOOT," BOARD_NAME));
  tryInit();
  beep(1500, 80);           // one short beep = powered on
}

void loop() {
  readCommands();

  if (!sensorOk) {
    // Blink the LED and retry the sensor every RETRY_MS.
    setLed((millis() / 250) % 2);
    if (lastInitTry == 0 || millis() - lastInitTry >= RETRY_MS) tryInit();
    return;
  }

  pollSensor();
}
