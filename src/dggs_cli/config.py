import logging
from pathlib import Path
from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings_logging import LoggingSettings

logger = logging.getLogger(__name__)


class Operations(BaseSettings):
    download_data: bool = Field(False, description="Download data from blob storage")
    convert_to_zarr: bool = Field(False, description="Convert downloaded data to Zarr format")


class MINIOSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MINIO_")
    ACCESS_KEY_ID: SecretStr = SecretStr("xxx")
    SECRET_ACCESS_KEY: SecretStr = SecretStr("xxx")


class Object(BaseSettings):
    path: str = Field(..., description="Path to the object in the bucket")
    is_dir: bool = Field(..., description="Whether the object is a directory of file")


class DownloadDataSettings(BaseSettings):
    bucket_name: str = Field("bucket_name")
    endpoint: str = Field(
        "https://pangeo-eosc-minioapi.vm.fedcloud.eu",
        description="The endpoint for communicating with AWS S3.",
    )
    minio_settings: Annotated[
        MINIOSettings, Field(default_factory=MINIOSettings, description="MinIO settings")
    ]
    objects: list[Object] = Field(default_factory=list, description="List of objects to download")
    output_folder: Path = Field(default=Path("data"), description="Output directory for downloaded data")


class Config(BaseSettings):
    log: LoggingSettings = Field(default_factory=LoggingSettings, description="Logging settings")
    operations: Annotated[Operations, Field(default_factory=Operations, description="Operations to perform")]
    download_data: Annotated[
        DownloadDataSettings,
        Field(default_factory=DownloadDataSettings, description="Download data settings"),
    ]

    def dump_toml(self, path: Path) -> None:
        """
        Dump the configuration to a TOML file.

        Parameters
        ----------
        path : Path
            The path to the TOML file where the configuration will be saved.
        """
        import json

        import toml

        Path(path).write_text(toml.dumps(json.loads(self.json())))
        logger.info(f"Configuration dumped to {path}")

    @classmethod
    def parse_toml(cls, path: Path) -> "Config":
        """
        Parse a TOML file into a Config object.

        Parameters
        ----------
        path : Path
            The path to the TOML file to parse.

        Returns
        -------
        Config
            The parsed configuration object.
        """

        import toml

        config_data = toml.loads(path.read_text())
        return cls.model_validate(config_data)
