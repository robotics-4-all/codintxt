from os.path import join
from rich import print, pretty
from codintxt.definitions import MODEL_REPO_PATH
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import json

pretty.install()


class Component(BaseModel):
    ctype: str
    name: str
    label: str = ""
    topic: str = ""
    broker: str = ""
    position: Dict[str, Any]


class Gauge(Component):
    attribute: str = ""
    minValue: int = 0
    maxValue: int = 100
    leftColor: str = "blue"
    rightColor: str = "red"
    levels: int = 10
    hideTxt: bool = False
    unit: str = ""


class ValueDisplay(Component):
    attribute: str
    unit: str = ""


class JsonViewer(Component):
    attribute: str = ""


class AliveDisplay(Component):
    timeout: int = 60


class LogsDisplay(Component):
    attribute: str = ""
    maxMsg: int = -1
    highlights: List[Dict[str, Any]] = [
        {"key": "Error", "color": "red"},
        {"key": "error", "color": "red"},
        {"key": "Exception", "color": "red"},
        {"key": "exception", "color": "red"},
        {"key": "failed", "color": "red"},
        {"key": "Warning", "color": "yellow"},
        {"key": "warning", "color": "yellow"},
    ]


class Button(Component):
    dynamic: bool = True
    color: str = "white"
    background: str = "#FF9D66"
    hover: str = "#ff7e33"
    payload: Dict[str, Any]


class ButtonGroup(Component):
    alignTxt: str = ""
    alignBtns: str = ""
    buttons: List[Button]


class Broker(BaseModel):
    name: str
    btype: str
    host: str
    port: int
    ssl: Optional[bool] = False
    auth: Dict[str, Any]


# Child class does not serialize. Workaround to use the BaseModel
class MQTTBroker(Broker):
    basePath: Optional[str] = ""
    webPath: Optional[str] = "/mqtt"
    webPort: Optional[int] = 8883


class CodinTxtModel(BaseModel):
    brokers: List[Any]
    components: List[Any]
    metadata: Dict[str, Any]


def model_2_object(model):
    _brokers = []
    _components = []
    for broker in model.brokers:
        if broker.__class__.__name__ == "MQTTBroker":
            br = MQTTBroker(
                name=broker.name,
                btype=broker.__class__.__name__,
                host=broker.host,
                port=broker.port,
                ssl=broker.ssl,
                basePath=broker.basePath,
                webPath=broker.webPath,
                webPort=broker.webPort,
                auth={
                    "username": broker.auth.username,
                    "password": broker.auth.password,
                },
            )
        else:
            br = Broker(
                name=broker.name,
                btype=broker.__class__.__name__,
                host=broker.host,
                ssl=broker.ssl,
                port=broker.port,
                auth={
                    "username": broker.auth.username,
                    "password": broker.auth.password,
                },
            )
        _brokers.append(br)
    for component in model.components:
        if component.__class__.__name__ == "Gauge":
            cmp = Gauge(
                ctype="Gauge",
                name=component.name,
                label=component.label,
                topic=component.entity.topic.replace(".", "/"),
                broker=component.entity.broker.name,
                attribute=component.attribute,
                minValue=component.minValue,
                maxValue=component.maxValue,
                leftColor=str(component.leftColor),
                rightColor=str(component.rightColor),
                levels=component.levels,
                hideTxt=component.hideTxt,
                unit=component.unit,
                position={
                    "x": component.position.x,
                    "y": component.position.y,
                    "w": component.position.w,
                    "h": component.position.h,
                },
            )
        elif component.__class__.__name__ == "ValueDisplay":
            cmp = ValueDisplay(
                ctype="ValueDisplay",
                name=component.name,
                label=component.label,
                topic=component.entity.topic.replace(".", "/"),
                broker=component.entity.broker.name,
                attribute=component.attribute,
                unit=component.unit,
                position={
                    "x": component.position.x,
                    "y": component.position.y,
                    "w": component.position.w,
                    "h": component.position.h,
                },
            )
        elif component.__class__.__name__ == "JsonViewer":
            cmp = JsonViewer(
                ctype="JsonViewer",
                name=component.name,
                label=component.label,
                topic=component.entity.topic.replace(".", "/"),
                broker=component.entity.broker.name,
                attribute=component.attribute,
                position={
                    "x": component.position.x,
                    "y": component.position.y,
                    "w": component.position.w,
                    "h": component.position.h,
                },
            )
        elif component.__class__.__name__ == "LogsDisplay":
            cmp = LogsDisplay(
                ctype="LogsDisplay",
                name=component.name,
                label=component.label,
                topic=component.entity.topic.replace(".", "/"),
                broker=component.entity.broker.name,
                attribute=component.attribute,
                maxMsg=component.maxMsg,
                position={
                    "x": component.position.x,
                    "y": component.position.y,
                    "w": component.position.w,
                    "h": component.position.h,
                },
            )
            if len(component.colorKeys):
                cmp.highlights = [{hl.key: str(hl.color)} for hl in component.colorKeys]
        elif component.__class__.__name__ == "AliveDisplay":
            cmp = AliveDisplay(
                ctype="AliveDisplay",
                name=component.name,
                label=component.label,
                topic=component.entity.topic.replace(".", "/"),
                broker=component.entity.broker.name,
                timeout=component.timeout,
                position={
                    "x": component.position.x,
                    "y": component.position.y,
                    "w": component.position.w,
                    "h": component.position.h,
                },
            )
        elif component.__class__.__name__ == "ButtonGroup":
            btns = [
                Button(
                    ctype="Button",
                    name=btn.name,
                    label=btn.label,
                    topic=btn.entity.topic.replace(".", "/"),
                    broker=btn.entity.broker.name,
                    dynamic=btn.dynamic,
                    color=str(btn.color),
                    background=str(btn.bg),
                    hover=str(btn.hover),
                    payload=dict(zip(btn.attrName, btn.attrVal)),
                    position={"x": 0, "y": 0, "w": 0, "h": 0},
                )
                for btn in component.buttons
            ]
            cmp = ButtonGroup(
                ctype="ButtonGroup",
                name=component.name,
                label=component.label,
                alignTxt=component.alignTxt,
                alignBtns=component.alignBtns,
                buttons=btns,
                position={
                    "x": component.position.x,
                    "y": component.position.y,
                    "w": component.position.w,
                    "h": component.position.h,
                },
            )
        else:
            continue
        _components.append(cmp)
    _model = CodinTxtModel(
        brokers=_brokers,
        components=_components,
        metadata={
            "name": model.metadata.name,
            "token": model.metadata.token,
        },
    )
    return _model


def model_2_codin(model) -> Dict[str, Any]:
    _model = model_2_object(model)
    _brokers = [br.dict() for br in _model.brokers]
    _json: Dict[str, Any] = model_2_json(model)
    codin_json: Dict[str, Any] = {
        "layout": [],
        "items": {},
        "sources": _brokers,
        "metadata": _model.metadata,
    }

    colors = {"Red": "#ff0000", "Blue": "#00ff00", "Green": "#00ff00"}

    # Get the brokers
    brokers = {}
    for b in _json["brokers"]:
        brokers[b["name"]] = b

    # Get the components
    current_id = 0
    for c in _json["components"]:
        current_id += 1
        str_id = str(current_id)

        # Handle the layout
        l = {
            "i": str_id,
            "x": c["position"]["x"],
            "y": c["position"]["y"],
            "w": c["position"]["w"],
            "h": c["position"]["h"],
            "minW": 1,
            "minH": 1,
            "moved": False,
            "static": False,
        }
        codin_json["layout"].append(l)

        # Handle the config
        if c["ctype"] == "Gauge":
            config = {
                "type": "gauge",
                "name": c["name"],
                "source": c["broker"],  # check this for duplicates
                "topic": c["topic"],
                "variable": c["attribute"],
                "minValue": c["minValue"],
                "maxValue": c["maxValue"],
                "leftColor": colors[c["leftColor"]],
                "rightColor": colors[c["rightColor"]],
                "levels": c["levels"],
                "hideText": c["hideTxt"],
                "unit": c["unit"],
            }
            codin_json["items"][str_id] = config
        elif c["ctype"] == "ValueDisplay":
            config = {
                "type": "value",
                "name": c["name"],
                "source": c["broker"],
                "topic": c["topic"],
                "variable": c["attribute"],
                "unit": "%",
            }
            codin_json["items"][str_id] = config
        elif c["ctype"] == "JsonViewer":
            config = {
                "type": "json",
                "name": c["name"],
                "source": c["broker"],
                "topic": c["topic"],
                "variable": c["attribute"],
            }
            codin_json["items"][str_id] = config
        elif c["ctype"] == "LogsDisplay":
            config = {
                "type": "logs",
                "name": c["name"],
                "source": c["broker"],
                "topic": c["topic"],
                "variable": c["attribute"],
                "maxMessages": c["maxMsg"],
                "colorKeys": [hl["key"] for hl in c["highlights"]],
                "colorValues": [hl["color"] for hl in c["highlights"]],
            }
            codin_json["items"][str_id] = config
        elif c["ctype"] == "AliveDisplay":
            config = {
                "type": "alive",
                "name": c["name"],
                "source": c["broker"],
                "topic": c["topic"],
                "timeout": c["timeout"],
            }
            codin_json["items"][str_id] = config
        elif c["ctype"] == "ButtonGroup":
            config = {
                "type": "buttons",
                "name": c["name"],
                "alignText": c["alignTxt"],
                "buttonsAlign": c["alignBtns"],
                "texts": [btn["name"] for btn in c["buttons"]],
                "sources": [btn["broker"] for btn in c["buttons"]],
                "topics": [btn["topic"] for btn in c["buttons"]],
                "payloads": [json.dumps(btn["payload"]) for btn in c["buttons"]],
                "isDynamic": [btn["dynamic"] for btn in c["buttons"]],
                "colors": [
                    "white" if btn["color"] in (None, "", "None") else btn["color"]
                    for btn in c["buttons"]
                ],
                "backgrounds": [
                    "#FF9D66"
                    if btn["background"] in (None, "", "None")
                    else btn["background"]
                    for btn in c["buttons"]
                ],
                "backgroundsHover": [
                    "#ff7e33" if btn["hover"] in (None, "", "None") else btn["hover"]
                    for btn in c["buttons"]
                ],
            }
            codin_json["items"][str_id] = config

    overlap = check_overlapping(codin_json)
    if overlap:
        raise ValueError("Visual Component Overlapping issue!")
    return codin_json


def check_overlapping(codin_json: Dict[str, Any]):
    # Validation
    occupancy = {}
    failed = False
    msg = ""
    for element in codin_json["layout"]:
        for i in range(element["x"], element["x"] + element["w"] - 1):
            for j in range(element["y"], element["y"] + element["h"] - 1):
                if (i, j) in occupancy:
                    msg = f"Conflict between elements {element['i']} and {occupancy[(i,j)]} in place {(i,j)}"
                    failed = True
                    break
                else:
                    occupancy[(i, j)] = element["i"]
            if failed:
                break
        if failed:
            break
    return failed


def model_2_json(model) -> Dict[str, Any]:
    _model = model_2_object(model)
    return _model.model_dump()
