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
        headers.extend(TensorBoardPlugin3D.headers)
        return headers
    return wrapper

exceptions.HTTPException.get_headers = decorate_headers(exceptions.HTTPException.get_headers)


class TensorBoardPlugin3D(base_plugin.TBPlugin):
    """TensorBoard plugin for 3D rendering."""

    plugin_name = "tensorboard_plugin_3d"
    headers = [("X-Content-Type-Options", "nosniff")]

    def __init__(self, context):
        """Instantiates TensorBoardPlugin3D.

        Args:
          context: A base_plugin.TBContext instance.
        """
        self._data_provider = context.data_provider
        self._logdir = context.logdir
        self.current_run = 0
        self._client_state = {}
        self._all_runs = []

    def get_plugin_apps(self):
        """
        Returns a map of the available endpoints to their respective method.
        """
        return {
            "/index.js": self._serve_static_file,
            "/index.html": self._serve_static_file,
            "/images/current": self._serve_image,
            "/images/count": self._serve_image_count,
            "/tags": self._serve_tags,
            "/saveState": self._save_state,
            "/fetchState": self._serve_state,
        }

    @wrappers.Request.application
    def _serve_image_count(self, request):
        response = {
            'current': self.current_run + 1,
            'total': len(self._all_runs)
        }
        return http_util.Respond(request, response, "application/json")

    @wrappers.Request.application
    def _serve_image(self, request):
        """
        If the run and tag are provided return the associated image(s).
        Otherwise return the most recent image and its label if it has one.
        """
        self._find_all_images()
        tag = request.args.get("tag")
        run = request.args.get("run")
        idx = request.args.get("idx")
        if tag and run:
            eis_list = self._select_images(request, run, tag)
            data = {tag: eis_list}
        elif idx:
            data = self._find_next_images(idx)
        else:
            # Grab the first run (event file)
            data = self._find_next_images(1)

        response = {}
        for tag, images in data.items():
            # There could be more than one image with the latest tag.
            # Grab the most recent.
            eis = images[-1].encoded_image_string

            # Default is to run with eager execution but users still have the
            # option to select graph execution so we will handle that case also
            if (tf.compat.v1.executing_eagerly()):
                np_arr = tf.io.decode_image(eis).numpy()
            else:
                decoded = tf.io.decode_image(eis)
                np_arr = decoded.eval(session=tf.compat.v1.Session())
            if np_arr.ndim == 4:
                np_arr = np_arr[:,:,:,0]

            # Use the tag to determine if it is an image or label
            if tag.startswith('image'):
                response['image'] = np_arr.tolist()
            elif tag.startswith('label'):
                response[f'label'] = np_arr.tolist()
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
            tags = ea.Tags()['images']
            if tags:
                run_info[run] = tags
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
            contents, content_type=mimetype, headers=TensorBoardPlugin3D.headers
        )

    def _find_next_images(self, idx):
        self.current_run = (int(idx) - 1) % len(self._all_runs)
        run = self._all_runs[self.current_run]
        return self._all_images[run]

    def _find_all_images(self):
        """
        Find all available images. Return False if no images are found,
        otherwise return True.
        """
        self._all_images = {}
        images_found = False
        event_files = sorted(glob.glob(os.path.join(self._logdir, '*')))
        for event in event_files:
            run = event.split('/')[-1]
            ea = event_accumulator.EventAccumulator(event)
            ea.Reload()
            tags = ea.Tags()['images']
            for tag in tags:
                if ea.Images(tag):
                    self._all_images.setdefault(run, {})
                    self._all_images[run][tag] = ea.Images(tag)
                    if ea.Images(tag) and (
                        tag.startswith('image') or tag.startswith('label')):
                        images_found = True
        self._all_runs = list(self._all_images.keys())
        return images_found

    def is_active(self):
        """Returns whether there is relevant data for the plugin to process.
        If there is no pending run, hide the plugin
        """
        images_available = self._find_all_images()
        return images_available

    def frontend_metadata(self):
        return base_plugin.FrontendMetadata(
            es_module_path="/index.js",
            disable_reload=True,
            tab_name="TensorBoard 3D"
        )

    @wrappers.Request.application
    def _select_images(self, run, tag):
        """Given a tag and single run, return the associated image(s)."""
        return self._all_images[run][tag]

    @wrappers.Request.application
    def _save_state(self, request):
        def parse_state(input, output):
            for key, value in input.items():
                if key == 'actorContext':
                    output.setdefault('actorContext', {})
                    parse_state(value, output['actorContext'])
                else:
                    output[key] = value
        parse_state(request.get_json(), self._client_state)
        return http_util.Respond(request, self._client_state, "application/json")

    @wrappers.Request.application
    def _serve_state(self, request):
        return http_util.Respond(request, self._client_state, "application/json")
