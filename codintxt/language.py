import json
import random
import os
import pathlib
from os.path import join
from typing import Any

import textx.scoping.providers as scoping_providers
from rich import pretty, print
from textx import (
    TextXSemanticError,
    get_children_of_type,
    language,
    metamodel_from_file,
    get_location,
)
from textx.scoping import GlobalModelRepository, ModelRepository

from codintxt.definitions import THIS_DIR, MODEL_REPO_PATH, BUILTIN_MODELS

pretty.install()

CURRENT_FPATH = pathlib.Path(__file__).parent.resolve()

GLOBAL_REPO = GlobalModelRepository()


def verify_component_names(model):
    _ids = []
    components = model.components
    for b in components:
        if b.name in _ids:
            raise TextXSemanticError(
                f"Component with name <{b.name}> already exists", **get_location(b)
            )
        _ids.append(b.name)


def verify_broker_names(model):
    _ids = []
    brokers = get_children_of_type("MQTTBroker", model)
    brokers += get_children_of_type("AMQPBroker", model)
    brokers += get_children_of_type("RedisBroker", model)
    for b in brokers:
        if b.name in _ids:
            raise TextXSemanticError(
                f"Broker with name <{b.name}> already exists", **get_location(b)
            )
        _ids.append(b.name)


def transform_colors(model):
    color_enum_map = {
        "Red": "#ff0000",
        "red": "#ff0000",
        "Blue": "#00ff00",
        "blue": "#00ff00",
        "Green": "#00ff00",
        "green": "#00ff00",
        "Yellow": "#ffff00",
        "yellow": "#ffff00",
    }
    for component in model.components:
        if hasattr(component, 'color'):
            if str(component.color) in (None, ""):
                continue
            elif str(component.color) not in color_enum_map:  #  Hex
                continue
            try:
                component.color = color_enum_map[str(component.color)]
            except:
                component.color = random.choice(list(color_enum_map.values()))

def model_proc(model, metamodel):
    transform_colors(model)
    verify_broker_names(model)
    verify_component_names(model)
    verify_attr_id_valid(model)


def verify_attr_id_valid(model):
    for component in model.components:
        if hasattr(component, 'attribute'):
            if str(component.attribute) in (None, ""):
                continue
            if str(component.attribute) not in [str(attr.name) for attr in component.entity.attributes]:
                raise TextXSemanticError(
                    f"Attribute <{component.attribute}> does not exist in component <{component.name}>",
                    **get_location(component),
                )


CUSTOM_CLASSES = [
]


def class_provider(name):
    classes = dict(map(lambda x: (x.__name__, x), CUSTOM_CLASSES))
    return classes.get(name)


def component_attribute_processor(component):
    if component.attribute == None:
        component.attribute = ""
    return component


def nid_processor(nid):
    nid = nid.replace("\n", "")
    return nid


def plot_processor(plot):
    if not plot.color:
        plot.color = "#FF9D66"


def plotview_processor(plotview):
    if not plotview.legendPosition:
        plotview.legendPosition = "topRight"
    return plotview


def gauge_processor(gauge):
    if not gauge.leftColor:
        gauge.leftColor = "Green"
    if not gauge.rightColor:
        gauge.rightColor = "Red"
    return component_attribute_processor(gauge)


def button_processor(button):
    if not button.color:
        button.color = "Blue"
    if not button.bg:
        button.bg = "#FF9D66"
    if not button.hover:
        button.hover = "#ff7e33"
    return button


def value_display_processor(vdisplay):
    return component_attribute_processor(vdisplay)


def json_viewer_processor(jviewer):
    return component_attribute_processor(jviewer)


def logs_display_processor(ldisplay):
    return component_attribute_processor(ldisplay)


obj_processors = {
    'Gauge': gauge_processor,
    'Button': button_processor,
    'ValueDisplay': value_display_processor,
    'JsonViewer': json_viewer_processor,
    'LogsDisplay': logs_display_processor,
    'Plot': plot_processor,
    'PlotView': plotview_processor,
    'NID': nid_processor,
}


def get_metamodel(debug: bool = False, global_repo: bool = False):
    metamodel = metamodel_from_file(
        join(THIS_DIR, 'grammar', 'codin.tx'),
        classes=class_provider,
        auto_init_attributes=True,
        textx_tools_support=True,
        global_repository=global_repo,
        debug=debug,
    )
    metamodel.register_scope_providers(get_scode_providers())
    metamodel.register_model_processor(model_proc)
    metamodel.register_obj_processors(obj_processors)
    return metamodel


def get_scode_providers():
    sp = {"*.*": scoping_providers.FQNImportURI(importAs=True)}
    if BUILTIN_MODELS:
        sp["brokers*"] = scoping_providers.FQNGlobalRepo(
            join(BUILTIN_MODELS, "broker", "*.goal"))
        sp["entities*"] = scoping_providers.FQNGlobalRepo(
            join(BUILTIN_MODELS, "entity", "*.goal"))
    if MODEL_REPO_PATH:
        sp["brokers*"] = scoping_providers.FQNGlobalRepo(
            join(MODEL_REPO_PATH, "broker", "*.goal"))
        sp["entities*"] = scoping_providers.FQNGlobalRepo(
            join(MODEL_REPO_PATH, "entity", "*.goal"))
    return sp


def build_model(model_path: str, debug: bool = False):
    # Parse model
    mm = get_metamodel(debug=debug)
    model = mm.model_from_file(model_path)
    return model


@language("codintxt", "*.codin")
def codintxt_language():
    "Codin Textual DSL"
    mm = get_metamodel()
    return mm
