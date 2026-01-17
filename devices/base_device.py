from abc import ABC, abstractmethod
from typing import Dict, Any, Type


class Device(ABC):
    """Base device interface"""
    
    def __init__(self, device_id: str, host: str = "127.0.0.1", port: int = 8000):
        self.device_id = device_id
        self.host = host
        self.port = port
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current device status"""
        pass
    
    @abstractmethod
    def perform_action(self, action: str, **kwargs) -> bool:
        """Perform device action"""
        pass


class LoggingDeviceDecorator(Device):
    """Decorator to add logging to device operations"""
    
    def __init__(self, device: Device):
        self._device = device
        super().__init__(device.device_id, device.host, device.port)
    
    def get_status(self) -> Dict[str, Any]:
        print(f"Getting status for device: {self._device.device_id}")
        return self._device.get_status()
    
    def perform_action(self, action: str, **kwargs) -> bool:
        print(f"Performing action '{action}' on device: {self._device.device_id}")
        result = self._device.perform_action(action, **kwargs)
        print(f"Action result: {result}")
        return result


class DeviceFactory:
    """Factory for creating devices with lazy imports"""
    
    @staticmethod
    def create_device(device_type: str, device_id: str, host: str = "127.0.0.1", port: int = None) -> Device:
        if device_type == "smart_speaker":
            from devices.smart_speaker import SmartSpeakerDevice
            return SmartSpeakerDevice(device_id, host, port or 8001)
        elif device_type == "smart_light":
            from devices.smart_light import SmartLightDevice
            return SmartLightDevice(device_id, host, port or 8002)
        elif device_type == "smart_curtains":
            from devices.smart_curtains import SmartCurtainsDevice
            return SmartCurtainsDevice(device_id, host, port or 8003)
        else:
            raise ValueError(f"Unknown device type: {device_type}")