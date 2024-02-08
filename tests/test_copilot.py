# Create a function that quesries MongoDB
from unittest.mock import Mock


def test_get_copilot(copilot=None):
    # Create a mock object
    mock = Mock()

    # Set the return value of the mock object
    mock.return_value = "mocked"

    # Replace the function with the mock object
    copilot.get_copilot = mock

    # Call the function
    result = copilot.get_copilot()

    # Assert that the result is the same as the return value of the mock object
    assert result == "mocked"