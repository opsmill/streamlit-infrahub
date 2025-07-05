"""Test fixtures for unit tests."""

from typing import Any
from unittest.mock import MagicMock

import pytest
from infrahub_sdk.schema import AttributeSchemaAPI
from infrahub_sdk.schema.main import AttributeKind


def create_attribute_schema(
    kind: AttributeKind = AttributeKind.DROPDOWN, choices: list[dict[str, Any]] | None = None, value: Any = None
) -> AttributeSchemaAPI:
    """Create an AttributeSchemaAPI instance for testing.

    Args:
        kind: The kind of attribute (default: DROPDOWN).
        choices: The list of choices for dropdown attributes.
        value: The value of the attribute.

    Returns:
        An AttributeSchemaAPI instance with the specified attributes.
    """
    attr_schema = MagicMock(spec=AttributeSchemaAPI)
    attr_schema.kind = kind
    attr_schema.choices = choices or []
    attr_schema.value = value
    return attr_schema


@pytest.fixture
def dropdown_attr_with_choices() -> AttributeSchemaAPI:
    """Fixture providing an attribute schema with choices.

    Returns:
        An AttributeSchemaAPI object with predefined choices.
    """
    return create_attribute_schema(
        kind=AttributeKind.DROPDOWN,
        choices=[
            {"name": "option1", "label": "Option 1"},
            {"name": "option2", "label": "Option 2"},
        ],
    )


@pytest.fixture
def dropdown_attr_with_duplicate_choices() -> AttributeSchemaAPI:
    """Fixture providing an attribute schema with duplicate choices.

    Returns:
        An AttributeSchemaAPI object with duplicate choices.
    """
    return create_attribute_schema(
        kind=AttributeKind.DROPDOWN,
        choices=[
            {"name": "option1", "label": "Option 1"},
            {"name": "option1", "label": "Option 1 Duplicate"},
        ],
    )


@pytest.fixture
def dropdown_attr_empty_choices() -> AttributeSchemaAPI:
    """Fixture providing an attribute schema with no choices.

    Returns:
        An AttributeSchemaAPI object with an empty choices list.
    """
    return create_attribute_schema(
        kind=AttributeKind.DROPDOWN,
        choices=[],
    )


@pytest.fixture
def streamlit_container() -> MagicMock:
    """Fixture providing a mock Streamlit container.

    Returns:
        A mock Streamlit container with badge and markdown methods.
    """
    container = MagicMock()
    container.badge.return_value = "badge_output"
    container.markdown.return_value = "markdown_output"
    return container


@pytest.fixture
def text_attribute() -> AttributeSchemaAPI:
    """Fixture providing a text attribute.

    Returns:
        An AttributeSchemaAPI object configured as a text attribute.
    """
    return create_attribute_schema(
        kind=AttributeKind.TEXT,
        value="sample text",
    )
