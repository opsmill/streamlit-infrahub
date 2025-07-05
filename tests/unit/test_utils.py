"""Unit tests for the utils module."""

from unittest.mock import MagicMock

from infrahub_sdk.schema import AttributeSchemaAPI

from streamlit_infrahub.utils import display_attribute, get_choice


def test_get_choice_matching_value(dropdown_attr_with_choices: AttributeSchemaAPI) -> None:
    """Test get_choice returns the correct choice when a match is found.

    Tests that the function returns the correct choice dictionary when
    a choice with a matching name is found in the attribute's choices.

    Args:
        dropdown_attr_with_choices: Fixture providing an attribute with choices.
    """
    # Arrange
    expected_choice = dropdown_attr_with_choices.choices[0]

    # Act
    result = get_choice(attr=dropdown_attr_with_choices, value="option1")

    # Assert
    assert result == expected_choice
    assert result["name"] == "option1"
    assert result["label"] == "Option 1"


def test_get_choice_no_match(dropdown_attr_with_choices: AttributeSchemaAPI) -> None:
    """Test get_choice returns None when no match is found.

    Tests that the function returns None when no choice with a
    matching name is found in the attribute's choices.

    Args:
        dropdown_attr_with_choices: Fixture providing an attribute with choices.
    """
    # Act
    result = get_choice(attr=dropdown_attr_with_choices, value="option3")

    # Assert
    assert result is None


def test_get_choice_empty_choices(dropdown_attr_empty_choices: AttributeSchemaAPI) -> None:
    """Test get_choice with empty choices list.

    Tests that the function returns None when the attribute has
    no choices in its list.

    Args:
        dropdown_attr_empty_choices: Fixture providing an attribute with no choices.
    """
    # Act
    result = get_choice(attr=dropdown_attr_empty_choices, value="option1")

    # Assert
    assert result is None


def test_get_choice_multiple_matches(dropdown_attr_with_duplicate_choices: AttributeSchemaAPI) -> None:
    """Test get_choice with multiple matching choices.

    Tests that the function returns None when there are multiple
    choices with the same name, which should not happen in practice
    but is handled by the function.

    Args:
        dropdown_attr_with_duplicate_choices: Fixture providing an attribute with duplicate choices.
    """
    # Act
    result = get_choice(attr=dropdown_attr_with_duplicate_choices, value="option1")

    # Assert
    assert result is None


def test_display_attribute_dropdown_with_choice(
    dropdown_attr_with_choices: AttributeSchemaAPI, streamlit_container: MagicMock
) -> None:
    """Test display_attribute with a dropdown attribute that has a matching choice.

    Tests that the function displays a badge with the choice label when the
    attribute is a dropdown and a matching choice is found.

    Args:
        dropdown_attr_with_choices: Fixture providing an attribute with choices.
        streamlit_container: Fixture providing a mock Streamlit container.
    """
    # Act
    result = display_attribute(attr=dropdown_attr_with_choices, value="option1", container=streamlit_container)

    # Assert
    streamlit_container.badge.assert_called_once_with("Option 1", color="primary")
    assert result == "badge_output"


def test_display_attribute_dropdown_no_choice(
    dropdown_attr_with_choices: AttributeSchemaAPI, streamlit_container: MagicMock
) -> None:
    """Test display_attribute with a dropdown attribute that has no matching choice.

    Tests that the function displays the value as markdown when the attribute is
    a dropdown but no matching choice is found.

    Args:
        dropdown_attr_with_choices: Fixture providing an attribute with choices.
        streamlit_container: Fixture providing a mock Streamlit container.
    """
    # Act
    result = display_attribute(attr=dropdown_attr_with_choices, value="option3", container=streamlit_container)

    # Assert
    streamlit_container.markdown.assert_called_once_with(dropdown_attr_with_choices.value)
    assert result == "markdown_output"


def test_display_attribute_non_dropdown(text_attribute: AttributeSchemaAPI, streamlit_container: MagicMock) -> None:
    """Test display_attribute with a non-dropdown attribute.

    Tests that the function displays the value as markdown when the attribute
    is not a dropdown.

    Args:
        text_attribute: Fixture providing a text attribute.
        streamlit_container: Fixture providing a mock Streamlit container.
    """
    # Act
    result = display_attribute(attr=text_attribute, value="any value", container=streamlit_container)

    # Assert
    streamlit_container.markdown.assert_called_once_with(text_attribute.value)
    assert result == "markdown_output"
