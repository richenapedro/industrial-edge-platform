from dataclasses import dataclass
from datetime import datetime, timezone

from app.models import MachineConfig


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class ConnectionRuntime:
    connected: bool = False
    last_update: datetime | None = None

    def mark_connected(self) -> None:
        self.connected = True
        self.last_update = utc_now()

    def mark_disconnected(self) -> None:
        self.connected = False
        self.last_update = utc_now()


@dataclass
class StateRuntime:
    current: str | None = None
    last_update: datetime | None = None

    def update(self, state: str) -> None:
        self.current = state
        self.last_update = utc_now()


@dataclass
class ProgramRuntime:
    current: str | None = None
    previous: str | None = None
    last_update: datetime | None = None

    def update(self, program: str) -> None:
        if program != self.current:
            self.previous = self.current
            self.current = program
            self.last_update = utc_now()


@dataclass
class ToolRuntime:
    current: str | None = None
    previous: str | None = None
    last_update: datetime | None = None

    def update(self, tool: str) -> None:
        if tool != self.current:
            self.previous = self.current
            self.current = tool
            self.last_update = utc_now()


@dataclass
class SpindleRuntime:
    speed: float | None = None
    last_update: datetime | None = None

    def update_speed(self, speed: float) -> None:
        self.speed = speed
        self.last_update = utc_now()


@dataclass
class AlarmRuntime:
    active_alarm: str | None = None
    last_update: datetime | None = None

    def update_active_alarm(self, alarm: str | None) -> None:
        self.active_alarm = alarm
        self.last_update = utc_now()


@dataclass
class MachineRuntime:
    connection: ConnectionRuntime
    state: StateRuntime
    program: ProgramRuntime
    tool: ToolRuntime
    spindle: SpindleRuntime
    alarm: AlarmRuntime

    @classmethod
    def create(cls) -> "MachineRuntime":
        return cls(
            connection=ConnectionRuntime(),
            state=StateRuntime(),
            program=ProgramRuntime(),
            tool=ToolRuntime(),
            spindle=SpindleRuntime(),
            alarm=AlarmRuntime(),
        )


class Machine:
    def __init__(self, config: MachineConfig):
        self.id = config.id
        self.name = config.name
        self.type = config.type
        self.runtime = MachineRuntime.create()
