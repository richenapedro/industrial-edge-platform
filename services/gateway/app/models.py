from pydantic import BaseModel, Field


class OpcUaNodes(BaseModel):
    current_state: str


class OpcUaConfig(BaseModel):
    endpoint: str
    nodes: OpcUaNodes


class MachineConfig(BaseModel):
    id: str
    name: str
    type: str
    enabled: bool = True
    opcua: OpcUaConfig


class AppConfig(BaseModel):
    machines: list[MachineConfig] = Field(default_factory=list)
