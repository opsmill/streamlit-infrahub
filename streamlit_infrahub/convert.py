from typing import Any

import polars as pl
from infrahub_sdk.node import Attribute, InfrahubNode, RelatedNode, RelationshipManager
from infrahub_sdk.schema.main import GenericSchemaAPI, NodeSchemaAPI


def node_to_dict(obj: InfrahubNode, include_id: bool = True) -> dict[str, Any]:
    """Convert an InfrahubNode object to a dictionary representation.

    This function converts an InfrahubNode object into a dictionary format, including its attributes
    and relationships. It handles both single relationships (RelatedNode) and multiple relationships
    (RelationshipManager).

    Args:
        obj: The InfrahubNode object to convert
        include_id: Whether to include the node's ID in the output dictionary. Defaults to True.

    Returns:
        A dictionary containing the node's attributes and relationships, with relationship values
        represented as either single IDs or lists of IDs.
    """
    data = {}

    if include_id:
        data["index"] = obj.id or None

    for attr_name in obj._schema.attribute_names:  # noqa: SLF001
        attr: Attribute = getattr(obj, attr_name)
        data[attr_name] = attr.value

    for rel_name in obj._schema.relationship_names:  # noqa: SLF001
        rel = getattr(obj, rel_name)
        if not rel.initialized:
            continue
        if rel and isinstance(rel, RelatedNode):
            related_node = rel.peer
            data[rel_name] = (
                related_node.get_human_friendly_id_as_string(include_kind=True)
                if related_node.hfid
                else related_node.id
            )
        elif rel and isinstance(rel, RelationshipManager):
            peers: list[dict[str, Any]] = []
            for peer in rel.peers:
                related_node = peer.peer
                if not related_node:
                    continue
                # peer.fetch()
                # related_node = peer.peer
                peers.append(
                    related_node.get_human_friendly_id_as_string(include_kind=True)
                    if related_node.hfid
                    else related_node.id
                )
            data[rel_name] = peers
    return data


def nodes_to_df(
    schema: NodeSchemaAPI | GenericSchemaAPI,
    nodes: list[InfrahubNode],
    include: list[str] | None = None,
) -> pl.DataFrame:
    """Convert a list of InfrahubNodes to a Polars DataFrame.

    This function takes a list of InfrahubNode objects and converts them into a Polars DataFrame,
    using the schema to determine the structure and order of columns. The function can optionally
    filter which attributes to include in the resulting DataFrame.

    Args:
        schema: The schema API object defining the node structure
        nodes: List of InfrahubNode objects to convert
        include: Optional list of attribute names to include in the DataFrame. If None, includes all attributes.

    Returns:
        A Polars DataFrame containing the node data with columns for each included attribute,
        ordered according to the schema's attribute order weights.
    """
    # relationships = [rel for rel in schema.relationships if rel.cardinality == "one"]
    # relationship_names = [rel.name for rel in relationships]
    columns = schema.attribute_names  # + relationship_names

    columns = [(item.name, item.order_weight) for item in schema.attributes if not include or item.name in include]

    sorted_columns = sorted(columns, key=lambda x: x[1])  # noqa: FURB118

    data = {}

    for attr_name in schema.attribute_names:
        if include and attr_name not in include:
            continue
        data[attr_name] = [getattr(node, attr_name).value for node in nodes]

    # for rel_name in relationship_names:
    #     data[rel_name] = []
    #     for node in nodes:
    #         related_node = getattr(node, rel_name)
    #         if related_node.peer:
    #             data[rel_name].append(related_node.display_label)
    #         else:
    #             data[rel_name].append(None)

    return pl.DataFrame(data, schema=[col[0] for col in sorted_columns])
