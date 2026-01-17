from typing import Dict, List, Any, Optional
import sys
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "devices"))

try:
    from controller.iot_facade import IOTFacade
    from devices.base_device import Device, LoggingDeviceDecorator
    from devices.smart_speaker import SmartSpeakerDevice
    from devices.smart_light import SmartLightDevice
    from devices.smart_curtains import SmartCurtainsDevice 
    print("Controller imports successful")
except ImportError as e:
    print(f"Controller import error: {e}")
    from iot_facade import IOTFacade
    from devices.base_device import Device, LoggingDeviceDecorator
    from devices.smart_speaker import SmartSpeakerDevice
    from devices.smart_light import SmartLightDevice
    from devices.smart_curtains import SmartCurtainsDevice  
    print("Alternative imports successful")

class AppController:
    _instance: Optional['AppController'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.facade = IOTFacade()
            self._register_default_devices()
            self._initialized = True
    
    def _register_default_devices(self):
        """Register default devices"""
        speaker = LoggingDeviceDecorator(SmartSpeakerDevice("speaker_001", "127.0.0.1", 8001))
        light = LoggingDeviceDecorator(SmartLightDevice("light_001", "127.0.0.1", 8002))
        curtains = LoggingDeviceDecorator(SmartCurtainsDevice("curtains_001", "127.0.0.1", 8003))
        
        self.facade.register_device(speaker)
        self.facade.register_device(light)
        self.facade.register_device(curtains)
        print("Devices registered")
    
    def _toggle_device(self, device_id: str, power_states: tuple) -> Dict[str, Any]:
        """Generic toggle method for all devices"""
        status = self.facade.get_device_status(device_id)
        if status:
            on_state, off_state = power_states
            current_state = off_state if status.get("is_on", status.get("is_open", False)) else on_state
            self.facade.perform_device_action(device_id, "power", state=current_state)
        return {}
    
    def toggle_speaker(self) -> Dict[str, Any]:
        return self._toggle_device("speaker_001", ("on", "off"))
    
    def set_speaker_volume(self, volume: int) -> bool:
        return self.facade.perform_device_action("speaker_001", "set_volume", level=volume)
    
    def toggle_light(self) -> Dict[str, Any]:
        return self._toggle_device("light_001", ("on", "off"))
    
    def set_light_brightness(self, brightness: int) -> bool:
        return self.facade.perform_device_action("light_001", "set_brightness", level=brightness)
    
    def toggle_curtains(self) -> Dict[str, Any]:
        return self._toggle_device("curtains_001", ("open", "close"))
    
    def set_curtains_position(self, position: int) -> bool:
        return self.facade.perform_device_action("curtains_001", "position", value=position)
    
    def get_all_status(self) -> List[Dict[str, Any]]:
        return self.facade.get_all_status()
    
    def register_new_device(self, device: Device) -> str:
        return self.facade.register_device(device)