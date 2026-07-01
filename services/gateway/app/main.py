from app.config import load_config


def main() -> None:
    config = load_config("../../config/machines.yml")

    print(f"MQTT broker: {config.gateway.mqtt.host}:{config.gateway.mqtt.port}")

    for machine in config.machines:
        print(f"{machine.id} | {machine.type} | enabled={machine.enabled}")


if __name__ == "__main__":
    main()
