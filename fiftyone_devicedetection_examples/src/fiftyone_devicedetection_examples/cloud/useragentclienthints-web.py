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

from flask.helpers import make_response
from fiftyone_devicedetection_cloud.devicedetection_cloud_pipelinebuilder import DeviceDetectionCloudPipelineBuilder
from fiftyone_pipeline_core.web import webevidence, set_response_header

# You need to create a resource key at https://configure.51degrees.com
# and paste it into the code, replacing !!YOUR_RESOURCE_KEY!! below.
# Alternatively, add a resource_key environment variable
import os
if "resource_key" in os.environ:
    resource_key = os.environ["resource_key"]
else:
    resource_key = "!!YOUR_RESOURCE_KEY!!"

if resource_key == "!!YOUR_RESOURCE_KEY!!":
    print("""
    You need to create a resource key at
    https://configure.51degrees.com and paste it into the code,
    'replacing !!YOUR_RESOURCE_KEY!!
    To include the properties used in this example, go to https://configure.51degrees.com/
    """)
else:

    # First create the device detection pipeline with the desired settings and include required UACH SetHeader properties which are in the following format 
    # SetHeader[Component name][Response header name]
    # e.g. for browser component properties to be set in Accept-CH response header use following property
    # SetHeaderBrowserAccept-CH

    pipeline = DeviceDetectionCloudPipelineBuilder({
        "resource_key": resource_key
    }).build()

    from flask import Flask, request

    app = Flask(__name__)

    # Helper function to get a property value if it exists and return 
    # the reason why if it doesn't

    def get_value_helper(flowdata, engine, property_key):

        engine_properties = getattr(flowdata, engine)

        try:
            property_value = getattr(engine_properties, property_key)

            if property_value.has_value():
                return property_value.value()
            else:
                return property_value.no_value_message()
        except:
            return "Not found in cloud"

    # Create a main route for the device detections

    @app.route('/')
    def server():

        # Create the flowdata object for the device detection
        
        flowdata = pipeline.create_flowdata()

        # Add any information from the request (headers, cookies and any other additional information)

        flowdata.evidence.add_from_dict(webevidence(request))

        # Process the flowdata

        flowdata.process()

        # Generate the HTML

        output = "<h2>User Agent Client Hints Example</h2>"

        output += """

        <p>
        By default, the user-agent, sec-ch-ua and sec-ch-ua-mobile HTTP headers
        are sent.
        <br />
        This means that on the first request, the server can determine the
        browser from sec-ch-ua while other details must be derived from the
        user-agent.
        <br />
        If the server determines that the browser supports client hints, then
        it may request additional client hints headers by setting the
        Accept-CH header in the response.
        <br />
        Select the <strong>Make second request</strong> button below,
        to use send another request to the server. This time, any
        additional client hints headers that have been requested
        will be included.
        </p>

        <button type="button" onclick="redirect()">Make second request</button>
        <script>

            // This script will run when button will be clicked and device detection request will again 
            // be sent to the server with all additional client hints that was requested in the previous
            // response by the server.
            // Following sequence will be followed.
            // 1. User will send the first request to the web server for detection.
            // 2. Web Server will return the properties in response based on the headers sent in the request. Along 
            // with the properties, it will also send a new header field Accept-CH in response indicating the additional
            // evidence it needs. It builds the new response header using SetHeader[Component name]Accept-CH properties 
            // where Component Name is the name of the component for which properties are required.
            // 3. When "Make second request" button will be clicked, device detection request will again 
            // be sent to the server with all additional client hints that was requested in the previous
            // response by the server.
            // 4. Web Server will return the properties based on the new User Agent CLient Hint headers 
            // being used as evidence.

            function redirect() {
                sessionStorage.reloadAfterPageLoad = true;
                window.location.reload(true);
                }

            window.onload = function () { 
                if ( sessionStorage.reloadAfterPageLoad ) {
                document.getElementById('description').innerHTML = "<p>The information shown below is determined using <strong>User Agent Client Hints</strong> that was sent in the request to obtain additional evidence. If no additional information appears then it may indicate an external problem such as <strong>User Agent Client Hints</strong> being disabled in your browser.</p>";
                sessionStorage.reloadAfterPageLoad = false;
                }
                else{
                document.getElementById('description').innerHTML = "<p>The following values are determined by sever-side device detection on the first request.</p>";
                }
            }

        </script>
        
        <div id="evidence">
            <strong></br>Evidence values used: </strong>
            <table>
                <tr>
                    <th>Key</th>
                    <th>Value</th>
                </tr>

        """
        evidences = pipeline.get_element("cloud").filter_evidence(flowdata)
        for key, value in evidences.items():
            if ("header.user-agent" in key or "header.sec-ch" in key):
                output += "<tr>"
                output += "<td>" + str(key) + "</td>"
                output += "<td>" + str(value) + "</td>"
                output += "</>"
        output += "</table>"
        output += "</div>"

        output += "<div id=description></div>"
        output += "<div id=\"content\">"
        output += "<strong>Detection results:</strong></br>"
        output += "<p>"
        output += "<b>Hardware Vendor:</b> " + str(get_value_helper(flowdata, "device", "hardwarevendor"))
        output += "<br />"
        output += "<b>Hardware Name:</b> " + str(get_value_helper(flowdata, "device", "hardwarename"))
        output += "<br />"
        output += "<b>Device Type:</b> " + str(get_value_helper(flowdata, "device", "devicetype"))
        output += "<br />"
        output += "<b>Platform Vendor:</b> " + str(get_value_helper(flowdata, "device", "platformvendor"))
        output += "<br />"
        output += "<b>Platform Name:</b> " + str(get_value_helper(flowdata, "device", "platformname"))
        output += "<br />"
        output += "<b>Platform Version:</b> " + str(get_value_helper(flowdata, "device", "platformversion"))
        output += "<br />"
        output += "<b>Browser Vendor:</b> " + str(get_value_helper(flowdata, "device", "browservendor"))
        output += "<br />"
        output += "<b>Browser Name:</b> " + str(get_value_helper(flowdata, "device", "browsername"))
        output += "<br />"
        output += "<b>Browser Version:</b> " + str(get_value_helper(flowdata, "device", "browserversion"))
        output += "<br /></div>"

        # Create a response variable and add response object

        response = make_response(output)

        # Some browsers require that extra HTTP headers are explicitly
        # requested. So set whatever headers are required by the browser in
        # order to return the evidence needed by the pipeline.
        # More info on this can be found at
        # https://51degrees.com/blog/user-agent-client-hints

        response = set_response_header(flowdata, response)

        return response
