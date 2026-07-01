import json

from app.domain import Machine
from app.models import MqttConfig


class MqttPublisher:
    def __init__(self, mqtt_config: MqttConfig):
        self.config = mqtt_config

    async def publish_machine_state(self, machine: Machine) -> None:
        topic = f"{self.config.topic_prefix}/{machine.id}/state"

        payload = {
            "machine_id": machine.id,
            "state": machine.current_state,
            "connected": machine.connected,
            "last_update": machine.last_update.isoformat()
            if machine.last_update
            else None,
        }

        print(f"[MQTT] Publishing to {topic}: {json.dumps(payload)}")
