
![CodinTxt_Light](https://github.com/robotics-4-all/codintxt/assets/4770702/4151cda1-9d69-46e7-8953-ba28ee60fb02)


# Introduction

CodinTxt is a textual DSL for automating the development process for the
[Codin low-code platform](https://codin.issel.ee.auth.gr/).

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/e2e18911-077d-4af1-ad95-c5d4475dd722)

Codin was engineered and developed at the [ISSEL Laboratory](https://lab.issel.ee.auth.gr/) to automate the development process of
Dashboards for Cyber-Physical Systems. It provides a Web UI for developing Dashboards using drag-and-drop of various
components for remote monitoring and control of devices, applications and systems.

**Note #1**: For the auto deployment to Codin you have to create a Token from your **Codin Profile Page** (see image below)

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/522caa8f-15b5-43fa-8df8-d068b2e0aa8e)


CodinTxt defines a Metamodel for the Codin Platform (thus it is
Platform-specific) and allows definition of Dashboards using textual semantics,
while it also provides an **M2T Transformation** for generating a Json that can
be imported in Codin.


# The Language

The grammar of the DSL is pretty simple.

A CodinTxt model includes:
- Metadata definition
- Broker Definition
- Visual components

The **Metadata** section must be top-level, before any other definitions. In the same way, **Broker** definitions follow, but before any **Visual Component** definition.

## Metadata

Model metadata include the following information:

- **name**: The name of the model
- **description**: A brief description of the model
- **authoer**: The author of the model
- **token**: The Codin API Token for deployment purposes

Below is an example Metadata definition.

```
Metadata
    name: "MyCodinTxtModel"
    description: "My first CodinTxt model"
    author: "klpanagi"
    token: "CODIN_TOKEN_HERE"  // ** The Codin token **
end
```

The token is used to deploy the dashboard in Codin

## Broker

The Broker acts as the communication layer for messages where each device has
its own Topic which is basically a mailbox for sending and receiving messages.
SmartAutomation DSL supports Brokers which support the MQTT, AMQP and Redis
protocols. You can define a Broker using the syntax in the following example:

```
Broker<MQTT> default_broker
    host: "emqx.auth.gr"
    port: 1883
    ssl: false
    webPath: "/mqtt"
    webPort: 8093  // 8093 is the MQTT over websockets port for EMQX broker
    auth:
        username: "BROKER_USERNAME"
        password: "BROKER_PASSWORD"
end
```


Broker definitions include the following information:

- **type**: The first line can be `MQTT`, `AMQP` or `Redis` according to the Broker type
- **host**: Host IP address or hostname for the Broker
- **port**: Broker (default protocol) port number
- **ssl**: Whether or not to use SSL/TLS for communication
- **webPort**: Broker Web port number for MQTT over Websockets communication
- **webPath**: Broker Web transport default path (usually `/ws` or `/mqtt`) for MQTT over Websockets communication
- **auth**: Authentication credentials. Unified for all communication brokers.
    - **username**: Username used for authentication
    - **password**: Password used for authentication
- **vhost (Optional)**: Vhost parameter. Only for AMQP brokers
- **topicExchange (Optional)**: (Optional) Exchange parameter. Only for AMQP brokers.
- **rpcExchange (Optional)**: Exchange parameter. Only for AMQP brokers.
- **db (Optional)**: Database number parameter. Only for Redis brokers.


## Entities

Entities are your connected smart devices that send and receive information
using a message broker. Entities have the following required properties:

- A unique name
- A broker to connect to
- A topic to send/receive messages
- A set of attributes

**Attributes** are what define the structure and the type of information in the
messages the Entity sends to the communication broker.

Entity definitions follow the syntax of the below examples, for both sensor and actuator types. The difference between the two is that sensors are considered "Producers" while actuators are "Consumers" in the environment. Sensor Entities have an extra property, that is the `freq` to set the publishing frequency of either physical or virtual.

```
Entity EnvSensor_1
    type: sensor
    topic: 'bedroom.sensors.env'
    broker: CloudMQTT
    description: "A smart env sensor installed in the bedroom of the house"
    attributes:
        - temperature: float
        - humidity: float
        - gas: float
end

Entity Logs_A
    type: sensor
    topic: "myagent.logs"
    broker: BrokerA
    description: "Logs received from a software agent attached to the system"
    attributes:
        - msg: dict
        - level: str
end
```

```
Entity Bulb_A
    type: actuator
    topic: "bedroom.actuators.bulb_a"
    broker: CloudMQTT
    description: "A smart bulb installed in the bedroom of the house"
    attributes:
        - state: bool
        - brightness: float
end

Entity Switch_2
    type: actuator
    topic: 'bedroom.actuators.switch_2'
    broker: CloudMQTT
    description: "A smart switch with two in-out lines installed in the bedroom of the house"
    attributes:
        - out_a: bool
        - out_b: bool
end
```

- **type**: The Entity type. Currently supports `sensor`, `actuator` or `hybrid`
- **topic**: The Topic in the Broker used by the Entity to send and receive
messages. Note that / should be substituted with .
(e.g: bedroom/aircondition -> bedroom.aircondition).
- **broker**: The name property of a previously defined Broker which the
Entity uses to communicate.
- **attributes**: Attributes have a name and a type. As can be seen in the above
example, HA-Auto supports int, float, string, bool, list and dictionary types.
Note that nested dictionaries are also supported.
- **description (Optional)**: A description of the Entity
- **freq (Optional)**: Used for Entities of type "**sensor**" to set the msg publishing rate

Notice that each Entity has it's own reference to a Broker, thus the metamodel
allows for communicating with Entities which are connected to different message
brokers. This allows for definining automation for multi-broker architectures.

Supported data types for Attributes:

- **int**: Integer numerical values
- **float**: Floating point numerical values
- **bool**: Boolean (true/false) values
- **str**: String values
- **time**: Time values (e.g. `01:25`)
- **list**: List / Array
- **dict**: Dictionary


## Visual Components

Below is the list of the currently supported Codin Components:

- Gauge
- LogsDisplay
- ValueDisplay
- AliveDisplay
- JsonViewer
- Plot
- PlotView
- Button
- ButtonGroup

### Gauge

Visualize entity attributes (or messages arriving at topics in general) using a gauge component.

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/2832ebe9-fe81-4845-876a-572769b031f8)


```
Gauge G1
    label: "MyGauge"
    entity: TempSensor1
    attribute: temp
    minValue: 0
    maxValue: 1
    leftColor: Red
    rightColor: Blue
    levels: 10
    hideTxt: false
    unit: "%"
    position:
        x: 0
        y: 0
        width: 10
        height: 10
end
```

### LogsDisplay

Use this component to monitor entity attributes (or messages arriving at topics in general) formatted as logs.

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/51c5b286-858e-4949-9c4c-e3881a11ee4c)


```
LogsDisplay LD1
    label: "MyLogsDisplay"
    entity: Logs
    attribute: msg
    position:
        x: 40
        y: 40
        width: 10
        height: 10
end
```

### ValueDisplay

Use this component to monitor an entity attribute (or a message property in general).

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/b2826070-2182-451e-86d2-c32f1c6f429e)


```
ValueDisplay VD1
    label: "MyValueDisplay"
    entity: TempSensor1
    attribute: temp
    unit: "%"
    position:
        x: 10
        y: 10
        width: 10
        height: 10
end
```

### AliveDisplay

Use this component to monitor activeness of entities (or topics in general).

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/0db32a0b-eefe-414b-8b17-a6bc41ef46b0)


```
AliveDisplay AV1
    label: "MyAliveDisplay"
    entity: TempSensor1
    timeout: 60
    position:
        x: 30
        y: 30
        width: 10
        height: 10
end
```

### JsonViewer

This component is used to visualize json-formatted entity attributes (or messages arriving at topics in general).

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/77d64d85-be41-4901-80b3-9012d05348c4)


```
JsonViewer JV1
    label: "MyJsonViewer"
    entity: TempSensor1
    position:
        x: 20
        y: 20
        width: 10
        height: 10
end
```

### Plot

Adds Plot definitions into a PlotView container for visualization of entity attributes (or messages arriving at topics in general).

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/5a568a61-542b-400a-9f21-e799236cfa58)

Below is the list of **Plot** properties:
- label: The label of the plot
- ptype: The type of the plot. Select between `Line` and `Bar`.
- entity: The referenced entity
- attribute: The attribute of the entity to plot
- color: The color of the plot (red, blue, yellow, green, cyan)
- smooth (bool): Smooth the plot. This is a Codin functionality.

Below is the list of **PlotView** properties:
- label: The label of the plot
- plots: The list of plots to include
- position: The position on the canvas, defined using the `Placement` grammar.
- xAxis (bool): Enable/Disable x axis.
- yAxis (bool): Enable/Disable y axis.
- horizontalGrid (bool): Enable/Disable horizontal plot grid.
- verticalGrid (bool): Enable/Disable vertical plot grid.
- legend (bool): Show the legent
- legendPosition: Select between  topRight, topLeft, bottomRight, bottomLeft
- maxValues (int): Maximum values to show on the plot


The following examples shows the construction of a **PlotView** that includes three (3) **Plots**.

```
Entity EnvSensor_1
    type: sensor
    topic: 'bedroom.sensor.env'
    broker: CloudMQTT
    attributes:
        - temperature: float
        - humidity: float
        - gas: float
end

Plot HumidityPlot
    label: "Humidity"
    entity: EnvSensor_1
    ptype: Line
    attribute: humidity
end

Plot TemperaturePlot
    label: "Temperature"
    entity: EnvSensor_1
    ptype: Line
    attribute: temperature
    color: red
    smooth: False
end

Plot GasPlot
    label: "Gas"
    entity: EnvSensor_1
    ptype: Line
    attribute: gas
end

PlotView MyPlots
    label: "Env Sensor Plots"
    xAxis: True
    yAxis: True
    horizontalGrid: True
    verticalGrid: True
    legend: True
    maxValues: -1
    legendPosition: topRight
    plots:
        - HumidityPlot
        - TemperaturePlot
        - GasPlot
    position:
        x: 0
        y: 0
        width: 8
        height: 8
end
```

### Buttons

Buttons are used to allow manually sending commands to actuator entities from the Codin dashboard.
Commands practically change the state of the actuator, by setting the relevant attribute(s) of the entity.

![image](https://github.com/robotics-4-all/codintxt/assets/4770702/81f09b55-35c8-4b6a-9021-2852db387cd6)



```
Button Btn1
    label: "Button1"
    topic: "actuators.relay_1"
    broker: CloudMQTT
    payload:
        - state: int = 1
end

Button Btn2
    label: "Button2"
    topic: "actuators.relay_2"
    broker: CloudMQTT
    payload:
        - state: int = 1
end

ButtonGroup Btn_Group_A
    label: "Btn_Group_A"
    alignTxt: Center
    alignBtns: Horizontal
    buttons:
        - Btn1
        - Btn2
    position:
        x: 0
        y: 0
        width: 4
        height: 4
end
```

## General Rules and Enumerations

### Color

Valid color values for visual component properties are listed below.

```
Color:
    'Red'		|
    'red'		|
    'Blue'		|
    'blue'		|
	'Yellow'	|
	'yellow'	|
	'Green'     |
	'green'     |
	'Cyan'      |
	'cyan'
;
```

### Alignment

Valid alignment values for visual component properties are listed below.

```
AlignType:
    'Center'     |
    'Left'       |
    'Right'      |
    'Top'        |
    'Bottom'     |
    'Horizontal' |
    'Vertical'
;
```

### Placement

Used in visual components to define the position on the canvas, given `x`, `y`, `width` and `height` values.
The syntax (in textX) is shown below.

```
Placement:
    'x:' x=INT
    'y:' y=INT
    'width:' w=INT
    'height:' h=INT
;
```

For example, positioning of a PlotView component on the canvas of the dashboard is defined using the syntax below:

```
PlotView MyPlots
    label: "Env Sensor Plots"
    plots:
        - HumidityPlot
        - TemperaturePlot
        - GasPlot
    position:
        x: 0
        y: 0
        width: 8
        height: 8
end
```

# Installation

Build and run the docker image, using the `build.sh` and `start.sh` scripts.

This repository also includes a `docker-compose.yml` file for deploying with docker compose.

# Examples

Examples can be found in the [examples/](./examples) directory of this repository.
