import logging.config
import pprint
from typing import Sequence
from pathlib import Path
import asyncio

from .config import Config


def get_parser():
    """Get the argument parser for the CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="Run configuration file")
    parser.add_argument(
        "config_file",
        type=Path,
        help="Path to the configuration file in .toml format",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = get_parser()
    args = vars(parser.parse_args(argv))

    return dispatch(**args)


def dispatch(config_file: Path) -> int:
    conf = Config.parse_toml(config_file)

    logging.config.dictConfig(conf.log.model_dump())
    logger = logging.getLogger(__name__)
    # conf.dump_toml(Path("config.toml"))

    logger.info("Running EOPF-DDGGS data processing pipeline")
    logger.info("Configuration:\n" + pprint.pformat(conf.model_dump(), indent=2))

    ops = conf.operations

    if ops.download_data:
        from .download import main as download_main

        logger.info("Downloading data from blob storage")
        asyncio.run(download_main(conf.download_data))

    if ops.convert_to_zarr:
        logger.info("Converting data to Zarr format")
        # TODO: Implement Zarr conversion

    return 0
