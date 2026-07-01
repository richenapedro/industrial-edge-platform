from datetime import datetime, timezone

from app.models import MachineConfig


class Machine:
    def __init__(self, config: MachineConfig) -> None:
        self.config = config
        self.connected: bool = False
        self.current_state: str | None = None
        self.last_update: datetime | None = None

    @property
    def id(self) -> str:
        return self.config.id

    @property
    def type(self) -> str:
        return self.config.type

    @property
    def name(self) -> str:
        return self.config.name

    def mark_connected(self) -> None:
        self.connected = True
        self.last_update = datetime.now(timezone.utc)

    def mark_disconnected(self) -> None:
        self.connected = False
        self.last_update = datetime.now(timezone.utc)

    def update_state(self, state: str) -> None:
        self.current_state = state
        self.last_update = datetime.now(timezone.utc)
