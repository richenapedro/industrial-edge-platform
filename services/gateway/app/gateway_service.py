from app.clients.mqtt_publisher import MqttPublisher
from app.clients.opcua_client import OpcUaClient
from app.domain import Machine
from app.models import GatewayConfig, MachineConfig


class GatewayService:
    def __init__(
        self,
        machine_config: MachineConfig,
        gateway_config: GatewayConfig,
    ):
        self.machine = Machine(machine_config)
        self.opcua_client = OpcUaClient(machine_config)
        self.mqtt_publisher = MqttPublisher(gateway_config.mqtt)

    async def run_once(self) -> None:
        await self.opcua_client.connect()

        try:
            self.machine.mark_connected()

            values = await self.opcua_client.read_all_configured_nodes()

            if "current_state" in values:
                self.machine.update_state(str(values["current_state"]))

            await self.mqtt_publisher.publish_machine_state(self.machine)

        finally:
            await self.opcua_client.disconnect()
