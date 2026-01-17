import pytest
from devices.base_device import DeviceFactory
from devices.smart_speaker import SmartSpeakerDevice
from devices.smart_light import SmartLightDevice
from devices.smart_curtains import SmartCurtainsDevice

class TestDeviceFactory:
    
    def test_create_smart_speaker(self):
        device = DeviceFactory.create_device("smart_speaker", "speaker_001")
        assert isinstance(device, SmartSpeakerDevice)
        assert device.port == 8001
    
    def test_create_smart_light(self):
        device = DeviceFactory.create_device("smart_light", "light_001")
        assert isinstance(device, SmartLightDevice)
        assert device.port == 8002
    
    def test_create_smart_curtains(self):
        device = DeviceFactory.create_device("smart_curtains", "curtains_001")
        assert isinstance(device, SmartCurtainsDevice)
        assert device.port == 8003
    
    def test_create_with_custom_port(self):
        device = DeviceFactory.create_device("smart_speaker", "speaker_002", port=9000)
        assert device.port == 9000
    
    def test_unknown_device_type(self):
        with pytest.raises(ValueError, match="Unknown device type"):
            DeviceFactory.create_device("unknown_device", "test_001")