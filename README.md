# codintxt
Codin Textual DSL

## Introduction

CodinTxt is a textual DSL for automating the development process for the
[Codin low-code platform](https://codin.issel.ee.auth.gr/).

Codin was engineered by the [ISSEL Laboratory](https://lab.issel.ee.auth.gr/)
to automate the development process of Dashboards for Cyber-Physical Systems.
It provides a Web UI for developing Dashboards using drag-and-drop of various
components for remote monitoring and control of devices, applications and
systems.

**Note**:
In order to connect from Codin to non-secure hosts (not SSL) follow the instructions from the image below.

![Codin SSL](https://cdn.discordapp.com/attachments/1174290357333266482/1179008567475458108/image.png?ex=6578384b&is=6565c34b&hm=be39efda5e048dc7a699188026549b8bce306a2a77f807616b37f9f48f85464b&)

**Note #2**: For the auto deployment to Codin you have to create a Token from your **Codin Profile Page** (see image below)

![Codin Token](https://media.discordapp.net/attachments/779427740826730516/1179011338480123975/image.png)

CodinTxt defines a Metamodel for the Codin Platform (thus it is
Platform-specific) and allows definition of Dashboards using textual semantics,
while it also provides an **M2T Transformation** for generating a Json that can
be imported in Codin.

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


## The Language

The grammar of the DSL is pretty simple.

A CodinTxt model includes:
- Metadata definition
- Broker Definition
- Visual components

The **Metadata** section must be top-level, before any other definitions. In the same way, **Broker** definitions follow, but before any **Visual Component** definition.

```
Metadata
    name: "MyCodinTxtModel"
    description: "My first CodinTxt model"
    author: "klpanagi"
    token: "CODIN_TOKEN_HERE"  // ** The Codin token **
end

Broker<MQTT> default_broker
    host: "emqx.auth.gr"
    port: 1883
    ssl: false
    webPath: "/mqtt"
    webPort: 8883
    auth:
        username: "BROKER_USERNAME"
        password: "BROKER_PASSWORD"
end

// Transformed from actuator Entity sn_temperature_1
JsonViewer sn_temperature_1Display
    label: "sn_temperature_1 Display"
    topic: "sensors.sn_temperature_1"
    broker: default_broker
    position:
        x: 0
        y: 0
        width: 4
        height: 4
end
...
```

### Gauge

```
Gauge G1
    label: "MyGauge"
    topic: "sensors.humidity"
    broker: BrokerA
    attribute: "humidity"
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

```
LogsDisplay RTMonitorLogs
    label: "RTMonitor Logs"
    topic: "smauto.o3iYD.logs"
    broker: default_broker
    attribute: "msg"
    position:
        x: 0
        y: 4
        width: 8
        height: 4
end
```

### ValueDisplay

```
ValueDisplay VD1
    label: "MyValueDisplay"
    topic: "sensors.humidity"
    broker: BrokerA
    attribute: "humidity"
    unit: "%"
    position:
        x: 10
        y: 10
        width: 10
        height: 10
end
```

### AliveDisplay

```
AliveDisplay AV1
    label: "MyAliveDisplay"
    topic: "sensors.humidity"
    broker: BrokerA
    timeout: 60
    position:
        x: 30
        y: 30
        width: 10
        height: 10
end
```

### JsonViewer

```
JsonViewer RTMonitorEvents
    label: "RTMonitor Events"
    topic: "smauto.o3iYD.event"
    broker: default_broker
    position:
        x: 8
        y: 4
        width: 4
        height: 4
end
```

### Plot

```
Plot HumidityPlot
    label: "Humidity"
    topic: "bedroom.humidity"
    broker: CloudMQTT
    ptype: Line
    attribute: "humidity"
end

PlotView MyPlots
    label: "Env Sensor Plots"
    plots:
        - HumidityPlot
    position:
        x: 0
        y: 0
        width: 8
        height: 8
end
```

### Buttons

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


## Installation

Build and run the docker image, using the `build.sh` and `start.sh` scripts.

This repository also includes a `docker-compose.yml` file for deploying with docker compose.

## Examples

TODO.