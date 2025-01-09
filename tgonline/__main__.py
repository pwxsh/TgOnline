import asyncio
import logging

from pyrogram.client import Client

from tgonline import TgStatusUpdater
from tgonline.config import Config, load_config

logging.basicConfig(level=logging.INFO)


def create_client(config: Config) -> Client:
	client_args = Client.__init__.__annotations__
	config_args = config.__dict__

	for config_arg in config_args.copy():
		if not config_arg in client_args:
			config_args.pop(config_arg)

	return Client(system_version="4.16.30-vxArchLinux", **config_args)


config = load_config()
client = create_client(config)

async def main() -> None:
	await client.start()
	await TgStatusUpdater(client).start(config.is_offline, update_delay=config.update_delay)
	await client.stop()


if __name__ == "__main__":
	asyncio.run(main())
