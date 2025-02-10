import pytest
from unittest.mock import patch, MagicMock
from digitalocean_manager.managers.sshkey import SSHKeyManager


# Define the fake API response
api_response = {
    "ssh_keys": [
        {"id": 123, "name": "TestKey1", "fingerprint": "fingerprint1"},
        {"id": 456, "name": "TestKey2", "fingerprint": "fingerprint2"},
    ]
}

# Mock Config and DigitalOceanClient properly
@patch("digitalocean_manager.config.Config._read_config_file", autospec=True, return_value={})
@patch("digitalocean_manager.managers.sshkey.DigitalOceanClient.get_client", autospec=True)
def test_list(mock_get_client, mock_config, capsys):
    """Test the list method of SSHKeyManager."""

    # Mock DigitalOceanClient instance's list() method to return the fake response
    mock_client_instance = MagicMock()
    mock_client_instance.ssh_keys.list.return_value = api_response
    mock_client_instance.raise_api_error.side_effect = Exception("API Error: Something went wrong")

    # Mock get_client() to return our mocked client instance
    mock_get_client.return_value = mock_client_instance

    # Instantiate SSHKeyManager (it will use the mocked Config and Client)
    manager = SSHKeyManager()

    # Call the list method
    manager.list()

    # Capture the printed output using capsys
    captured = capsys.readouterr()

    # Assertions to check if the output contains the expected values
    assert "TestKey1" in captured.out
    assert "fingerprint1" in captured.out
    assert "TestKey2" in captured.out
    assert "fingerprint2" in captured.out


@patch("digitalocean_manager.config.Config._read_config_file", autospec=True, return_value={})
@patch("digitalocean_manager.managers.sshkey.DigitalOceanClient.get_client", autospec=True)
def test_list_empty_response(mock_get_client, mock_config, capsys):
    """Test the list method of SSHKeyManager with an empty API response."""

    # Mock DigitalOceanClient instance's list() method to return an empty response
    mock_client_instance = MagicMock()
    mock_client_instance.ssh_keys.list.return_value = {'ssh_keys': []}
    mock_client_instance.raise_api_error.side_effect = Exception("API Error: Something went wrong")

    # Mock get_client() to return our mocked client instance
    mock_get_client.return_value = mock_client_instance

    # Instantiate SSHKeyManager (it will use the mocked Config and Client)
    manager = SSHKeyManager()

    # Call the list method
    manager.list()

    # Capture the printed output using capsys
    captured = capsys.readouterr()

    # Assertions to check that the method didn't print anything (since you don't print for empty responses)
    assert captured.out == ""  # Check that there's no output


@patch("digitalocean_manager.config.Config._read_config_file", autospec=True, return_value={})
@patch("digitalocean_manager.managers.sshkey.DigitalOceanClient.get_client", autospec=True)
def test_list_with_api_error(mock_get_client, mock_config, capsys):
    """Test the raise_api_error method of SSHKeyManager."""

    # Mock the DigitalOceanClient instance's raise_api_error method to raise an exception
    mock_client_instance = MagicMock()
    mock_client_instance.ssh_keys.list.return_value = {}
    mock_client_instance.raise_api_error.side_effect = Exception("API Error: Something went wrong")

    # Mock get_client() to return our mocked client instance
    mock_get_client.return_value = mock_client_instance

    # Instantiate SSHKeyManager (it will use the mocked Config and Client)
    manager = SSHKeyManager()

    # Call the method that triggers the exception
    manager.list()

    # Capture the printed output using capsys
    captured = capsys.readouterr()

    # Assertions to check if the error message was printed correctly
    assert "API Error" in captured.out


@patch("digitalocean_manager.config.Config._read_config_file", autospec=True, return_value={})
@patch("digitalocean_manager.managers.sshkey.DigitalOceanClient.get_client", autospec=True)
def test_list_with_exeption(mock_get_client, mock_config, capsys):
    """Test the list method of SSHKeyManager with exception handling."""

    error_message = "Something went wrong"

    # Mock the DigitalOceanClient instance's raise_api_error method to raise an exception
    mock_client_instance = MagicMock()
    mock_client_instance.ssh_keys.list.side_effect = Exception(error_message)

    # Mock get_client() to return our mocked client instance
    mock_get_client.return_value = mock_client_instance

    # Instantiate SSHKeyManager (it will use the mocked Config and Client)
    manager = SSHKeyManager()

    # Call the method that triggers the exception
    manager.list()

    # Capture the printed output using capsys
    captured = capsys.readouterr()

    # Assertions to check if the error message was printed correctly
    assert error_message in captured.out