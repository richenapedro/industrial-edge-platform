from app.config import load_config
from app.domain import Machine


def main() -> None:
    config = load_config("../../config/machines.yml")

    machines = [Machine(machine_config) for machine_config in config.machines]

    for machine in machines:
        print(f"{machine.id} | {machine.type} | connected={machine.connected}")

        machine.update_state("Automatic")

        print(
            f"{machine.id} | state={machine.current_state} | "
            f"last_update={machine.last_update}"
        )


if __name__ == "__main__":
    main()
