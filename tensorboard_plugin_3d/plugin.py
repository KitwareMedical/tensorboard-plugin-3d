import os
import glob

import tensorflow as tf

import werkzeug
from werkzeug import exceptions, wrappers

from tensorboard.backend import http_util
from tensorboard.backend.event_processing import event_accumulator
from tensorboard.plugins import base_plugin

def decorate_headers(func):
    def wrapper(*args, **kwargs):
        headers = func(*args, **kwargs)
        headers.extend(TensorboardPlugin3D.headers)
        return headers
    return wrapper

exceptions.HTTPException.get_headers = decorate_headers(exceptions.HTTPException.get_headers)

_PLUGIN_DIRECTORY_PATH_PART = "/data/plugin/tensorboard_plugin_3d/"


class TensorboardPlugin3D(base_plugin.TBPlugin):
    """TensorBoard plugin for 3D rendering."""

    plugin_name = "tensorboard_plugin_3d"
    headers = [("X-Content-Type-Options", "nosniff")]

    def __init__(self, context):
        """Instantiates TensorboardPlugin3D.

        Args:
          context: A base_plugin.TBContext instance.
        """
        self._data_provider = context.data_provider
        self._logdir = context.logdir

    def get_plugin_apps(self):
        return {
            "/index.js": self._serve_static_file,
            "/index.html": self._serve_static_file,
            "/images": self._serve_image,
            "/tags": self._serve_tags,
        }

    @wrappers.Request.application
    def _serve_image(self, request):
        self._find_all_images()
        tag = request.args.get("tag")
        run = request.args.get("run")
        if tag and run:
            return self._select_images(request, run, tag)
        response = {'images': []}
        for eis in self._encoded_images:
            if (tf.compat.v1.executing_eagerly()):
                np_arr = tf.io.decode_image(eis).numpy()
                if np_arr.ndim == 4:
                    np_arr = np_arr[:,:,:,0]
                response['images'].append({'array': np_arr.tolist()})
            else:
                decoded = tf.io.decode_image(eis)
                np_arr = decoded.eval(session=tf.compat.v1.Session())
                if np_arr.ndim == 4:
                    np_arr = np_arr[:,:,:,0]
                response['images'].append({'array': np_arr.tolist()})
        return http_util.Respond(request, response, "application/json")

    @wrappers.Request.application
    def _serve_tags(self, request):
        """Serves run to tag info.

        Frontend clients can use the Multiplexer's run+tag structure to request data
        for a specific run+tag. Responds with a map of the form:
        {runName: [tagName, tagName, ...]}
        """
        run_info = {}
        events = sorted(glob.glob(os.path.join(self._logdir, '*')))
        for event in events:
            run = event.split('/')[-1]
            ea = event_accumulator.EventAccumulator(event)
            ea.Reload()
            run_info[run] = ea.Tags()['images']

        return http_util.Respond(request, run_info, "application/json")

    @wrappers.Request.application
    def _serve_static_file(self, request):
        """Returns a resource file from the static asset directory.

        Requests from the frontend have a path in this form:
        /data/plugin/tensorboard_plugin_3d/static/foo
        This serves the appropriate asset: ./static/foo.

        Checks the normpath to guard against path traversal attacks.
        """
        filename = os.path.basename(request.path)
        extension = os.path.splitext(filename)[1]
        if extension == '.html':
            mimetype = 'text/html'
        elif extension == '.css':
            mimetype = 'text/css'
        elif extension == '.js':
            mimetype = 'application/javascript'
        else:
            mimetype = 'application/octet-stream'
        filepath = os.path.join(os.path.dirname(__file__), 'static', filename)
        try:
            with open(filepath, 'rb') as infile:
                contents = infile.read()
        except IOError:
            raise exceptions.NotFound("404 Not Found")
        return werkzeug.Response(
            contents, content_type=mimetype, headers=TensorboardPlugin3D.headers
        )

    def _find_all_images(self):
        self._images = {}
        self._encoded_images = []
        events = sorted(glob.glob(os.path.join(self._logdir, '*')))
        for event in events:
            run = event.split('/')[-1]
            self._images[run] = {}
            ea = event_accumulator.EventAccumulator(event)
            ea.Reload()
            tags = ea.Tags()['images']
            for tag in tags:
                self._images[run][tag] = [img for img in ea.Images(tag)]
                self._encoded_images.extend(
                    [img.encoded_image_string for img in ea.Images(tag)])
        return len(self._encoded_images)

    def is_active(self):
        """Returns whether there is relevant data for the plugin to process.
        If there is no any pending run, hide the plugin
        """
        images_available = self._find_all_images()
        return images_available

    def frontend_metadata(self):
        return base_plugin.FrontendMetadata(
            es_module_path="/index.js",
            disable_reload=True,
            tab_name="Tensorboard 3D"
        )

    @wrappers.Request.application
    def _select_images(self, request, run, tag):
        """Given a tag and single run, return array of ImageEvents."""
        body = self._encoded_images[run][tag]
        return http_util.Respond(request, body, "application/json")
