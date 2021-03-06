![51Degrees](https://51degrees.com/DesktopModules/FiftyOne/Distributor/Logo.ashx?utm_source=github&utm_medium=repository&utm_content=readme_main&utm_campaign=python-open-source "THE Fastest and Most Accurate Device Detection") **v4 Device Detection Python**

[Pipeline Documentation](https://51degrees.com/documentation/4.1/index.html "Complete documentation") | [Available Properties](https://51degrees.com/resources/property-dictionary?utm_source=github&utm_medium=repository&utm_content=property_dictionary&utm_campaign=python-open-source "View all available properties and values")

## Introduction
This project contains 51Degrees Device Detection engines that can be used with the Pipeline API.

The Pipeline is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines) 

## Requirements

* Python 2.7 or Python 3
* The `flask` python library to run the web examples

## Installation and Examples

### From PyPI

`pip install fiftyone_devicedetection`

You can confirm this is working with the following micro-example.

* Create a resource key for free with the 51Degrees [configurator](https://configure.51degrees.com/np5M4nlF). This defines the properties you want to access.
* On the 'implement' page of the configurator, copy the resource key and replace YOUR_RESOURCE_KEY in the example below. Save this as exampledd.py
* Run the example with `python exampledd.py`
* Feel free to try different user-agents and property values.

```
from fiftyone_devicedetection.devicedetection_pipelinebuilder import DeviceDetectionPipelineBuilder
pipeline = DeviceDetectionPipelineBuilder({"resourceKey": "YOUR_RESOURCE_KEY"}).build()
fd = pipeline.create_flowdata()
fd.evidence.add("header.user-agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148")
fd.process()
print(fd.device.ismobile.value())
```

For more in-depth examples, check out the [examples](https://51degrees.com/documentation/4.1/_examples__device_detection__index.html) page in the documentation.

### From GitHub

If you've cloned the GitHub repository, you will be able to run the examples directly:

`python3 -m examples.cloud.gettingstarted`

To run the web example:

#### Linux

Execute `export FLASK_APP=` with the name of the web example file, then `flask run`.

#### Windows

Execute `$env:FLASK_APP = "x"` with the name of the example file, then `flask run`.
