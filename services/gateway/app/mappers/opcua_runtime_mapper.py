from app.domain import MachineRuntime
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class OpcUaRuntimeMapper:
    def update(
        self,
        runtime: MachineRuntime,
        values: dict[str, object],
    ) -> None:
        if "current_state" in values:
            runtime.state.update(str(values["current_state"]))

        if "current_program" in values:
            runtime.program.update(str(values["current_program"]))

        if "current_tool" in values:
            runtime.tool.update(str(values["current_tool"]))

        if "spindle_speed" in values:
            spindle_speed = values["spindle_speed"]

            if isinstance(spindle_speed, int | float | str):
                runtime.spindle.update_speed(float(spindle_speed))
            else:
                logger.warning("Invalid spindle_speed value: %s", spindle_speed)

        if "active_alarm" in values:
            alarm = values["active_alarm"]
            runtime.alarm.update_active_alarm(str(alarm) if alarm is not None else None)
