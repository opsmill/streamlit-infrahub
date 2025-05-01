from typing import Any

from infrahub_sdk.schema import AttributeSchemaAPI
from infrahub_sdk.schema.main import AttributeKind


def get_choice(attr: AttributeSchemaAPI, value: Any) -> dict[str, Any] | None:
    """Get the choice for a dropdown attribute."""
    options = [item for item in attr.choices if item["name"] == value]
    if len(options) == 1:
        return options[0]

    return None


def display_attribute(attr: AttributeSchemaAPI, value: Any, container: Any) -> str:
    """Display an attribute in a human-readable format."""
    if attr.kind == AttributeKind.DROPDOWN:
        choice = get_choice(attr=attr, value=value)
        if choice:
            return container.badge(choice.get("label", value), color="primary")

    return container.markdown(attr.value)
