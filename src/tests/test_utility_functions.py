import pytest
from src.files.utility_functions import keyvault_connection_strings
from unittest.mock import patch, MagicMock

"""
Note: Ensure to set python path with the following command:
$env:PYTHONPATH = "$PWD"
"""

# Test keyvault_connection_strings function:
def test_data_types_accepted():
    type_list = [1, 1.0, True, None, [], {}, set(), bytes(), bytearray()]
    
    for item in type_list:
        with pytest.raises(TypeError) as excinfo:
            keyvault_connection_strings(item)
        assert str(excinfo.value) == f'Expecting strings.  Got: keyvault_name:\
                        {type(item)}.'
        

def test_keyvault_connection_strings():
    # Define the keyvault name
    keyvault_name = "test-keyvault"

    # Create a dictionary of mock connection strings:
    mock_strings = {'metadata': 'metadata_string',
                    'totesys': 'totesys_string'}
    
    # Create mock for secret client:
    mock_client = MagicMock()

    # Create two separate mock objects for secrets:
    mock_secret_metadata = MagicMock()
    mock_secret_metadata.value = mock_strings['metadata']
    mock_secret_totesys = MagicMock()
    mock_secret_totesys.value = mock_strings['totesys']

    # Patch the SecretClient. Logic for totesys or metadata:
    """
    This configures the get_secret method on the mock client to return different
    values based on thhe argument. 
    If called with 'metadataConnectionString' it returns the metadata mock. 
    If called with anythign else, it returns the totesys mock.
    """
    mock_client.get_secret.side_effect = lambda secret_name: \
    (mock_secret_metadata if secret_name == 'metadataConnectionString' else
     mock_secret_totesys)
    
    
    """
    Patch decorators are used to replace the actual secret clients;
    SecretClient (from azure.keyvault.secrets) and DefaultAzureCrednetial
    (from azure.identity) with the mock client.

    Note that you need to patch the modules where the function is used.
    """
    # Patch the SecretClient class and DefaultAzureCredential:
    with patch('src.files.utility_functions.SecretClient',
            return_value=mock_client), \
        patch('src.files.utility_functions.DefaultAzureCredential'):
        # Call the function with the mock keyvault name:
        result = keyvault_connection_strings(keyvault_name)

        # Type of result should be dictionary:
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"

        
        # Check the result contains the expected keys:
        assert set(result.keys()) == set(mock_strings.keys()), \
            "Missing or extra keys in result"
        for key in mock_strings:
            assert result[key] == mock_strings[key], \
                f"Value mismatch for key '{key}'"


        # Assert that the mock client was called at least once:
        mock_client.get_secret.assert_any_call("metadataConnectionString")
        mock_client.get_secret.assert_any_call("totesysConnectionString")
