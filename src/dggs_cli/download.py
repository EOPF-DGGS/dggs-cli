from pathlib import Path
import logging
import obstore as obs

from tqdm import tqdm


from .config import DownloadDataSettings

logger = logging.getLogger(__name__)


async def download_file(store: obs.store.S3Store, path: str, output_folder: Path):
    """Download a file from S3 to a local folder.

    Parameters
    ----------
    store : obs.store.S3Store
        The S3 store to download from.
    path : str
        The path to the file in the S3 store.
    output_folder : Path
        The local folder to download the file to.
    """
    resp = await obs.get_async(store, path)
    file_size = resp.meta["size"]

    local_path = output_folder / path
    local_directory = local_path.parent
    local_directory.mkdir(parents=True, exist_ok=True)
    logger.info(f"Downloading {path} to {output_folder} ({file_size / 1e6:.2f} MB)")

    with open(local_path, "wb") as f:
        with tqdm(total=file_size) as pbar:
            async for bytes_chunk in resp:
                # Do something with buffer
                pbar.update(len(bytes_chunk))
                f.write(bytes_chunk)


async def main(settings: DownloadDataSettings):
    logger.info(f"Opening S3 store for bucket {settings.bucket_name}")
    store = obs.store.S3Store(
        bucket=settings.bucket_name,
        endpoint=settings.endpoint,
        access_key_id=settings.minio_settings.ACCESS_KEY_ID.get_secret_value(),
        secret_access_key=settings.minio_settings.SECRET_ACCESS_KEY.get_secret_value(),
        virtual_hosted_style_request=False,
        client_options={"allow_http": True},
    )

    output_folder = settings.output_folder / settings.bucket_name
    output_folder.mkdir(parents=True, exist_ok=True)
    logger.info(f"Downloading to {output_folder}")

    for obj in settings.objects:
        logger.info(f"Processing path {obj}")

        # Check if the path is a folder

        if obj.is_dir:
            files_in_folder = store.list_async(prefix=obj.path)
            # And if there are folders we download all the files in the folder
            async for file in files_in_folder:
                await download_file(store, file["path"], output_folder)
        else:
            # Assume we have a single file to download
            await download_file(store, obj.path, output_folder)
