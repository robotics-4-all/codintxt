import json
import os
import pathlib
from os.path import join
from typing import Any

import textx.scoping.providers as scoping_providers
from rich import pretty, print
from textx import (TextXSemanticError, get_children_of_type, language,
                   metamodel_from_file, get_location)
from textx.scoping import GlobalModelRepository, ModelRepository

from codintxt.definitions import MODEL_REPO_PATH

pretty.install()

CURRENT_FPATH = pathlib.Path(__file__).parent.resolve()

GLOBAL_REPO = GlobalModelRepository()


def verify_component_names(model):
    _ids = []
    components = model.components
    for b in components:
        if b.name in _ids:
            raise TextXSemanticError(
                f'Component with name <{b.name}> already exists', **get_location(b)
            )
        _ids.append(b.name)


def verify_broker_names(model):
    _ids = []
    brokers = get_children_of_type('MQTTBroker', model)
    brokers += get_children_of_type('AMQPBroker', model)
    brokers += get_children_of_type('RedisBroker', model)
    for b in brokers:
        if b.name in _ids:
            raise TextXSemanticError(
                f'Broker with name <{b.name}> already exists', **get_location(b)
            )
        _ids.append(b.name)


def model_proc(model, metamodel):
    verify_broker_names(model)
    verify_component_names(model)


def get_metamodel(debug=False) -> Any:
    metamodel = metamodel_from_file(
        CURRENT_FPATH.joinpath('grammar/codin.tx'),
        auto_init_attributes=True,
        # global_repository=GLOBAL_REPO,
        debug=debug
    )

    metamodel.register_scope_providers(
        {
            "*.*": scoping_providers.FQNImportURI(importAs=True),
            # "*.*": scoping_providers.FQNGlobalRepo(
            #     join(MODEL_REPO_PATH, '*.codin')
            # ),
        }
    )
    metamodel.register_model_processor(model_proc)
    return metamodel


def build_model(model_path: str, debug: bool = False):
    # Parse model
    mm = get_metamodel(debug=debug)
    model = mm.model_from_file(model_path)
    return model


def get_model_grammar(model_path):
    mm = get_metamodel()
    grammar_model = mm.grammar_model_from_file(model_path)
    return grammar_model


@language('codintxt', '*.codin')
def codintxt_language():
    "Codin Textual DSL"
    mm = get_metamodel()
    return mm
