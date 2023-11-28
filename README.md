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

- Gauge:
- LogsDisplay
- ValueDisplay
- AliveDisplay
- JsonViewer
- Plot
- PlotView
- Button
- ButtonGroup


## The Language

TODO

## Installation

TODO

## Examples

TODO
