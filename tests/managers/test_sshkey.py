import pytest
from unittest.mock import MagicMock, patch
from digitalocean_manager.managers.sshkey import SSHKeyManager
import json


# Define mock data
mock_ssh_key = {
    'id': 123,
    'name': 'test_key',
    'fingerprint': 'aa:bb:cc:dd:ee:ff'
}

mock_resp = {
    'ssh_keys': [mock_ssh_key]
}


# Test for the list method
@patch('digitalocean_manager.managers.sshkey.DigitalOceanClient')
@patch('digitalocean_manager.managers.sshkey.Config')
def test_list(mock_config, mock_client):
    # Set up mocks
    mock_instance = mock_client.return_value
    mock_instance.ssh_keys.list.return_value = mock_resp
    mock_config_instance = mock_config.return_value
    mock_config_instance.json_indent = 4
    
    # Instantiate SSHKeyManager and call the list method
    manager = SSHKeyManager()
    with patch('builtins.print') as mocked_print:
        manager.list()
    
        # Debugging: Check if the method was called
        print(mock_instance.ssh_keys.list.call_args)
        
        # Verify that the list method makes the expected call
        mock_instance.ssh_keys.list.assert_called_once()


# Test for the info method
@patch('digitalocean_manager.managers.sshkey.DigitalOceanClient')
@patch('digitalocean_manager.managers.sshkey.Config')
def test_info(mock_config, mock_client):
    # Set up mocks
    mock_instance = mock_client.return_value
    mock_instance.ssh_keys.get.return_value = {'ssh_key': mock_ssh_key}
    mock_config_instance = mock_config.return_value
    mock_config_instance.json_indent = 4

    # Instantiate SSHKeyManager and call the info method
    manager = SSHKeyManager()
    with patch('builtins.print') as mocked_print:
        manager.info(123)

        # Verify that the info method calls the client API correctly
        mock_instance.ssh_keys.get.assert_called_once_with(123)

        # Check that the info method formats the response as expected
        mocked_print.assert_called_with(
            json.dumps(mock_ssh_key, indent=mock_config_instance.json_indent)
        )


# Test for handling API errors in list method
@patch('digitalocean_manager.managers.sshkey.DigitalOceanClient')
@patch('digitalocean_manager.managers.sshkey.Config')
def test_list_api_error(mock_config, mock_client):
    # Set up mock to simulate an API error
    mock_instance = mock_client.return_value
    mock_instance.ssh_keys.list.return_value = {'error': 'Something went wrong'}
    mock_config_instance = mock_config.return_value
    mock_config_instance.json_indent = 4

    # Instantiate SSHKeyManager and call the list method
    manager = SSHKeyManager()
    with patch('builtins.print') as mocked_print:
        manager.list()

        # Verify that the error handling is triggered
        mock_instance.raise_api_error.assert_called_once_with({'error': 'Something went wrong'})
        mocked_print.assert_called_with("Error listing SSH keys: Something went wrong")


# Test for handling API errors in info method
@patch('digitalocean_manager.managers.sshkey.DigitalOceanClient')
@patch('digitalocean_manager.managers.sshkey.Config')
def test_info_api_error(mock_config, mock_client):
    # Set up mock to simulate an API error
    mock_instance = mock_client.return_value
    mock_instance.ssh_keys.get.return_value = {'error': 'SSH key not found'}
    mock_config_instance = mock_config.return_value
    mock_config_instance.json_indent = 4

    # Instantiate SSHKeyManager and call the info method
    manager = SSHKeyManager()
    with patch('builtins.print') as mocked_print:
        manager.info(123)

        # Verify that the error handling is triggered
        mock_instance.raise_api_error.assert_called_once_with({'error': 'SSH key not found'})
        mocked_print.assert_called_with("Error getting SSH key info: SSH key not found")