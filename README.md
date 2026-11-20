# SmartBedsideSystem

*SmartBedsideSystem* is a bedside care system built on a Raspberry Pi that monitors a patient's vital signs, manages emergency alarms, and regulates oxygen delivery.

The system includes the following sensors and actuators:

- A **pulse oximeter and heart-rate sensor** (MAX30102), used to measure blood oxygen saturation.
- An **active buzzer module** (KY-012), used to raise an emergency alarm.
- A **pushbutton** (B3F-1020), used to silence the emergency alarm.
- A **servo motor** (MG90S), used to regulate the oxygen delivery valve.

The buzzer, the pushbutton, and the servo motor are connected to the Raspberry Pi through GPIO pins, while the MAX30102 sensor communicates over the I²C bus (BOARD pins 3 and 5), which is fully managed by the sensor's library. The GPIO numbering is already configured in BOARD mode (i.e., GPIO pins are referred to by their physical number on the board).

## Instructions for You

- You are asked to develop *SmartBedsideSystem*.
- You **CANNOT** change the signatures of the provided methods, move the provided methods to other classes, or change the names of the provided classes and instance variables.
- If you belong to the **NO_LLM group**, you **CAN** use the internet to consult Python API documentation or QA websites (e.g., Stack Overflow) using **DuckDuckGo**, but you **CANNOT** use any AI tools (e.g., Microsoft Copilot).
- If you belong to the **LLM group**, you **CAN** use **Microsoft Copilot** as your only AI tool.
- You **CANNOT** interact with your colleagues. Work independently and do your best!
- Each **USER STORY** is accompanied by an **ACCEPTANCE TEST SUITE**.
- The *SmartBedsideSystem* requirements are divided into a set of **USER STORIES**, which serve as a to-do list (see the _Issues_ section).
- You should be able to develop *SmartBedsideSystem* incrementally, without having to understand all the user stories upfront. **DO NOT read ahead.** Instead, address the user stories one at a time, following the order in which they are provided. Start by implementing the requirements of the first user story. Once a story has been **IMPLEMENTED**, move on to the **NEXT** one. A story is considered **IMPLEMENTED** when its acceptance test suite **PASSES**. Naturally, all acceptance test suites for previously implemented stories must continue to pass as well. You may need to revise your program as you progress through subsequent user stories.
- Each time you **IMPLEMENT** a user story, **COMMIT** your changes.
- Whenever a user story requires you to handle an error situation, raise a `SmartBedsideError` exception. Do **NOT** add error checks that are not required by the user stories.

## Project Structure

The project is organized as follows:

```
smartbedsidesystem/
├── mock/
│   ├── __init__.py                  # Marks the folder as a Python package
│   ├── GPIO.py                      # Mock of the RPi.GPIO library
│   └── max30102.py                  # Mock of the DFRobot_BloodOxygen_S library (MAX30102 sensor)
├── src/
│   ├── __init__.py                  # Marks the folder as a Python package
│   ├── smart_bedside_error.py       # SmartBedsideError exception
│   └── smart_bedside_system.py      # SmartBedsideSystem class (to be implemented)
├── test/
│   ├── __init__.py                  # Marks the folder as a Python package
│   └── test_smart_bedside_system.py # Acceptance test suites for the user stories
└── README.md
```

**Note:** All acceptance tests are in the file `test/test_smart_bedside_system.py`, grouped into one test class per user story (`TestUserStory1`, `TestUserStory2`, ..., `TestUserStory5`). In PyCharm, you can run them in two ways:

- **Tests of all user stories (recommended):** run the test file as usual (e.g., right-click on `test_smart_bedside_system.py` and select *Run*).
- **Tests of a single user story:** click the green run icon next to the corresponding class (e.g., `class TestUserStory2`) and select *Run*. This can help you focus on a specific user story, for example while fixing a failing test.

We recommend to **ALWAYS** run the tests of **ALL** user stories: a change made for the current user story may break a previously implemented one. In any case, before **COMMITTING**, you **MUST** run the tests of all user stories and make sure that they pass.

## API Usage

Take a few minutes to understand, at a high level, how the API works. If you do not fully understand the API, do not worry: further details will be provided in the individual user stories (see the _Issues_ section).

## User Stories

### User Story #1 – Read Patient's Blood Oxygen Saturation (SpO₂)

*SmartBedsideSystem* relies on a **Pulse Oximeter and Heart-Rate Sensor (MAX30102)** to monitor the patient's blood oxygen saturation (SpO₂).

Communication with the sensor takes place via the I²C protocol, using the `DFRobot_BloodOxygen_S` library. This library is mocked for this project; see the file `max30102.py` in the `mock` folder.

The sensor has **NOT** yet been initialized in the `SmartBedsideSystem` constructor. To access it, use the `SmartBedsideSystem.spo2_hr_sensor` instance variable, which **MUST** be initialized in the constructor by instantiating a `DFRobot_BloodOxygen_S` object.

**DFRobot_BloodOxygen_S Configuration**

Before reading SpO₂, the following initialization steps are required:

1. Call `DFRobot_BloodOxygen_S.begin() -> bool` to initialize I²C communication with the MAX30102 sensor.
2. Call `DFRobot_BloodOxygen_S.sensor_start_collect() -> None` to start raw data acquisition.

**Note:** `begin()` returns `True` if the sensor was initialized successfully and `False` otherwise. For this project, assume that initialization always succeeds: **IGNORE** the value returned by `begin()` and do **NOT** raise a `SmartBedsideError` based on it.

**Reading SpO₂**

To retrieve the patient's current blood oxygen saturation, call the `DFRobot_BloodOxygen_S.get_spo2() -> int` method. It returns an integer representing the SpO₂ percentage.

**MAX30102 Sensor Description**

The sensor **only** returns SpO₂ values ranging from `70` to `100`, inclusive. If it cannot determine a valid reading, it returns `-1` (e.g., when the finger slips off).

**Requirements**

- Update the `SmartBedsideSystem` constructor to:
  - Initialize `SmartBedsideSystem.spo2_hr_sensor` by creating a new instance of `DFRobot_BloodOxygen_S` using its default constructor (i.e., without passing any arguments).
  - Configure the sensor by calling `begin()` followed by `sensor_start_collect()`, as described above (ignore the value returned by `begin()`).
- Implement `SmartBedsideSystem.read_vital_signs() -> int` to retrieve and return the patient's SpO₂ percentage by calling `get_spo2()`.
  - If the sensor returns `-1`, the method must raise a `SmartBedsideError`.
  - Otherwise, return the SpO₂ reading as an integer.

Acceptance tests: `TestUserStory1` in `test/test_smart_bedside_system.py`.

> **Reminder:** Once all the tests in `TestUserStory1` pass, **COMMIT** your changes before moving on to User Story #2.

### User Story #2 – Manage the Oxygen Saturation Alarm

The system is equipped with an **active buzzer module (KY-012)** to alert medical staff whenever the patient's blood oxygen saturation (SpO₂) drops below a critical level.

The alarm buzzer is connected to the Raspberry Pi using **BOARD pin 22**. A constant identifying this pin is already defined in the `smart_bedside_system.py` file.

The buzzer is controlled using the `GPIO.output(channel, value) -> None` function of the `RPi.GPIO` library (this library is mocked for this project; see the file `GPIO.py` in the `mock` folder), where `channel` is the GPIO pin and `value` is a boolean value (`False` or `True`):

- `True`: turns the buzzer ON.
- `False`: turns the buzzer OFF.

The buzzer pin has **NOT** yet been configured as an output pin in the `SmartBedsideSystem` constructor.

To keep track of the alarm status (ON or OFF), use the boolean instance variable `SmartBedsideSystem.alarm_on`.

**Alarm Rules**

Use the patient's SpO₂ reading (see User Story #1) to determine whether the alarm should be activated:

- If SpO₂ `< 88`, turn **ON** the alarm buzzer and set `SmartBedsideSystem.alarm_on` to `True`.
- Otherwise (SpO₂ `>= 88`), turn **OFF** the alarm buzzer and set `SmartBedsideSystem.alarm_on` to `False`.

**Requirements**

- Update the `SmartBedsideSystem` constructor to:
  - Configure BOARD pin 22 as an output pin, using the corresponding constant defined in `smart_bedside_system.py`.
  - Initialize `SmartBedsideSystem.alarm_on` to `False`, indicating that the alarm is OFF.
- Implement `SmartBedsideSystem.manage_alarm() -> None` to:
  - Retrieve the patient's SpO₂ reading by calling `SmartBedsideSystem.read_vital_signs() -> int`.
  - If `SmartBedsideSystem.read_vital_signs()` raises a `SmartBedsideError` (invalid SpO₂ reading), do **NOT** catch it: let it propagate to the caller, leaving the alarm buzzer and `SmartBedsideSystem.alarm_on` unchanged.
  - Control the alarm buzzer according to the alarm rules described above.
  - Update `SmartBedsideSystem.alarm_on` to reflect the current alarm status.

Acceptance tests: `TestUserStory2` in `test/test_smart_bedside_system.py`.

> **Reminder:** Once all the tests in `TestUserStory2` pass (together with those of the previous user stories), **COMMIT** your changes before moving on to User Story #3.

### User Story #3 – Stop the Oxygen Saturation Alarm

The system is equipped with a **pushbutton (B3F-1020)** that allows medical staff to stop the alarm while attending to the patient.

The pushbutton is connected to **BOARD pin 16**. A constant identifying this pin is already defined in the `smart_bedside_system.py` file.

The pushbutton is read using the `GPIO.input(channel) -> bool` function, where `channel` is the GPIO pin. The function returns a boolean value (`False` or `True`):

- `True`: the button is **pressed**.
- `False`: the button is **not pressed**.

The pushbutton pin has **NOT** yet been configured as an input pin in the `SmartBedsideSystem` constructor.

**Pushbutton Behavior**

- If the button is pressed (`True`), turn **OFF** the alarm buzzer and set `SmartBedsideSystem.alarm_on` to `False`.
- If the button is not pressed (`False`), do nothing and leave the alarm buzzer and its status unchanged.

**Note:** Stopping the alarm does not affect `SmartBedsideSystem.manage_alarm()`: if the SpO₂ is still critical, the next call to `manage_alarm()` turns the alarm ON again.

**Requirements**

- Update the `SmartBedsideSystem` constructor to configure BOARD pin 16 as an input pin, using the corresponding constant defined in `smart_bedside_system.py`.
- Implement `SmartBedsideSystem.stop_alarm() -> None` to:
  - Read the pushbutton, determining whether it is pressed.
  - Control the alarm buzzer according to the pushbutton behavior described above.
  - Update `SmartBedsideSystem.alarm_on` to reflect the resulting alarm status.

Acceptance tests: `TestUserStory3` in `test/test_smart_bedside_system.py`.

> **Reminder:** Once all the tests in `TestUserStory3` pass (together with those of the previous user stories), **COMMIT** your changes before moving on to User Story #4.

### User Story #4 – Control the Oxygen Delivery Valve

Oxygen delivery to the patient is regulated by a valve controlled by an **MG90S servo motor**.

The servo motor is connected to the Raspberry Pi using **BOARD pin 12**. A constant identifying this pin is already defined in the `smart_bedside_system.py` file.

The servo motor has **NOT** yet been configured or initialized in the `SmartBedsideSystem` constructor. Specifically:

- The servo motor's GPIO pin has **NOT** yet been configured as an output pin.
- The PWM instance has **NOT** yet been created.
- The PWM signal has **NOT** yet been started.

To access the servo motor, use the `SmartBedsideSystem.o2_servo` instance variable, which **MUST** be initialized in the `SmartBedsideSystem` constructor by creating a `PWM` instance configured with the servo's GPIO pin and operating frequency (the PWM signal must also be started with the appropriate initial duty cycle).

The servo motor's current angle is stored in the instance variable `SmartBedsideSystem.o2_valve_angle`.

**MG90S Servo Motor Specifications**

- Operates at a PWM frequency of `50` Hz, corresponding to a period of `20` ms.
- The pulse width varies linearly from `1` ms to `2` ms:
  - `1` ms corresponds to `0` degrees (valve fully closed), with a duty cycle of `5.0%`.
  - `2` ms corresponds to `180` degrees (valve fully open), with a duty cycle of `10.0%`.
- The duty cycle corresponding to a target `angle` in the range `[0, 180]` is calculated using:

```
duty_cycle = 5.0 + (angle / 180.0) * 5.0
```

**Requirements**

- Update the `SmartBedsideSystem` constructor to:
   - Configure BOARD pin 12 as an output pin, using the corresponding constant defined in `smart_bedside_system.py`.
   - Create a PWM instance on BOARD pin 12, using the corresponding constant defined in `smart_bedside_system.py`, with a frequency of `50` Hz. Assign this instance to `SmartBedsideSystem.o2_servo`.
   - Start the PWM signal with a duty cycle of `5.0%`, corresponding to the fully closed valve position.
   - Initialize the instance variable `SmartBedsideSystem.o2_valve_angle` to `0.0` degrees.

- Implement `SmartBedsideSystem.set_o2_valve_angle(angle: float) -> None` to control the oxygen delivery valve:
   - Check that `angle` is within the inclusive range `0.0` to `180.0` degrees. If it is outside this range, raise a `SmartBedsideError`.
   - Calculate the corresponding PWM duty cycle using the formula above.
   - Set the servo motor's position by changing its duty cycle.
   - Update `SmartBedsideSystem.o2_valve_angle` with the target angle.

Acceptance tests: `TestUserStory4` in `test/test_smart_bedside_system.py`.

> **Reminder:** Once all the tests in `TestUserStory4` pass (together with those of the previous user stories), **COMMIT** your changes before moving on to User Story #5.

### User Story #5 – Automatically Control the Oxygen Delivery Valve

The oxygen delivery valve is automatically opened or closed according to the patient's blood oxygen saturation (SpO₂).

The system reads the patient's SpO₂ (see User Story #1) and controls the MG90S servo motor (see User Story #4).

**Oxygen Valve Behavior**

- If SpO₂ `< 95`, the system fully opens the oxygen delivery valve by setting its angle to `180.0` degrees.
- If SpO₂ `>= 95`, the system fully closes the oxygen delivery valve by setting its angle to `0.0` degrees.

**Requirements**

- Implement `SmartBedsideSystem.manage_oxygen_valve() -> None` to automatically regulate the oxygen delivery valve based on the patient's SpO₂ reading:
  - Retrieve the patient's SpO₂ reading by calling `SmartBedsideSystem.read_vital_signs() -> int`.
  - If `SmartBedsideSystem.read_vital_signs()` raises a `SmartBedsideError` (invalid SpO₂ reading), do **NOT** catch it: let it propagate to the caller, leaving the valve and `SmartBedsideSystem.o2_valve_angle` unchanged.
  - Set the valve angle according to the behavior described above.

Acceptance tests: `TestUserStory5` in `test/test_smart_bedside_system.py`.

> **Reminder:** Once all the tests in `TestUserStory5` pass (together with those of the previous user stories), **COMMIT** and **PUSH** your changes to complete the task.
