from pydantic import BaseModel, Field


class MqttConfig(BaseModel):
    host: str = "localhost"
    port: int = 1883
    topic_prefix: str = "machines"
    qos: int = 1
    retain: bool = False


class GatewayConfig(BaseModel):
    mqtt: MqttConfig


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
    gateway: GatewayConfig
    machines: list[MachineConfig] = Field(default_factory=list)
