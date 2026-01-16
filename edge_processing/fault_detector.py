import sys
import os
import time
import json

# PROJECT ROOT PATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from data_logger.database import fetch_last_n_readings

print("=== FAULT DETECTION ENGINE (PHASE 4 – EDGE PROCESSING) ===")

# PDF-ALIGNED THRESHOLDS (UNCHANGED)
BATTERY_TEMP_WARNING = 55
BATTERY_TEMP_CRITICAL = 60

BATTERY_VOLT_WARNING = 50
BATTERY_VOLT_CRITICAL = 48



# FAULT CHECK FUNCTION

def check_faults():
    faults = []

    temp = fetch_last_n_readings("motor_temp_c", 2)
    volt = fetch_last_n_readings("battery_voltage_v", 2)
    curr = fetch_last_n_readings("battery_current_a", 2)
    speed = fetch_last_n_readings("vehicle_speed_kmh", 1)
    rpm = fetch_last_n_readings("motor_rpm", 1)
    soc = fetch_last_n_readings("soc_percent", 2)

    # Battery Temperature
    if temp:
        t_val = temp[0]["value"]

        if t_val > BATTERY_TEMP_CRITICAL:
            faults.append(("CRITICAL", "Battery Temp > 60°C", t_val, "°C"))
        elif t_val > BATTERY_TEMP_WARNING:
            faults.append(("WARNING", "Battery Temp > 55°C", t_val, "°C"))

        if len(temp) == 2 and abs(temp[0]["value"] - temp[1]["value"]) > 10:
            faults.append(("WARNING", "Battery Temp Rapid Rise", t_val, "°C"))

    # Battery Voltage
    if volt:
        v_val = volt[0]["value"]

        if v_val < BATTERY_VOLT_CRITICAL:
            faults.append(("CRITICAL", "Battery Voltage < 48V", v_val, "V"))
        elif v_val < BATTERY_VOLT_WARNING:
            faults.append(("WARNING", "Battery Voltage < 50V", v_val, "V"))

        if len(volt) == 2 and (volt[1]["value"] - volt[0]["value"]) > 5:
            faults.append(("ERROR", "Battery Voltage Sudden Drop", v_val, "V"))

    # Correlation: RPM vs Speed
    if rpm and speed:
        if rpm[0]["value"] > 0 and speed[0]["value"] == 0:
            faults.append(("WARNING", "RPM > 0 but Speed = 0", rpm[0]["value"], "rpm"))

    # Correlation: Current vs SOC
    if curr and soc and len(soc) == 2:
        if curr[0]["value"] > 0 and soc[0]["value"] > soc[1]["value"]:
            faults.append(("ERROR", "SOC Increasing While Discharging", soc[0]["value"], "%"))

    return faults


# CONTINUOUS MONITORING

while True:
    detected_faults = check_faults()

    status = {
        "overall": "NORMAL",
        "alerts": []
    }

    if detected_faults:
        for severity, msg, value, unit in detected_faults:
            status["alerts"].append({
                "severity": severity,
                "message": msg,
                "value": value,
                "unit": unit
            })

        severities = [f[0] for f in detected_faults]
        if "CRITICAL" in severities:
            status["overall"] = "CRITICAL"
        elif "ERROR" in severities:
            status["overall"] = "ERROR"
        else:
            status["overall"] = "WARNING"

    output_json = {
        "device_id": "EV_TEST_001",
        "timestamp": int(time.time() * 1000),
        "status": status
    }

    # ALWAYS PRINT (Heartbeat + Faults)
    print(json.dumps(output_json, indent=2))

    time.sleep(2)
