from pydantic import BaseModel, Field


class MqttConfig(BaseModel):
    host: str = "localhost"
    port: int = 1883
    topic_prefix: str = "machines"
    qos: int = 1
    retain: bool = False


class GatewayConfig(BaseModel):
    poll_interval_seconds: int = 5
    mqtt: MqttConfig


class OpcUaNodes(BaseModel):
    current_state: str


class OpcUaSecurityConfig(BaseModel):
    enabled: bool = False
    policy: str | None = None
    mode: str | None = None
    certificate_path: str | None = None
    private_key_path: str | None = None


class OpcUaConfig(BaseModel):
    endpoint: str
    nodes: OpcUaNodes
    security: OpcUaSecurityConfig = Field(default_factory=OpcUaSecurityConfig)


class MachineConfig(BaseModel):
    id: str
    name: str
    type: str
    enabled: bool = True
    opcua: OpcUaConfig


class AppConfig(BaseModel):
    gateway: GatewayConfig
    machines: list[MachineConfig] = Field(default_factory=list)
