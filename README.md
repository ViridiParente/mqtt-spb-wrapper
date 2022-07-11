# MQTT-SPB-WRAPPER

This python module implements a wrapper around the python Eclipse Tahu Sparkplug B v1.0 core modules, to easily create and handle MQTT Sparkplug B entities in an easy way.

The *mqtt-spb-wrapper* python module includes the following object classes to handle generic Sparkplug B entities in an easy way:

- **MqttSpbEntityEdgeNode** - End of Network (EoN) entity that can publish NDATA, NBIRTH, NDEATH messages and subscribe to its own commands NCMD as well as to the STATUS messages from the SCADA application.

- **MqttSpbEntityDevice** - End of Network Device (EoND) entity that can publish DDATA, DBIRTH, DDEATH messages and subscribe to its own commands DCMD as well as to the STATUS messages from the SCADA application.

- **MqttSpbEntityApplication** - Application entity that can publish NDATA, NBIRTH, NDEATH messages and subscribe to its own commands NCMD, to the STATUS messages from the SCADA application as well as to all other messages from the Sparkplug B Domain ID.

- **MqttSpbEntityScada** - SCADA entity that can publish NDATA, NBIRTH, NDEATH messages as well as to send commands to all EoN and EoND (NCMD, DCMD), and subscribe to all other messages from the Sparkplug B Domain ID.

- **MqttSpbTopic** - Object to easily parse, decode and handle MQTT Sparkplug B topics.

  

## Examples

The repository includes a folder with some basic examples for the different type of entities, **see the folder /examples** in this repository for more examples.

### Basic EoN Device

The following code shows how to create an EoND entity that transmit some simple data.

```python
import time
from mqtt_spb_wrapper import *

_DEBUG = True  # Enable debug messages

print("--- Sparkplug B example - End of Node Device - Simple")


def callback_command(payload):
    print("DEVICE received CMD: %s" % (payload))


def callback_message(topic, payload):
    print("Received MESSAGE: %s - %s" % (topic, payload))


# Create the spB entity object
domain_name = "Domain-001"
edge_node_name = "Gateway-001"
device_name = "SimpleEoND-01"

device = MqttSpbEntityDevice(domain_name, edge_node_name, device_name, _DEBUG)

device.on_message = callback_message  # Received messages
device.on_command = callback_command  # Callback for received commands

# Set the device Attributes, Data and Commands that will be sent on the DBIRTH message --------------------------

# Attributes
device.attribures.set_value("description", "Simple EoN Device node")
device.attribures.set_value("type", "Simulated-EoND-device")
device.attribures.set_value("version", "0.01")

# Data / Telemetry
device.data.set_value("value", 0)

# Commands
device.commands.set_value("rebirth", False)

# Connect to the broker --------------------------------------------
# Upon connection, the BIRTH message will be sent and DEATH messages will be set
print("Connecting to broker...")
device.connect("localhost", 1883)

# Send some telemetry values ---------------------------------------
value = 0  # Simple counter
for i in range(5):
    # Update the data value
    device.data.set_value("value", value)

    # Send data values
    print("Sending data - value : %d" % value)
    device.publish_data()

    # Increase counter
    value += 1

    # Sleep some time
    time.sleep(5)

# Disconnect device -------------------------------------------------
# After disconnection the MQTT broker will send the entity DEATH message.
print("Disconnecting device")
device.disconnect()

print("Application finished !")
```



### Basic Listener Application

The following code shows how to create an application entity to listen to all Sparkplug B messages on a given group.

```python
import time
from mqtt_spb_wrapper import *

_DEBUG = True  # Enable debug messages

print("--- Sparkplug B example - Application Entity Listener")


def callback_app_message(topic, payload):
    print("APP received MESSAGE: %s - %s" % (topic, payload))


def callback_app_command(payload):
    print("APP received CMD: %s" % (payload))


domain_name = "Domain-001"
app_entity_name = "ListenApp01"

app = MqttSpbEntityApplication(domain_name, app_entity_name, debug_info=_DEBUG)

# Set callbacks
app.on_message = callback_app_message
app.on_command = callback_app_command

# Set the device Attributes, Data and Commands that will be sent on the DBIRTH message --------------------------

# Attributes
app.attribures.set_value("description", "Test application")

# Commands
app.commands.set_value("rebirth", False)

# Connect to the broker----------------------------------------------------------------
# Upon connection, the BIRTH message will be sent and DEATH messages will be set
print("Connecting to broker...")
app.connect("localhost", 1883)

# Loop forever, messages and commands will be handeled by the callbacks
while True:
    time.sleep(1000)
```



## Eclipse Sparkplug B v1.0

Sparkplug is a specification for MQTT enabled devices and applications to send and receive messages in a stateful way. While MQTT is stateful by nature it doesn't ensure that all data on a receiving MQTT application is current or valid. Sparkplug provides a mechanism for ensuring that remote device or application data is current and valid. The main Sparkplug B features include:

- Complex data types using templates
- Datasets
- Richer metrics with the ability to add property metadata for each metric
- Metric alias support to maintain rich metric naming while keeping bandwidth usage to a minimum
- Historical data
- File data

Sparkplug B Specification: [https://www.eclipse.org/tahu/spec/Sparkplug%20Topic%20Namespace%20and%20State%20ManagementV2.2-with%20appendix%20B%20format%20-%20Eclipse.pdf](https://www.eclipse.org/tahu/spec/Sparkplug Topic Namespace and State ManagementV2.2-with appendix B format - Eclipse.pdf)



## Eclipse Tahu spB v1.0 implementation

Eclipse Tahu provide client libraries and reference implementations in various languages and for various devices to show how the device/remote application must connect and disconnect from the MQTT server using the Sparkplug specification explained below.  This includes device lifecycle messages such as the required birth and last will & testament messages that must be sent to ensure the device lifecycle state and data integrity.

The *mqtt-spb-wrapper* python module uses the open source Sparkplug core function from Eclipse Tahu repository, located at: https://github.com/eclipse/tahu (The current release used is v0.5.15 ).

For more information visit : https://github.com/eclipse/tahu

