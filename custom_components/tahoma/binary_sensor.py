"""Support for TaHoma binary sensors."""
from datetime import timedelta
import logging
from typing import Optional

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOTION,
    DEVICE_CLASS_OCCUPANCY,
    DEVICE_CLASS_OPENING,
    DEVICE_CLASS_SMOKE,
    BinarySensorEntity,
)
from homeassistant.const import STATE_OFF, STATE_ON

from .const import DOMAIN, TAHOMA_TYPES
from .tahoma_device import TahomaDevice

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=120)

CORE_BUTTON_STATE = "core:ButtonState"
CORE_CONTACT_STATE = "core:ContactState"
CORE_GAS_DETECTION_STATE = "core:GasDetectionState"
CORE_OCCUPANCY_STATE = "core:OccupancyState"
CORE_RAIN_STATE = "core:RainState"
CORE_SMOKE_STATE = "core:SmokeState"
CORE_WATER_DETECTION_STATE = "core:WaterDetectionState"

DEVICE_CLASS_BUTTON = "button"
DEVICE_CLASS_GAS = "gas"
DEVICE_CLASS_RAIN = "rain"
DEVICE_CLASS_WATER = "water"

ICON_WATER = "mdi:water"
ICON_WATER_OFF = "mdi:water-off"
ICON_WAVES = "mdi:waves"
ICON_WEATHER_RAINY = "mdi:weather-rainy"

IO_VIBRATION_STATE = "io:VibrationDetectedState"

STATE_OPEN = "open"
STATE_PERSON_INSIDE = "personInside"
STATE_DETECTED = "detected"
STATE_PRESSED = "pressed"

TAHOMA_BINARY_SENSOR_DEVICE_CLASSES = {
    "AirFlowSensor": DEVICE_CLASS_GAS,
    "CarButtonSensor": DEVICE_CLASS_BUTTON,
    "SmokeSensor": DEVICE_CLASS_SMOKE,
    "OccupancySensor": DEVICE_CLASS_OCCUPANCY,
    "MotionSensor": DEVICE_CLASS_MOTION,
    "ContactSensor": DEVICE_CLASS_OPENING,
    "WindowHandle": DEVICE_CLASS_OPENING,
    "RainSensor": DEVICE_CLASS_RAIN,
    "WaterDetectionSensor": DEVICE_CLASS_WATER,
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the TaHoma sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    controller = data.get("controller")

    entities = [
        TahomaBinarySensor(device, controller)
        for device in data.get("devices")
        if TAHOMA_TYPES[device.uiclass] == "binary_sensor"
    ]

    async_add_entities(entities)


class TahomaBinarySensor(TahomaDevice, BinarySensorEntity):
    """Representation of a TaHoma Binary Sensor."""

    def __init__(self, tahoma_device, controller):
        """Initialize the sensor."""
        super().__init__(tahoma_device, controller)

        self._state = None

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._state == STATE_ON

    @property
    def device_class(self):
        """Return the class of the device."""
        return (
            TAHOMA_BINARY_SENSOR_DEVICE_CLASSES.get(self.tahoma_device.widget)
            or TAHOMA_BINARY_SENSOR_DEVICE_CLASSES.get(self.tahoma_device.uiclass)
            or None
        )

    @property
    def icon(self) -> Optional[str]:
        """Return the icon to use in the frontend, if any."""
        if self.device_class == DEVICE_CLASS_WATER:
            if self.is_on:
                return ICON_WATER
            else:
                return ICON_WATER_OFF

        icons = {
            DEVICE_CLASS_GAS: ICON_WAVES,
            DEVICE_CLASS_RAIN: ICON_WEATHER_RAINY,
        }

        return icons.get(self.device_class)

    def update(self):
        """Update the state."""
        if self.should_wait():
            self.schedule_update_ha_state(True)
            return

        self.controller.get_states([self.tahoma_device])

        states = self.tahoma_device.active_states

        if CORE_CONTACT_STATE in states:
            self.current_value = states.get(CORE_CONTACT_STATE) == STATE_OPEN

        if CORE_OCCUPANCY_STATE in states:
            self.current_value = states.get(CORE_OCCUPANCY_STATE) == STATE_PERSON_INSIDE

        if CORE_SMOKE_STATE in states:
            self.current_value = states.get(CORE_SMOKE_STATE) == STATE_DETECTED

        if CORE_RAIN_STATE in states:
            self.current_value = states.get(CORE_RAIN_STATE) == STATE_DETECTED

        if CORE_WATER_DETECTION_STATE in states:
            self.current_value = (
                states.get(CORE_WATER_DETECTION_STATE) == STATE_DETECTED
            )

        if CORE_GAS_DETECTION_STATE in states:
            self.current_value = states.get(CORE_GAS_DETECTION_STATE) == STATE_DETECTED

        if IO_VIBRATION_STATE in states:
            self.current_value = states.get(IO_VIBRATION_STATE) == STATE_DETECTED

        if CORE_BUTTON_STATE in states:
            self.current_value = states.get(CORE_BUTTON_STATE) == STATE_PRESSED

        if self.current_value:
            self._state = STATE_ON
        else:
            self._state = STATE_OFF
