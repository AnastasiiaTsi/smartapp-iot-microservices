import pytest
from unittest.mock import Mock, patch
import sys
import os

# Додаємо шлях до кореня проекту для імпортів
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controller.app_controller import AppController
from controller.iot_facade import IOTFacade, RequestHandler, ActionHandler
from devices.base_device import Device


class TestAppController:
    
    def test_singleton_pattern(self):
        # Очищаємо instance для тестування
        AppController._instance = None
        AppController._initialized = False
        
        controller1 = AppController()
        controller2 = AppController()
        assert controller1 is controller2
    
    def test_toggle_device_generic_method(self):
        # Очищаємо instance для тестування
        AppController._instance = None
        AppController._initialized = False
        
        controller = AppController()
        
        # Мокаємо facade
        mock_facade = Mock()
        controller.facade = mock_facade
        
        mock_facade.get_device_status.return_value = {"is_on": True}
        mock_facade.perform_device_action.return_value = True
        
        result = controller._toggle_device("test_device", ("on", "off"))
        
        mock_facade.get_device_status.assert_called_once_with("test_device")
        mock_facade.perform_device_action.assert_called_once_with(
            "test_device", "power", state="off"
        )
        assert result == {}
    
    def test_toggle_speaker(self):
        AppController._instance = None
        AppController._initialized = False
        
        controller = AppController()
        with patch.object(controller, '_toggle_device') as mock_toggle:
            controller.toggle_speaker()
            mock_toggle.assert_called_once_with("speaker_001", ("on", "off"))
    
    def test_toggle_light(self):
        AppController._instance = None
        AppController._initialized = False
        
        controller = AppController()
        with patch.object(controller, '_toggle_device') as mock_toggle:
            controller.toggle_light()
            mock_toggle.assert_called_once_with("light_001", ("on", "off"))
    
    def test_toggle_curtains(self):
        AppController._instance = None
        AppController._initialized = False
        
        controller = AppController()
        with patch.object(controller, '_toggle_device') as mock_toggle:
            controller.toggle_curtains()
            mock_toggle.assert_called_once_with("curtains_001", ("open", "close"))
    
    def test_set_speaker_volume(self):
        AppController._instance = None
        AppController._initialized = False
        
        controller = AppController()
        mock_facade = Mock()
        controller.facade = mock_facade
        mock_facade.perform_device_action.return_value = True
        
        result = controller.set_speaker_volume(75)
        
        mock_facade.perform_device_action.assert_called_once_with(
            "speaker_001", "set_volume", level=75
        )
        assert result is True


class TestIOTFacade:
    
    def test_action_strategy_pattern(self):
        mock_device = Mock()
        mock_device.host = "127.0.0.1"
        mock_device.port = 8001
        mock_device.device_id = "test_device"
        
        mock_request_handler = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request_handler.post.return_value = mock_response
        
        mock_action_handler = ActionHandler(mock_request_handler)
        
        facade = IOTFacade(
            request_handler=mock_request_handler,
            action_handler=mock_action_handler
        )
        facade._devices["test_device"] = mock_device
        
        # Test power action
        result = facade.perform_device_action("test_device", "power", state="on")
        assert result is True
        mock_request_handler.post.assert_called_once_with(
            "http://127.0.0.1:8001/power/on", timeout=5
        )