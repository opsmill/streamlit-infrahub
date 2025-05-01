from infrahub_sdk.schema import AttributeSchemaAPI
from infrahub_sdk.schema.main import AttributeKind, NodeSchemaAPI, GenericSchemaAPI
from infrahub_sdk.node import InfrahubNode, Attribute, RelatedNode, RelationshipManager
from typing import Any

import polars as pl

import streamlit as st

def node_to_dict(obj: InfrahubNode, include_id: bool = True) -> dict[str, Any]:
    data = {}

    if include_id:
        data["index"] = obj.id or None

    for attr_name in obj._schema.attribute_names:
        attr: Attribute = getattr(obj, attr_name)
        data[attr_name] = attr.value

    for rel_name in obj._schema.relationship_names:
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

def nodes_to_df(schema: NodeSchemaAPI | GenericSchemaAPI, nodes: list[InfrahubNode], include: list[str] | None = None) -> pl.DataFrame:

    relationships = [ rel for rel in schema.relationships if rel.cardinality == "one"]
    relationship_names = [ rel.name for rel in relationships ]
    columns = schema.attribute_names # + relationship_names

    columns = [ (item.name, item.order_weight) for item in schema.attributes if not include or item.name in include ]

    sorted_columns = sorted(columns, key=lambda x: x[1])

    data = {}

    for attr_name in schema.attribute_names:
        if include and attr_name not in include:
            continue
        data[attr_name] = [ getattr(node, attr_name).value for node in nodes ]

    # for rel_name in relationship_names:
    #     data[rel_name] = []
    #     for node in nodes:
    #         related_node = getattr(node, rel_name)
    #         if related_node.peer:
    #             data[rel_name].append(related_node.display_label)
    #         else:
    #             data[rel_name].append(None)

    df = pl.DataFrame(data, schema=[col[0] for col in sorted_columns])
    return df

