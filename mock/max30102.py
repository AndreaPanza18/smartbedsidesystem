"""
Mocked module for the DFRobot Gravity MAX30102 Heart Rate and Oximeter Sensor (`DFRobot_BloodOxygen_S`).
Exposes the exact API of the real Python library (`pinpong.libs.dfrobot_max30102.DFRobot_BloodOxygen_S`
/ `DFRobot_BloodOxygen_S` repository for SKU SEN0518 / SEN0344).

Hardware & Protocol Specification:
- Sensor: DFRobot Gravity MAX30102 PPG Heart Rate and Oximeter Sensor (I2C mode).
- Interface: Native digital I2C protocol (internal 18-bit ADC and onboard MCU integrated on the module;
  no external ADC module is required).
- Raspberry Pi Connections (BOARD mode):
  * Pin 1: 3.3V Power (`VCC`)
  * Pin 3 (GPIO 2 / SDA1): I2C Data (`SDA`)
  * Pin 5 (GPIO 3 / SCL1): I2C Clock (`SCL`)
  * Pin 6: Ground (`GND`)
- Default I2C Address: `0x57`
"""


class DFRobot_BloodOxygen_S:
    """
    Mock of the official `DFRobot_BloodOxygen_S` class for the MAX30102 I2C sensor.
    Exposes strictly the real hardware library methods (`begin`, `sensor_start_collect`,
    `sensor_end_collect`, `get_spo2`, `get_heartbeat`, `get_temperature_c`).
    """

    I2C_ADDRESS = 0x57

    def __init__(self, bus_num: int = 1, i2c_addr: int = I2C_ADDRESS):
        self.bus_num = bus_num
        self.i2c_addr = i2c_addr
        self._collecting = False

    def begin(self) -> bool:
        """Initializes communication with the MAX30102 sensor over I2C."""
        return True

    def sensor_start_collect(self) -> None:
        """Starts the onboard PPG data acquisition and calculation cycle."""
        self._collecting = True

    def sensor_end_collect(self) -> None:
        """Stops the onboard PPG data acquisition cycle."""
        self._collecting = False

    def get_spo2(self) -> int:
        """Returns the blood oxygen saturation percentage (SpO2 %)."""
        return 97

    def get_heartbeat(self) -> int:
        """Returns the patient's heart rate in beats per minute (BPM)."""
        return 75

    def get_temperature_c(self) -> float:
        """Returns the sensor's onboard die temperature in degrees Celsius."""
        return 36.8
