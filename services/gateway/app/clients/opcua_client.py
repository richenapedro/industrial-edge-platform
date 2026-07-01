from asyncua import Client

from app.models import MachineConfig
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class OpcUaClient:
    def __init__(self, machine_config: MachineConfig):
        self.machine_config = machine_config
        self.endpoint = machine_config.opcua.endpoint
        self.nodes = machine_config.opcua.nodes
        self._client: Client | None = None
        self._connected = False

    async def connect(self) -> None:
        logger.info("Creating OPC UA client for endpoint %s", self.endpoint)

        self._client = Client(url=self.endpoint)

        security = self.machine_config.opcua.security

        if security.enabled:
            logger.info(
                "Applying OPC UA security: policy=%s mode=%s",
                security.policy,
                security.mode,
            )

            if not security.policy or not security.mode:
                raise ValueError(
                    "OPC UA security is enabled, but policy or mode is missing."
                )

            if not security.certificate_path or not security.private_key_path:
                raise ValueError(
                    "OPC UA security is enabled, but certificate or private key path is missing."
                )

            await self._client.set_security_string(
                f"{security.policy},{security.mode},{security.certificate_path},{security.private_key_path}"
            )
        else:
            logger.warning("OPC UA security is disabled for endpoint %s", self.endpoint)

        try:
            logger.info("Connecting to OPC UA endpoint %s", self.endpoint)
            await self._client.connect()
            self._connected = True
            logger.info("Connected to OPC UA endpoint %s", self.endpoint)

        except Exception:
            self._connected = False
            self._client = None
            logger.error("Failed to connect to OPC UA endpoint %s", self.endpoint)
            raise

    async def disconnect(self) -> None:
        if self._client is not None and self._connected:
            await self._client.disconnect()

        self._connected = False
        self._client = None

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def read_node(self, node_name: str) -> object:
        if not self._connected or self._client is None:
            raise RuntimeError("OPC UA client is not connected.")

        node_id = getattr(self.nodes, node_name, None)

        if node_id is None:
            raise KeyError(f"Node '{node_name}' not found in machine configuration.")

        node = self._client.get_node(node_id)

        return await node.read_value()

    async def read_all_configured_nodes(self) -> dict[str, object]:
        values: dict[str, object] = {}

        for node_name in self.nodes.model_fields:
            values[node_name] = await self.read_node(node_name)

        return values
