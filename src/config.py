import os 
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
	ENV_STATE: Optional[str] = 'dev' # default value

	model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '..','.env'),
        extra='ignore')

class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    ALGORITHM: Optional[str] = None
    

class DevConfig(GlobalConfig):
	model_config = SettingsConfigDict(env_prefix='DEV_')


class ProdConfig(GlobalConfig):
	model_config = SettingsConfigDict(env_prefix='PROD_')


class TestConfig(GlobalConfig):
	DATABASE_URL: str = 'sqlite:///test.db'

	model_config = SettingsConfigDict(env_prefix='TEST_')


@lru_cache()
def get_config(env_state: str):
	config = {'dev': DevConfig, 'prod': ProdConfig, 'test': TestConfig}
	return config[env_state]()


config = get_config(BaseConfig().ENV_STATE)

