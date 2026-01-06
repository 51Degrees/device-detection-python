# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2026 51 Degrees Mobile Experts Limited, Davidson House,
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

import inspect
import json5
from pathlib import Path
import unittest
from fiftyone_devicedetection_examples.cloud.nativemodellookup_console import NativeModelLookupConsole
from fiftyone_devicedetection_examples.cloud.taclookup_console import TacLookupConsole
from fiftyone_devicedetection_examples.cloud.metadata_console import MetaDataConsole
from fiftyone_pipeline_core.logger import Logger
from fiftyone_devicedetection_examples.example_utils import ExampleUtils
from fiftyone_devicedetection_examples.cloud.gettingstarted_console import GettingStartedConsole
from fiftyone_devicedetection_examples.cloud.configurator_console import ConfiguratorConsole

class DeviceDetectionExampleTests(unittest.TestCase):

    # Init method - specify Resource Key to run examples here or 
    # set a Resource Key in an environment variable called 'resource_key'.
    def setUp(self):
        self.resource_key = ExampleUtils.get_resource_key()
        self.logger = Logger()

        if not self.resource_key:
            self.fail(
                "ResourceKey must be specified in the setUp method" +
                " or as an Environment variable")

    def test_cloud_getting_started_console(self):
        example = GettingStartedConsole()
        configFile = Path(inspect.getfile(example.__class__)).parent.resolve().joinpath("gettingstarted_console.json").read_text()
        config = json5.loads(configFile)
        ExampleUtils.set_resource_key_in_config(config, self.resource_key)
        example.run(config, self.logger, print)
    def test_cloud_nativemodellookup_console(self):
        example = NativeModelLookupConsole()
        example.run(self.resource_key, self.logger, print)
    def test_cloud_taclookup_console(self):
        example = TacLookupConsole()
        configFile = Path(inspect.getfile(example.__class__)).parent.resolve().joinpath("taclookup_console.json").read_text()
        config = json5.loads(configFile)
        ExampleUtils.set_resource_key_in_config(config, self.resource_key)
        example.run(config, self.logger, print)
    def test_cloud_metadata_console(self):
        example = MetaDataConsole()
        example.run(self.resource_key, self.logger, print)
    def test_cloud_configurator_console(self):
        example = ConfiguratorConsole()
        example.run(self.resource_key, self.logger, print)