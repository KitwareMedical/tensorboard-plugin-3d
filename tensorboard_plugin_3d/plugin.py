import mimetypes
import os
import glob

import tensorflow as tf

import werkzeug
from werkzeug import exceptions, wrappers

from tensorboard import errors
from tensorboard import plugin_util
from tensorboard.backend import http_util
from tensorboard.backend.event_processing import event_accumulator
from tensorboard.data import provider
from tensorboard.plugins import base_plugin
from tensorboard.plugins.scalar import metadata

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
        """Instantiates ExampleRawScalarsPlugin.

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
        response = {'images': []}
        for eis in self._images:
            np_arr = tf.io.decode_image(eis).numpy()
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
        ctx = plugin_util.context(request.environ)
        experiment = plugin_util.experiment_id(request.environ)
        run_tag_mapping = self._data_provider.list_scalars(
            ctx,
            experiment_id=experiment,
            plugin_name=metadata.PLUGIN_NAME,
        )
        run_info = {run: list(tags) for (run, tags) in run_tag_mapping.items()}

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
        self._images = []
        events = sorted(glob.glob(os.path.join(self._logdir, '*')))
        for event in events:
            ea = event_accumulator.EventAccumulator(event)
            ea.Reload()
            tags = ea.Tags()['images']
            for tag in tags:
                for image in ea.Images(tag):
                    self._images.append(image.encoded_image_string)
        return len(self._images)

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

    def scalars_impl(self, ctx, experiment, tag, run):
        """Returns scalar data for the specified tag and run.

        For details on how to use tags and runs, see
        https://github.com/tensorflow/tensorboard#tags-giving-names-to-data

        Args:
          tag: string
          run: string

        Returns:
          A list of ScalarEvents - tuples containing 3 numbers describing entries in
          the data series.

        Raises:
          NotFoundError if there are no scalars data for provided `run` and
          `tag`.
        """
        all_scalars = self._data_provider.read_scalars(
            ctx,
            experiment_id=experiment,
            plugin_name=metadata.PLUGIN_NAME,
            downsample=5000,
            run_tag_filter=provider.RunTagFilter(runs=[run], tags=[tag]),
        )
        scalars = all_scalars.get(run, {}).get(tag, None)
        if scalars is None:
            raise errors.NotFoundError(
                "No scalar data for run=%r, tag=%r" % (run, tag)
            )
        return [(x.wall_time, x.step, x.value) for x in scalars]

    @wrappers.Request.application
    def scalars_route(self, request):
        """Given a tag and single run, return array of ScalarEvents."""
        tag = request.args.get("tag")
        run = request.args.get("run")
        ctx = plugin_util.context(request.environ)
        experiment = plugin_util.experiment_id(request.environ)
        body = self.scalars_impl(ctx, experiment, tag, run)
        return http_util.Respond(request, body, "application/json")
