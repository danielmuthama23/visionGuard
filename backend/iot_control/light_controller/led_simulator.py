# iot_control/light_controller/led_simulator.py
import logging
from gpiozero import LED  # Replace with mock for non-RPi systems

logger = logging.getLogger(__name__)

class LEDController:
    def __init__(self):
        self.lights = {}
        
    def _get_or_create_led(self, lot_id, pin):
        if lot_id not in self.lights:
            try:
                self.lights[lot_id] = {
                    'red': LED(pin[0]),
                    'green': LED(pin[1])
                }
            except Exception as e:
                logger.error(f"LED initialization failed: {str(e)}")
                return None
        return self.lights[lot_id]

    def set_red(self, lot_id, pin=(17, 27)):
        led = self._get_or_create_led(lot_id, pin)
        if led:
            led['red'].on()
            led['green'].off()
            logger.info(f"{lot_id} status: RED")

    def set_green(self, lot_id, pin=(17, 27)):
        led = self._get_or_create_led(lot_id, pin)
        if led:
            led['red'].off()
            led['green'].on()
            logger.info(f"{lot_id} status: GREEN")

    def cleanup(self):
        for lot in self.lights.values():
            lot['red'].close()
            lot['green'].close()