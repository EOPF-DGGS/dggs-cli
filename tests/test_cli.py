from textwrap import dedent
import logging
from unittest import mock
from dggs_cli import cli


def test_cli_dry_run(tmp_path, caplog):
    # Just create a temporary config file
    caplog.set_level(logging.INFO)
    tmp_path = tmp_path / "config.toml"
    tmp_path.touch()
    ret = cli.main([str(tmp_path)])
    assert ret == 0

    assert caplog.records[0].message == "Running EOPF-DDGGS data processing pipeline"


def test_cli_download_file(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        dedent(
            f"""
    [operations]
    download_data = true

    [download_data]
    bucket_name = "some_bucket"
    endpoint = "https://some_endpoint.com"
    objects = [{{path = "some_file", is_dir = false}}]
    output_folder = "{tmp_path}/data"

    """
        )
    )

    store_mock = mock.MagicMock()
    obs_get_async_mock = mock.AsyncMock()
    resp_mock = mock.AsyncMock()
    obs_get_async_mock.return_value = resp_mock
    resp_mock.meta = {"size": 123456}
    with (
        mock.patch("dggs_cli.download.obs.store.S3Store", store_mock),
        mock.patch("dggs_cli.download.obs.get_async", obs_get_async_mock),
    ):
        ret = cli.main([str(config_path)])
    assert ret == 0

    # Check that store has been called
    store_mock.assert_called_once()

    # check that get_async has been awaited
    obs_get_async_mock.assert_awaited()

    # Check that we called get_async with the correct parameters
    obs_get_async_mock.assert_called_with(store_mock.return_value, "some_file")

    # Check that we have iterated over the response
    resp_mock.__aiter__.assert_called()


def test_cli_download_folder(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        dedent(
            f"""
    [operations]
    download_data = true

    [download_data]
    bucket_name = "some_bucket"
    endpoint = "https://some_endpoint.com"
    objects = [{{path = "some_folder", is_dir = true}}]
    output_folder = "{tmp_path}/data"

    """
        )
    )

    store_mock = mock.MagicMock()
    # Make sure list_async returns a list of files
    store_mock.return_value.list_async.return_value.__aiter__.return_value = [{"path": "some_file"}]
    obs_get_async_mock = mock.AsyncMock()
    resp_mock = mock.AsyncMock()
    obs_get_async_mock.return_value = resp_mock
    resp_mock.meta = {"size": 123456}
    with (
        mock.patch("dggs_cli.download.obs.store.S3Store", store_mock),
        mock.patch("dggs_cli.download.obs.get_async", obs_get_async_mock),
    ):
        ret = cli.main([str(config_path)])
    assert ret == 0

    # Check that store has been called
    store_mock.assert_called_once()

    # Check that list_async has been called
    store_mock.return_value.list_async.assert_called_once_with(prefix="some_folder")

    # check that get_async has been awaited
    obs_get_async_mock.assert_awaited()

    # Check that we called get_async with the correct parameters
    obs_get_async_mock.assert_called_with(store_mock.return_value, "some_file")

    # Check that we have iterated over the response
    resp_mock.__aiter__.assert_called()
