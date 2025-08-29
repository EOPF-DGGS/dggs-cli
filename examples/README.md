# Example of downloading data from MinIO


## Setting up the environment variables for accessing MinIO

First you need to set up your environment variables for MinIO access.

```bash
export MINIO_ACCESS_KEY_ID=your_access_key
export MINIO_SECRET_ACCESS_KEY=your_secret_key
```


Replace `your_access_key` and `your_secret_key` with your actual MinIO credentials.

### Using a .env file
You can also create a `.env` file with your MinIO credentials

```bash
# .env
MINIO_ACCESS_KEY_ID=your_access_key
MINIO_SECRET_ACCESS_KEY=your_secret_key
```

and export the environment variables so that they are available to your application. You can do this by running the following command (unix) in your terminal:

```bash
set -o allexport && source .env && set +o allexport
```

## Downloading data from MinIO
Create a `config.toml` file with the following content:
```toml
[operations]
download_data = true

[download_data]
bucket_name = "okihle-s2l1b"
endpoint = "https://pangeo-eosc-minioapi.vm.fedcloud.eu"
objects = [
    { path = "Sentinel-2/MSI/MSI_L1B_GR/2025/07/24/S2A_OPER_MSI_L1B_GR_2APS_20250724T011636_S20250724T000406_D03_N05.11.tar", is_dir = false },
]
output_folder = "data"
```

Under `[operations]`, set `download_data` to `true` to enable the download operation. (here we will add more operations in the future to enable e.g conversion from one format to another).

Under `[download_data]`, specify the `bucket_name`, `endpoint`, a list of `objects` to download (with their paths and whether they are directories or files), and the `output_folder` where the data should be saved.
