import asyncio

from app.clients.opcua_client import OpcUaClient
from app.config import load_config


async def main() -> None:
    config = load_config("../../config/machines.yml")

    enabled_machines = [machine for machine in config.machines if machine.enabled]

    for machine_config in enabled_machines:
        opcua_client = OpcUaClient(machine_config)

        try:
            await opcua_client.connect()
            print(f"Connected to {machine_config.id}")

            values = await opcua_client.read_all_configured_nodes()
            print(values)

        finally:
            await opcua_client.disconnect()
            print(f"Disconnected from {machine_config.id}")


if __name__ == "__main__":
    asyncio.run(main())
