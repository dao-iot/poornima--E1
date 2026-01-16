n this project, ThingsBoard Cloud is used as the IoT platform to receive EV sensor data via MQTT and display it on a real-time dashboard.

MQTT Broker Details

Platform: ThingsBoard Cloud

Protocol: MQTT

QoS: 1 (At least once delivery)

Authentication: Device Access Token

Topic Used (As per ThingsBoard Standard)

ThingsBoard uses a fixed telemetry topic:

v1/devices/me/telemetry


{device_id} is handled internally by ThingsBoard using the access token

No custom topic hierarchy is required

Telemetry Message Format
{
  "motor_rpm": 5420,
  "battery_voltage": 62.4,
  "battery_current": -85.2,
  "soc_percent": 67,
  "vehicle_speed_kmh": 45,
  "battery_temp_c": 57.2
}

Data Flow

EV sensor data is generated at the edge

Data is validated and processed locally

Telemetry is published to v1/devices/me/telemetry

ThingsBoard visualizes data

Subscription & Visualization

ThingsBoard automatically subscribes to device telemetry