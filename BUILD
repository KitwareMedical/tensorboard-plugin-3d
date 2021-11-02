# Description:
# TensorBoard example plugin

# This plugin is not primarily built with Bazel (intentionally, to
# demonstrate that Bazel is not required); we use this BUILD file only
# to define integration tests for TensorBoard itself.

package(default_visibility = ["//tensorboard:internal"])

licenses(["notice"])

sh_test(
    name = "smoke_test",
    size = "large",
    timeout = "moderate",
    srcs = ["smoke_test.sh"],
    # Don't just `glob(["**"])` because `setup.py` creates artifacts
    # like wheels and a `tensorboard_plugin_example_raw_scalars.egg-info`
    # directory, and we want to make sure that those don't interfere with the
    # test.
    data = [
        "setup.py",
        "//tensorboard/pip_package",
    ] + glob([
        "tensorboard_plugin_example_raw_scalars/*.py",
        "tensorboard_plugin_example_raw_scalars/static/**",
    ]),
    tags = [
        "manual",  # https://github.com/tensorflow/tensorboard/issues/2987
    ],
)

py_test(
    name = "unit_test",
    size = "small",
    srcs = [
        "test.py",
    ],
    main = "test.py",
    srcs_version = "PY3",
    tags = ["support_notf"],
    deps = [
        "//tensorboard",
    ],
)
