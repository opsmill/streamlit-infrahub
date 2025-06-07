from typing import Any

from infrahub_sdk.schema import AttributeSchemaAPI
from infrahub_sdk.schema.main import AttributeKind


def get_choice(attr: AttributeSchemaAPI, value: Any) -> dict[str, Any] | None:
    """Get the choice for a dropdown attribute.

    Retrieves the choice object from the attribute's choices list that matches the given value.

    Args:
        attr: The attribute schema containing the choices.
        value: The value to match against the choice names.

    Returns:
        The matching choice dictionary if found, None otherwise.
    """
    options = [item for item in attr.choices if item["name"] == value]
    if len(options) == 1:
        return options[0]

    return None


def display_attribute(attr: AttributeSchemaAPI, value: Any, container: Any) -> str:
    """Display an attribute in a human-readable format.

    Formats the attribute value based on its kind. For dropdown attributes,
    displays a badge with the choice label. For other types, displays the value
    as markdown.

    Args:
        attr: The attribute schema to display.
        value: The value to display.
        container: The Streamlit container to use for display elements.

    Returns:
        The formatted display string.
    """
    if attr.kind == AttributeKind.DROPDOWN:
        choice = get_choice(attr=attr, value=value)
        if choice:
            return container.badge(choice.get("label", value), color="primary")

    return container.markdown(attr.value)
