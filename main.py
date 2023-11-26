from config.config import Config
from src.adapters.external_services.service_bus import ServiceBus


def main():
    service_bus = ServiceBus(Config.SERVICE_BUS_CONNECTION_STRING, Config.SERVICE_BUS_QUEUE_NAME)
    while True:
        service_bus.get_from_queue()


if __name__ == "__main__":
    main()
