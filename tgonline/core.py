from abc import abstractmethod
from typing import Protocol

from pyrogram.client import Client


class ClientStatusUpdater(Protocol):
	@property
	@abstractmethod
	def client(self) -> Client:
		raise NotImplementedError

	@abstractmethod
	async def update(self, offline: bool) -> bool:
		raise NotImplementedError
