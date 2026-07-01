import asyncio

from app.config import load_config
from app.gateway_service import GatewayService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def main() -> None:
    config = load_config("../../config/machines.yml")

    enabled_machines = [machine for machine in config.machines if machine.enabled]

    logger.info("Starting gateway with %s enabled machine(s)", len(enabled_machines))

    services = [
        GatewayService(machine_config, config.gateway)
        for machine_config in enabled_machines
    ]

    await asyncio.gather(
        *[
            service.run_forever(config.gateway.poll_interval_seconds)
            for service in services
        ]
    )


if __name__ == "__main__":
    asyncio.run(main())
