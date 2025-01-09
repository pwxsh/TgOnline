import os
from dataclasses import dataclass
from typing import Optional, Union

from dotenv import load_dotenv

from tgonline import DEFAULT_UPDATE_DELAY


@dataclass
class Config:
	name: str
	api_id: int
	api_hash: str
	phone_number: str
	password: Optional[str] = None
	is_offline: bool = False
	update_delay: Union[int, float] = DEFAULT_UPDATE_DELAY


def load_config() -> Config:
	load_dotenv()
	update_delay = os.environ["UPDATE_DELAY"]
	return Config(
		name=os.environ["SESSION_NAME"],
		api_id=int(os.environ["API_ID"]),
		api_hash=os.environ["API_HASH"],
		phone_number=os.environ["PHONE_NUMBER"],
		password=os.environ["PASSWORD"],
		is_offline=bool(os.environ["IS_OFFLINE"]),
		update_delay=float(update_delay) if "." in update_delay else int(update_delay)
	)
