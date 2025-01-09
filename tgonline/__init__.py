import asyncio
import logging
from typing import Union

from pyrogram.client import Client
from pyrogram.errors import ConnectionNotInited

from tgonline.core import ClientStatusUpdater

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DEFAULT_UPDATE_DELAY = 15


class TgStatusUpdater(ClientStatusUpdater):
	def __init__(self, client: Client):
		if not client.is_connected:
			raise ConnectionNotInited("Telegram client should be connected before StatusUpdater initialize")
		self.__client = client
		self.__is_running = False

	@property
	def client(self) -> Client:
		return self.__client

	@property
	def is_running(self) -> bool:
		return self.__is_running

	async def update(self, offline: bool) -> bool:
		logger.debug(f"Updating status to {'offline' if offline else 'online'}...")
		return await self.__client.update_status(offline=offline)

	async def start(
		self,
		offline: bool,
		update_delay: Union[int, float] = DEFAULT_UPDATE_DELAY
	) -> None:
		if self.is_running:
			raise RuntimeError("Status updater loop is already running")

		if update_delay < 1:
			raise ValueError("Update delay should be higher than 1 second")

		self.__is_running = True

		logger.info(f"Starting StatusUpdater with status: {'offline' if offline else 'online'}...")
		while self.is_running:
			await self.update(offline)
			await asyncio.sleep(update_delay)

	async def stop(self) -> None:
		logger.info(f"Closing StatusUpdater...")
		if not self.is_running:
			raise RuntimeError("Status updater loop is not running")
		self.__is_running = False

	async def __aenter__(
		self,
		offline: bool,
		update_delay: Union[int, float] = DEFAULT_UPDATE_DELAY
	):
		await self.start(offline, update_delay)

	async def __aexit__(self, exc_type, exc, tb) -> None:
		await self.stop()
