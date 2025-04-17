import os

from modal import App, Image, Secret, asgi_app

from modal_test.app import create_app

APP_NAME = "fastapi-hello-app"

"""
NOTES:

More info about images can be found here: https://modal.com/docs/guide/images

- add_local_dir: copies local dir to remote
- add_local_file: copies local file to remote
- Setting up the environment:
  - when using uv and uv sync, we need to add the modal_test to the image
    since uv sync will look for this folder.
  - alternately, if you are not using uv sync and instead using pip install
    with requirements.txt, you do not need to add this.
- run_commands: runs shell commands
"""

image = (
    Image.debian_slim(python_version="3.10")
    .add_local_dir("modal_test", "/root/modal_test", copy=True)
    .add_local_file("pyproject.toml", "/root/pyproject.toml", copy=True)
    .add_local_file("uv.lock", "/root/uv.lock", copy=True)
    .pip_install("uv")
    .run_commands("cd /root && uv sync --frozen")
)

app = App(APP_NAME, image=image)

"""
NOTES:

More information about auto-scaling can be found here:
https://modal.com/docs/guide/scale#configuring-autoscaling-behavior

- `max_containers`: The upper limit on containers for the specific Function.
- `min_containers`:
      The minimum number of containers that should be kept warm, even when the
      Function is inactive.
- `buffer_containers`:
      The size of the buffer to maintain while the Function is active, so that
      additional inputs will not need to queue for a new container.
- `scaledown_window`:
      The maximum duration (in seconds) that individual containers can remain
      idle when scaling down.

Using Secrets: https://modal.com/docs/guide/secrets

Using Volumes: https://modal.com/docs/guide/volumes
"""


@app.function(
    image=image,
    cpu=1,
    min_containers=1,
    secrets=[Secret.from_name("custom-secret")],
    allow_concurrent_inputs=2,
)
@asgi_app()
def fastapi_app():
    app = create_app(name=os.environ["NAME"])

    return app
