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