# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2025 51 Degrees Mobile Experts Limited, Davidson House,
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


## @example cloud/gettingstarted_web/app.py
#
# @include{doc} example-getting-started-web.txt
# 
# This example is available in full on [GitHub](https://github.com/51Degrees/device-detection-python/blob/main/fiftyone_devicedetection_examples/src/fiftyone_devicedetection_examples/cloud/gettingstarted_web/app.py). 
# 
# @include{doc} example-require-resourcekey.txt
# 
# Required PyPi Dependencies:
# - [fiftyone-devicedetection](https://pypi.org/project/fiftyone-devicedetection/)
# - flask
# 
# ## Overview
# 
# The `DeviceDetectionPipelineBuilder` class is used to create a Pipeline instance from the configuration
# that is supplied.
# The fiftyone_pipeline_core.web module contains helpers which deal with
# automatically populating evidence from a web request.
# ```{py}
# flowdata.evidence.add_from_dict(webevidence(request))
# ```

# The module can also handling setting response headers (e.g. Accept-CH for User-Agent 
# Client Hints) and serving requests for client-side JavaScript and JSON resources.
# ```{py}
# set_response_header(flowdata, response)
# ```
# 
# The results of detection can be accessed by through the flowdata object once
# processed. This can then be used to interrogate the data.
# ```{py}
# flowdata.process()
# device = flowdata.device
# hardware_vendor = device.hardwarevendor
# ```
# 
# Results can also be accessed in client-side code by using the `fod` object. See the 
# [JavaScriptBuilderElementBuilder](https://51degrees.com/pipeline-python/4.3/classpipeline-python_1_1fiftyone__pipeline__core_1_1fiftyone__pipeline__core_1_1javascriptbuilde778a9036818b19ab55d981a40be4a4d7.html)
# for details on available settings such as changing the `fod` name.
# ```{js}
# window.onload = function () {
#     fod.complete(function(data) {
#         var hardwareName = data.device.hardwarename;
#         alert(hardwareName.join(", "));
#     }
# }
# ```
#
# ## View
# @include templates/index.html
#
# ## App

from fiftyone_devicedetection_examples.example_utils import ExampleUtils
from flask import Flask, request, render_template
from flask.helpers import make_response
from fiftyone_devicedetection.devicedetection_pipelinebuilder import DeviceDetectionPipelineBuilder
from fiftyone_pipeline_core.logger import Logger
from fiftyone_pipeline_core.web import webevidence, set_response_header
import json
import sys

class GettingStartedWeb():
    app = Flask(__name__)

    def build(self, resource_key, logger):
        # Here we add some callback settings for the page to make a request with extra evidence from the client side, in this case the Flask /json route we will make below

        javascript_builder_settings = {
            "endpoint": "/json",
            "minify": True,
            # The enable_cookies setting is needed if you want to work with results from client-side
            # evidence on the server. For example, precise Apple models or screen dimensions.
            # This will store the results of client-side detection scripts on the client as cookies.
            # On subsequent requests, these cookies will be included in the payload and will be 
            # used by the device detection API when it runs.
            "enable_cookies": True
        }
        GettingStartedWeb.pipeline = DeviceDetectionPipelineBuilder(
            resource_key = resource_key, 
            javascript_builder_settings = javascript_builder_settings).add_logger(logger).build()
        
        return self

    def run(self):

        GettingStartedWeb.app.run()

    # First we make a JSON route that will be called from the client side and will return
    # a JSON encoded property database using any additional evidence provided by the client 

    @staticmethod
    @app.route('/json', methods=['POST'])
    def jsonroute():

        # Create the flowdata object for the JSON route
        flowdata = GettingStartedWeb.pipeline.create_flowdata()

        # Add any information from the request (headers, cookies and additional 
        # client side provided information)

        flowdata.evidence.add_from_dict(webevidence(request))

        # Process the flowdata

        flowdata.process()

        # Return the JSON from the JSONBundler engine

        return json.dumps(flowdata.jsonbundler.json)

    # In the main route we dynamically update the screen's device property display
    # using the above JSON route

    @staticmethod
    @app.route('/')
    def server():

        # Create the flowdata object for the JSON route
        flowdata = GettingStartedWeb.pipeline.create_flowdata()

        # Add any information from the request (headers, cookies and additional 
        # client side provided information)

        flowdata.evidence.add_from_dict(webevidence(request))

        # Process the flowdata

        flowdata.process()

        response = make_response()

        # Some browsers require that extra HTTP headers are explicitly
        # requested. So set whatever headers are required by the browser in
        # order to return the evidence needed by the pipeline.
        # More info on this can be found at
        # https://51degrees.com/blog/user-agent-client-hints

        set_response_header(flowdata, response)

        # Generate the HTML
        response.set_data(render_template(
            'index.html',
            data=flowdata,
            utils=ExampleUtils,
            response=response))

        return response

def main(argv):
    # Use the command line args to get the resource key if present.
    # Otherwise, get it from the environment variable.
    resource_key = argv[0] if len(argv) > 0 else ExampleUtils.get_resource_key() 
    
    # Configure a logger to output to the console.
    logger = Logger(min_level="info")

    if (resource_key):
        GettingStartedWeb().build(resource_key, logger).run()

    else:
        logger.log("error",
            "No resource key specified in environment variable " +
            f"'{ExampleUtils.RESOURCE_KEY_ENV_VAR}'. The 51Degrees " +
            "cloud service is accessed using a 'ResourceKey'. " +
            "For more detail see " +
            "https://51degrees.com/documentation/4.4/_info__resource_keys.html. " +
            "A resource key with the properties required by this " +
            "example can be created for free at " +
            "https://configure.51degrees.com/g3gMZdPY. " +
            "Once complete, populated the environment variable " +
            "mentioned at the start of this message with the key.")

if __name__ == "__main__":
    main(sys.argv[1:])
