from homeassistant.components.cover import (
    DEVICE_CLASS_AWNING,
    DEVICE_CLASS_BLIND,
    DEVICE_CLASS_CURTAIN,
    DEVICE_CLASS_GARAGE,
    DEVICE_CLASS_SHUTTER,
    DEVICE_CLASS_WINDOW,
)

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_SMOKE,
    DEVICE_CLASS_MOTION,
    DEVICE_CLASS_OPENING
)

"""Constants for the Tahoma integration."""

DOMAIN = "tahoma"

# Tahoma to Home Assistant mapping
TAHOMA_TYPES = {
    "Light": "light",
    "ExteriorScreen": "cover",
    "Pergola": "cover",
    "RollerShutter": "cover",
    "Window": "cover",
    "RemoteController": "",
    "HeatingSystem": "climate",
    "TemperatureSensor": "sensor",
    "LightSensor": "sensor",
    "DoorLock": "lock",
    "OnOff": "switch",
    "HumiditySensor": "sensor",
    "GarageDoor": "cover",
    "ContactSensor": "binary_sensor",
    "SmokeSensor": "binary_sensor",
    "MotionSensor": "binary_sensor",
    "ExteriorVenetianBlind": "cover"
}

TAHOMA_COVER_DEVICE_CLASSES = {
    "ExteriorScreen": DEVICE_CLASS_BLIND,
    "Pergola": DEVICE_CLASS_AWNING,
    "RollerShutter": DEVICE_CLASS_SHUTTER,
    "Window": DEVICE_CLASS_WINDOW,
    "GarageDoor": DEVICE_CLASS_GARAGE,
    "HorizontalAwning": DEVICE_CLASS_AWNING,
    "ExteriorVenetianBlind": DEVICE_CLASS_BLIND,
    "VeluxInteriorBlind": DEVICE_CLASS_BLIND
}

TAHOMA_BINARY_SENSOR_DEVICE_CLASSES = {
    "SmokeSensor": DEVICE_CLASS_SMOKE,
    "MotionSensor": DEVICE_CLASS_MOTION,
    "ContactSensor": DEVICE_CLASS_OPENING 
}

# Tahoma Attributes
ATTR_MEM_POS = "memorized_position"
ATTR_RSSI_LEVEL = "rssi_level"
ATTR_LOCK_START_TS = "lock_start_ts"
ATTR_LOCK_END_TS = "lock_end_ts"
ATTR_LOCK_LEVEL = "lock_level"
ATTR_LOCK_ORIG = "lock_originator"

# Tahoma internal device states
CORE_RSSI_LEVEL_STATE = "core:RSSILevelState"
CORE_STATUS_STATE = "core:StatusState"
CORE_CLOSURE_STATE = "core:ClosureState"
CORE_DEPLOYMENT_STATE = "core:DeploymentState"
CORE_SLATS_ORIENTATION_STATE = "core:SlatsOrientationState"
CORE_PRIORITY_LOCK_TIMER_STATE = "core:PriorityLockTimerState"
CORE_SENSOR_DEFECT_STATE = "core:SensorDefectState"

IO_PRIORITY_LOCK_LEVEL_STATE = "io:PriorityLockLevelState"
IO_PRIORITY_LOCK_ORIGINATOR_STATE = "io:PriorityLockOriginatorState"

# Commands
COMMAND_SET_CLOSURE = "setClosure"
COMMAND_SET_POSITION = "setPosition"