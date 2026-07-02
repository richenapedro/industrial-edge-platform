from app.clients.mqtt_publisher import MqttPublisher
from app.clients.opcua_client import OpcUaClient
from app.domain import Machine
from app.models import GatewayConfig, MachineConfig
from app.utils.logger import setup_logger

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

    async def run_once(self) -> None:
        logger.info("Connecting OPC UA client for machine %s", self.machine.id)

        await self.opcua_client.connect()

        try:
            self.machine.runtime.connection.mark_connected()
            logger.info("Machine %s marked as connected", self.machine.id)

            values = await self.opcua_client.read_all_configured_nodes()
            logger.info("Read values from machine %s: %s", self.machine.id, values)

            if "current_state" in values:
                self._update_machine_runtime(values)

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

    def _update_machine_runtime(self, values: dict[str, object]) -> None:
        if "current_state" in values:
            self.machine.runtime.state.update(str(values["current_state"]))

        if "current_program" in values:
            self.machine.runtime.program.update(str(values["current_program"]))

        if "current_tool" in values:
            self.machine.runtime.tool.update(str(values["current_tool"]))

        if "spindle_speed" in values:
            spindle_speed = values["spindle_speed"]

            if isinstance(spindle_speed, int | float | str):
                self.machine.runtime.spindle.update_speed(float(spindle_speed))
            else:
                logger.warning(
                    "Invalid spindle_speed value for machine %s: %s",
                    self.machine.id,
                    spindle_speed,
                )

        if "active_alarm" in values:
            alarm = values["active_alarm"]
            self.machine.runtime.alarm.update_active_alarm(
                str(alarm) if alarm is not None else None
            )
