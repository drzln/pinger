from pydantic import BaseModel
import yaml
import os


class AppConfig(BaseModel):
    name: str


class Config:
    _yaml = None

    @classmethod
    def yaml(cls):
        cls.being_tested(cls.local_cli())
        filename = ""
        if cls.being_tested():
            filename = f"envs/{cls.env()}/config.yml"
        else:
            filename = f"/var/task/envs/{cls.env()}/config.yml"

        print("USING FILENAME")
        print(filename)
        if cls._yaml is None:
            with open(filename) as ymlfile:
                cls._yaml = yaml.safe_load(ymlfile)
        return cls._yaml

    _env = None

    @classmethod
    def env(cls, setting=None):
        if cls._env is None:
            if setting is None:
                env = os.getenv("ENV")
            else:
                env = setting
            cls._env = env
            if cls._env is None:
                raise Exception("no ENV variable set!")
        return cls._env

    _being_tested = None

    @classmethod
    def being_tested(cls, setting: bool = False) -> bool:
        if cls._being_tested is None:
            cls._being_tested = setting
        return cls._being_tested

    @classmethod
    def local_cli(cls):
        return os.getenv("LOCAL_CLI") == "true"

    _config = None

    @classmethod
    def config(cls):
        if cls._config is None:
            cls._config = AppConfig(**cls.yaml())
        return cls._config
