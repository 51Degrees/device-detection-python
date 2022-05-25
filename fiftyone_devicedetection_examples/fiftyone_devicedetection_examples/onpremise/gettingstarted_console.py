# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2022 51 Degrees Mobile Experts Limited, Davidson House,
# Forbury Square, Reading, Berkshire, United Kingdom RG1 3EU.
#
# This Original Work is licensed under the European Union Public Licence
# (EUPL) v.1.2 and is subject to its terms as set out below.
#
# If a copy of the EUPL was not distributed with this file, You can obtain
# one at https://opensource.org/licenses/EUPL-1.2.
#
# The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
# amended by the European Commission) shall be deemed incompatible for
# the purposes of the Work and the provisions of the compatibility
# clause in Article 5 of the EUPL shall not apply.
# 
# If using the Work as, or as part of, a network application, by 
# including the attribution notice(s) required under Article 5 of the EUPL
# in the end user terms of the application under an appropriate heading, 
# such notice(s) shall fulfill the requirements of that article.
# ********************************************************************* 

## @example onpremise/gettingstarted_console.py
# 
# @include{doc} example-getting-started-onpremise.txt
# 
# This example is available in full on [GitHub](https://github.com/51Degrees/device-detection-python/blob/master/fiftyone_devicedetection_examples/fiftyone_devicedetection_examples/onpremise/gettingstarted_console.py). 
# 
# @include{doc} example-require-datafile.txt
# 
# Required PyPi Dependencies:
# - fiftyone_devicedetection
# 

import sys
from fiftyone_devicedetection.devicedetection_pipelinebuilder import DeviceDetectionPipelineBuilder
from fiftyone_devicedetection_examples.example_utils import ExampleUtils
from fiftyone_pipeline_core.logger import Logger

# In this example, by default, the 51degrees "Lite" file needs to be
# somewhere in the project space, or you may specify another file as
# a command line parameter.
#
# Note that the Lite data file is only used for illustration, and has
# limited accuracy and capabilities.
# Find out about the Enterprise data file on our pricing page:
# https://51degrees.com/pricing
LITE_V_4_1_HASH = "51Degrees-LiteV4.1.hash"

class GettingStartedConsole():
    def run(self, data_file, logger, output):

        # In this example, we use the DeviceDetectionPipelineBuilder
        # and configure it in code. For more information about
        # pipelines in general see the documentation at
        # http://51degrees.com/documentation/4.3/_concepts__configuration__builders__index.html
        pipeline = DeviceDetectionPipelineBuilder(
            data_file_path = data_file,
            # We use the low memory profile as its performance is
            # sufficient for this example. See the documentation for
            # more detail on this and other configuration options:
            # http://51degrees.com/documentation/4.3/_device_detection__features__performance_options.html
            # http://51degrees.com/documentation/4.3/_features__automatic_datafile_updates.html
            # http://51degrees.com/documentation/4.3/_features__usage_sharing.html
            performance_profile = "LowMemory",
            # inhibit sharing usage for this test, usually this
            # should be set "true"
            usage_sharing = False,
            # Inhibit auto-update of the data file for this example
            auto_update = False,
            licence_keys = "").add_logger(logger).build()

        ExampleUtils.check_data_file(pipeline, logger);

        # carry out some sample detections
        for values in self.EvidenceValues:
            self.analyseEvidence(values, pipeline, output)

    def analyseEvidence(self, evidence, pipeline, output):

        # FlowData is a data structure that is used to convey
        # information required for detection and the results of the
        # detection through the pipeline.
        # Information required for detection is called "evidence"
        # and usually consists of a number of HTTP Header field
        # values, in this case represented by a dictionary of header
        # name/value entries.
        data = pipeline.create_flowdata()
        
        message = []

        # List the evidence
        message.append("Input values:\n")
        for key in evidence:
            message.append(f"\t{key}: {evidence[key]}\n")
        
        output("".join(message))

        # Add the evidence values to the flow data
        data.evidence.add_from_dict(evidence)

        # Process the flow data.
        data.process()

        message = []
        message.append("Results:\n")

        # Now that it's been processed, the flow data will have
        # been populated with the result. In this case, we want
        # information about the device, which we can get by
        # asking for a result matching named "device"
        device = data.device

        # Display the results of the detection, which are called
        # device properties. See the property dictionary at
        # https://51degrees.com/developers/property-dictionary
        # for details of all available properties.
        self.outputValue("Mobile Device", device.ismobile, message)
        self.outputValue("Platform Name", device.platformname, message)
        self.outputValue("Platform Version", device.platformversion, message)
        self.outputValue("Browser Name", device.browsername, message)
        self.outputValue("Browser Version", device.browserversion, message)
        output("".join(message))

    def outputValue(self, name, value, message):
        # Individual result values have a wrapper called
        # `AspectPropertyValue`. This functions similarly to
        # a null-able type.
        # If the value has not been set then trying to access the
        # `value` method will throw an exception.
        # `AspectPropertyValue` also includes the `no_value_message`
        # method, which describes why the value has not been set.
        message.append(
            f"\t{name}: {value.value()}\n" if value.has_value()
            else f"\t{name}: {value.no_value_message()}\n")


    # This collection contains the various input values that will 
    # be passed to the device detection algorithm.
    EvidenceValues = [
        # A User-Agent from a mobile device.
        { "header.user-agent":
            "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960U) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "SamsungBrowser/10.1 Chrome/71.0.3578.99 Mobile Safari/537.36" },
        # A User-Agent from a desktop device.
        { "header.user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/78.0.3904.108 Safari/537.36" },
        # Evidence values from a windows 11 device using a browser
        # that supports User-Agent Client Hints.
        { "header.user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/98.0.4758.102 Safari/537.36",
            "header.sec-ch-ua-mobile": "?0",
        "header.sec-ch-ua":
            "\" Not A; Brand\";v=\"99\", \"Chromium\";v=\"98\", "
            "\"Google Chrome\";v=\"98\"",
            "header.sec-ch-ua-platform": "\"Windows\"",
            "header.sec-ch-ua-platform-version": "\"14.0.0\"" }
    ]

def main(argv):
    # Use the supplied path for the data file or find the lite
    # file that is included in the repository.
    data_file = argv[0] if len(argv) > 0 else ExampleUtils.find_file(LITE_V_4_1_HASH)

    # Configure a logger to output to the console.
    logger = Logger(min_level="info")

    if (data_file != None):
        GettingStartedConsole().run(data_file, logger, print)
    else:
        logger.log("error",
            "Failed to find a device detection " +
            "data file. Make sure the device-detection-data " +
            "submodule has been updated by running " +
            "`git submodule update --recursive`.")

if __name__ == "__main__":
    main(sys.argv[1:])
