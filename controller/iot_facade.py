import requests
from typing import Dict, Any, List, Optional, Callable
from devices.base_device import Device

class RequestHandler:
    """Dependency for handling HTTP requests"""
    
    @staticmethod
    def get(url: str, timeout: int = 5) -> requests.Response:
        return requests.get(url, timeout=timeout)
    
    @staticmethod
    def post(url: str, timeout: int = 5) -> requests.Response:
        return requests.post(url, timeout=timeout)

class ActionHandler:
    """Handler for device actions using strategy pattern"""
    
    def __init__(self, request_handler: RequestHandler):
        self.request_handler = request_handler
    
    def handle_power_action(self, device: Device, state: str) -> bool:
        response = self.request_handler.post(
            f"http://{device.host}:{device.port}/power/{state}",
            timeout=5
        )
        return response.status_code == 200
    
    def handle_volume_action(self, device: Device, level: int) -> bool:
        response = self.request_handler.post(
            f"http://{device.host}:{device.port}/set_volume/{level}",
            timeout=5
        )
        return response.status_code == 200
    
    def handle_brightness_action(self, device: Device, level: int) -> bool:
        response = self.request_handler.post(
            f"http://{device.host}:{device.port}/set_brightness/{level}",
            timeout=5
        )
        return response.status_code == 200
    
    def handle_position_action(self, device: Device, value: int) -> bool:
        response = self.request_handler.post(
            f"http://{device.host}:{device.port}/position/{value}",
            timeout=5
        )
        return response.status_code == 200

class IOTFacade:
    """Facade to handle HTTP communication with device microservices"""
    
    def __init__(self, request_handler: Optional[RequestHandler] = None, 
                 action_handler: Optional[ActionHandler] = None):
        self._devices: Dict[str, Device] = {}
        self.request_handler = request_handler or RequestHandler()
        self.action_handler = action_handler or ActionHandler(self.request_handler)
        
        # Action strategy mapping
        self._action_strategies: Dict[str, Callable] = {
            "power": self.action_handler.handle_power_action,
            "set_volume": self.action_handler.handle_volume_action,
            "set_brightness": self.action_handler.handle_brightness_action,
            "position": self.action_handler.handle_position_action
        }
    
    def register_device(self, device: Device) -> str:
        """Register a device with the facade"""
        self._devices[device.device_id] = device
        return device.device_id
    
    def get_device_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get status from a specific device"""
        if device_id not in self._devices:
            return None
        
        device = self._devices[device_id]
        try:
            response = self.request_handler.get(f"http://{device.host}:{device.port}/status", timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting status for {device_id}: {e}")
        return None
    
    def perform_device_action(self, device_id: str, action: str, **kwargs) -> bool:
        """Perform an action on a specific device using strategy pattern"""
        if device_id not in self._devices:
            return False
        
        device = self._devices[device_id]
        
        if action in self._action_strategies:
            handler = self._action_strategies[action]
            return handler(device, **kwargs)
        
        return False
    
    def get_all_status(self) -> List[Dict[str, Any]]:
        """Get status from all registered devices"""
        status_list = []
        for device_id in self._devices:
            status = self.get_device_status(device_id)
            if status:
                status_list.append(status)
        return status_list