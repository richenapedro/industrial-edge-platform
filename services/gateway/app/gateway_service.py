from app.clients.mqtt_publisher import MqttPublisher
from app.clients.opcua_client import OpcUaClient
from app.domain import Machine
from app.models import GatewayConfig, MachineConfig
from app.utils.logger import setup_logger
from app.mappers.opcua_runtime_mapper import OpcUaRuntimeMapper

import asyncio

logger = setup_logger(__name__)


class GatewayService:
    def __init__(
        self,
        machine_config: MachineConfig,
        gateway_config: GatewayConfig,
    ):
        self.machine = Machine(machine_config)
        self.opcua_client = OpcUaClient(machine_config)
        self.mqtt_publisher = MqttPublisher(gateway_config.mqtt)
        self.runtime_mapper = OpcUaRuntimeMapper()

    async def run_once(self) -> None:
        logger.info("Connecting OPC UA client for machine %s", self.machine.id)

        await self.opcua_client.connect()

        try:
            self.machine.runtime.connection.mark_connected()
            logger.info("Machine %s marked as connected", self.machine.id)

            values = await self.opcua_client.read_all_configured_nodes()
            logger.info("Read values from machine %s: %s", self.machine.id, values)

            self.runtime_mapper.update(self.machine.runtime, values)

            logger.info(
                "Machine %s state updated to %s",
                self.machine.id,
                self.machine.runtime.state.current,
            )

            await self.mqtt_publisher.publish_machine_state(self.machine)

        finally:
            logger.info("Disconnecting OPC UA client for machine %s", self.machine.id)
            await self.opcua_client.disconnect()

    async def run_forever(self, poll_interval_seconds: int) -> None:
        logger.info(
            "Starting continuous gateway loop for machine %s with interval %s second(s)",
            self.machine.id,
            poll_interval_seconds,
        )

        while True:
            try:
                await self.run_once()

            except Exception:
                logger.exception(
                    "Gateway loop iteration failed for machine %s",
                    self.machine.id,
                )

            await asyncio.sleep(poll_interval_seconds)
