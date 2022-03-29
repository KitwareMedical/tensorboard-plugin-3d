# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests the TensorBoard images plugin."""


import collections.abc
import json

from pathlib import Path
import tensorflow as tf
from werkzeug import test as werkzeug_test
from werkzeug import wrappers

from tensorboard.backend import application
from tensorboard.backend.event_processing import data_provider
from tensorboard.backend.event_processing import (
    plugin_event_multiplexer as event_multiplexer,
)
from tensorboard.plugins import base_plugin
from tensorboard_plugin_3d import plugin as tb_3d_plugin
from tensorflow.python.framework import test_util

tf.compat.v1.disable_v2_behavior()


@test_util.run_all_in_graph_and_eager_modes
class TensorBoard3DPluginTest(tf.test.TestCase):
    def setUp(self):
        super().setUp()
        logdir, multiplexer = self._gather_data()
        provider = data_provider.MultiplexerDataProvider(multiplexer, logdir)
        ctx = base_plugin.TBContext(logdir=logdir, data_provider=provider)
        self.plugin = tb_3d_plugin.TensorBoardPlugin3D(ctx)
        wsgi_app = application.TensorBoardWSGI([self.plugin])
        self.server = werkzeug_test.Client(wsgi_app, wrappers.Response)
        self.routes = self.plugin.get_plugin_apps()

    def _gather_data(self):
        """Point to data on disk, returning `(logdir, multiplexer)`."""
        self.log_dir = Path('./data')

        # Start a server with the plugin.
        multiplexer = event_multiplexer.EventMultiplexer(
            {
                "image_and_label": f'{self.log_dir}/image_and_label',
                "image_only": f'{self.log_dir}/image_only',
            }
        )
        multiplexer.Reload()
        return self.log_dir, multiplexer

    def testServeFrontend(self):
        serve_static_file = self.plugin._serve_static_file
        client = werkzeug_test.Client(serve_static_file, wrappers.Response)
        response = client.get('/data/plugin/tensorboard_plugin_3d/static/index.js')
        self.assertEqual(200, response.status_code)

    def testPluginVisibility(self):
        visible = self.plugin.is_active()
        self.assertTrue(visible)

    def _DeserializeResponse(self, byte_content):
        """Deserializes byte content that is a JSON encoding.

        Args:
          byte_content: The byte content of a response.

        Returns:
          The deserialized python object decoded from JSON.
        """
        return json.loads(byte_content.decode("utf-8"))

    def testRoutesProvided(self):
        """Tests that the plugin offers the correct routes."""
        self.assertIsInstance(self.routes["/index.js"], collections.abc.Callable)
        self.assertIsInstance(self.routes["/index.html"], collections.abc.Callable)
        self.assertIsInstance(self.routes["/images/current"], collections.abc.Callable)
        self.assertIsInstance(self.routes["/images/count"], collections.abc.Callable)
        self.assertIsInstance(self.routes["/tags"], collections.abc.Callable)
        self.assertIsInstance(self.routes["/saveState"], collections.abc.Callable)
        self.assertIsInstance(self.routes["/fetchState"], collections.abc.Callable)


    def testNewStyleImagesRouteEager(self):
        """Tests that the /images routes returns correct data."""
        self.plugin.is_active()
        response = self.server.get("/data/plugin/tensorboard_plugin_3d/images/current")
        self.assertEqual(200, response.status_code)

        # Verify that the correct entries are returned.
        entries = self._DeserializeResponse(response.get_data())
        self.assertEqual(sorted(list(entries.keys())), ['image', 'label'])

    def testRunsRoute(self):
        """Tests that the /runs route offers the correct run to tag mapping."""
        response = self.server.get("/data/plugin/tensorboard_plugin_3d/tags")
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {
                'image_and_label': ['image_HWD/image', 'label_HWD/image'],
                'image_only': ['image_HWD/image']
            },
            self._DeserializeResponse(response.get_data()),
        )

    def testImagesCount(self):
        self.plugin.is_active()
        response = self.server.get("/data/plugin/tensorboard_plugin_3d/images/count")
        self.assertEqual(200, response.status_code)
        count = self._DeserializeResponse(response.get_data())
        self.assertEqual(count['current'], 1)
        self.assertEqual(count['total'], 2)

    def testStateSaveAndFetch(self):
        self.plugin.is_active()
        test_state = {
            'annotationsEnabled': True,
            'axesEnabled': False,
            'actorContext': {
                'blendMode': 'composite',
                'volumeSampleDistance': 0.2
            }
        }
        response = self.server.put(
            "/data/plugin/tensorboard_plugin_3d/saveState",
            data=json.dumps(test_state),
            headers={'Content-type': 'application/json'}
        )
        self.assertEqual(200, response.status_code)
        response = self.server.get("/data/plugin/tensorboard_plugin_3d/fetchState")
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(test_state, self._DeserializeResponse(response.get_data()))
        updates = {
            'annotationsEnabled': False,
            'actorContext': {
                'blendMode': 'maximum',
            }
        }
        response = self.server.put(
            "/data/plugin/tensorboard_plugin_3d/saveState",
            data=json.dumps(updates),
            headers={'Content-type': 'application/json'}
        )
        self.assertEqual(200, response.status_code)
        response = self.server.get("/data/plugin/tensorboard_plugin_3d/fetchState")
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {
                'annotationsEnabled': False,
                'axesEnabled': False,
                'actorContext': {
                    'blendMode': 'maximum',
                    'volumeSampleDistance': 0.2
                }
            },
            self._DeserializeResponse(response.get_data())
        )




if __name__ == "__main__":
    tf.test.main()
