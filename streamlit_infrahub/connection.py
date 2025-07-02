from typing import Any

from infrahub_sdk import InfrahubClientSync
from infrahub_sdk.client import SchemaTypeSync
from infrahub_sdk.exceptions import NodeNotFoundError
from streamlit.connections import BaseConnection


class InfrahubConnection(BaseConnection):
    def _connect(self, **kwargs: Any) -> InfrahubClientSync:  # noqa: PLR6301, ARG002
        """Initialize and return a new InfrahubClientSync instance.

        This is an internal method used by Streamlit's connection framework.

        Returns:
            InfrahubClientSync: A new Infrahub client instance.
        """
        # config = Config(
        #     server_address = self._secrets.get("address", None)
        # )
        return InfrahubClientSync()

    @property
    def client(self) -> InfrahubClientSync:
        """Get the Infrahub client instance.

        Returns:
            InfrahubClientSync: The current Infrahub client instance.
        """
        return self._instance

    def get_display_label(self, kind: str | type[SchemaTypeSync], id: str, branch: str | None = None) -> str:  # noqa: A002
        """Get the display label for an Infrahub object.

        Args:
            kind: The kind of object (e.g., 'Device', 'Interface') or its schema type.
            id: The unique identifier of the object.
            branch: Optional branch name to query from. Defaults to None.

        Returns:
            str: The display label of the object if found, otherwise returns the input id.
        """
        try:
            obj = self.client.store.get(kind=kind, key=id, branch=branch)
            return obj.display_label
        except NodeNotFoundError:
            pass

        return id

    def get_dropdown_options(
        self,
        kind: str | type[SchemaTypeSync],
        attribute_name: str,
        branch: str = "main",
        # client: InfrahubClientSync = Depends(get_client),
    ) -> list[str]:
        """Get the list of valid choices for a specific attribute of a given kind.

        Args:
            kind: The kind of object (e.g., 'Device', 'Interface') or its schema type.
            attribute_name: The name of the attribute to get choices for.
            branch: The branch to query from. Defaults to "main".

        Returns:
            list[str]: A list of valid choice names for the specified attribute.

        Raises:
            Exception: If the specified attribute is not found for the given kind.
        """
        # Get schema for this kind

        schema = self.client.schema.get(kind=kind, branch=branch)

        # Find desired attribute
        matched_attribute = next((att for att in schema.attributes if att.name == attribute_name), None)

        if matched_attribute is None:
            raise Exception(f"Can't find attribute `{attribute_name}` for kind `{kind}`")
        return [choice["name"] for choice in matched_attribute.choices]
