from streamlit.connections import BaseConnection

from infrahub_sdk import InfrahubClientSync, Config
from infrahub_sdk.branch import BranchData  # noqa: TC001
from infrahub_sdk.client import SchemaTypeSync  # noqa: TC001
from infrahub_sdk.exceptions import NodeNotFoundError

class InfrahubConnection(BaseConnection):

    def _connect(self) -> InfrahubClientSync:
        # config = Config(
        #     server_address = self._secrets.get("address", None)
        # )
        return InfrahubClientSync()

    @property
    def client(self) -> InfrahubClientSync:
        return self._instance

    def get_display_label(self, kind: str | type[SchemaTypeSync], id: str, branch: str | None = None) -> str:
        """Get the display label for an object."""
        try:
            obj = self.client.store.get(kind=kind, key=id,branch=branch)
            return obj.display_label
        except NodeNotFoundError as exc:
            pass

        return id

    def get_dropdown_options(
        self,
        kind: str | type[SchemaTypeSync],
        attribute_name: str,
        branch: str = "main",
        # client: InfrahubClientSync = Depends(get_client),
    ) -> list[str]:
        """Get dropdown options for a given attribute."""
        # Get schema for this kind

        schema = self.client.schema.get(kind=kind, branch=branch)

        # Find desired attribute
        matched_attribute = next((att for att in schema.attributes if att.name == attribute_name), None)

        if matched_attribute is None:
            raise Exception(f"Can't find attribute `{attribute_name}` for kind `{kind}`")
        return [choice["name"] for choice in matched_attribute.choices]
