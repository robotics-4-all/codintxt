import os
from os.path import join
from textx import language, metamodel_from_file, get_children_of_type, TextXSemanticError
import pathlib
import textx.scoping.providers as scoping_providers
from rich import print, pretty
from textx.scoping import ModelRepository, GlobalModelRepository
from codintxt.definitions import MODEL_REPO_PATH
from typing import Any, Dict, List
from pydantic import BaseModel

pretty.install()

CURRENT_FPATH = pathlib.Path(__file__).parent.resolve()

GLOBAL_REPO = GlobalModelRepository()


def get_metamodel(debug=False) -> Any:
    metamodel = metamodel_from_file(
        CURRENT_FPATH.joinpath('grammar/codin.tx'),
        auto_init_attributes=True,
        global_repository=GLOBAL_REPO,
        debug=debug
    )

    metamodel.register_scope_providers(
        {
            "*.*": scoping_providers.FQNImportURI(importAs=True),
            # "entities*": scoping_providers.FQNGlobalRepo(
            #     join(MODEL_REPO_PATH, 'entity', 'system_clock.smauto')
            # ),
        }
    )
    return metamodel


class Component(BaseModel):
    ctype: str
    name: str
    label: str
    topic: str
    broker: str
    position: Dict[str, Any]


class Gauge(Component):
    attribute: str
    minValue: int
    maxValue: int
    leftColor: str = ""
    rightColor: str = ""
    levels: int = 10
    hideTxt: bool = False
    unit: str = ""


class ValueDisplay(Component):
    attribute: str
    unit: str = ""


class JsonViewer(Component):
    attribute: str


class AliveDisplay(Component):
    timeout: int


class Button(Component):
    dynamic: bool = False
    color: str = ''
    background: str = ''
    hover: str = ''
    payload: Dict[str, Any]


class Broker(BaseModel):
    name: str
    btype: str
    host: str
    port: int
    auth: Dict[str, Any]


class CodinTxtModel(BaseModel):
    brokers: List[Broker]
    components: List[Any]


def model_2_object(model):
    _brokers = []
    _components = []
    for broker in model.brokers:
        br = Broker(
            name=broker.name,
            btype=broker.__class__.__name__,
            host=broker.host,
            port=broker.port,
            auth={
                'username': broker.auth.username,
                'password': broker.auth.password,
            }
        )
        _brokers.append(br)
    for component in model.components:
        if component.__class__.__name__ == 'Gauge':
            cmp = Gauge(
                ctype='Gauge',
                name=component.name,
                label=component.label,
                topic=component.topic,
                broker=component.broker.name,
                attribute=component.attribute,
                minValue=component.minValue,
                maxValue=component.maxValue,
                leftColor=str(component.leftColor),
                rightColor=str(component.rightColor),
                levels=component.levels,
                hideTxt=component.hideTxt,
                unit=component.unit,
                position={
                    'x': component.position.x,
                    'y': component.position.y,
                    'w': component.position.w,
                    'h': component.position.h,
                }
            )
        elif component.__class__.__name__ == 'ValueDisplay':
            cmp = ValueDisplay(
                ctype='ValueDisplay',
                name=component.name,
                label=component.label,
                topic=component.topic,
                broker=component.broker.name,
                attribute=component.attribute,
                unit=component.unit,
                position={
                    'x': component.position.x,
                    'y': component.position.y,
                    'w': component.position.w,
                    'h': component.position.h,
                }
            )
        elif component.__class__.__name__ == 'JsonViewer':
            cmp = JsonViewer(
                ctype='JsonViewer',
                name=component.name,
                label=component.label,
                topic=component.topic,
                broker=component.broker.name,
                attribute=component.attribute,
                position={
                    'x': component.position.x,
                    'y': component.position.y,
                    'w': component.position.w,
                    'h': component.position.h,
                }
            )
        elif component.__class__.__name__ == 'AliveDisplay':
            cmp = AliveDisplay(
                ctype='AliveDisplay',
                name=component.name,
                label=component.label,
                topic=component.topic,
                broker=component.broker.name,
                timeout=component.timeout,
                position={
                    'x': component.position.x,
                    'y': component.position.y,
                    'w': component.position.w,
                    'h': component.position.h,
                }
            )
        elif component.__class__.__name__ == 'Button':
            cmp = Button(
                ctype='Button',
                name=component.name,
                label=component.label,
                topic=component.topic,
                broker=component.broker.name,
                dynamic=component.dynamic,
                color=str(component.color),
                background=str(component.bg),
                hover=str(component.hover),
                payload={attr.name: attr.default for attr in component.payload},
                position={
                    'x': component.position.x,
                    'y': component.position.y,
                    'w': component.position.w,
                    'h': component.position.h,
                }
            )
        else:
            continue
        _components.append(cmp)
    _model = CodinTxtModel(
        brokers=_brokers,
        components=_components,
    )
    return _model


def model_2_codin(model) -> Dict[str, Any]:
    _model = model_2_object(model)
    # print(_model)
    _json: Dict[str, Any] = {}
    # TODO: Implement the transformation to Codin json
    return _json


def model_2_json(model) -> Dict[str, Any]:
    _model = model_2_object(model)
    return _model.model_dump()


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
