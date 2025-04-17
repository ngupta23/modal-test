import os

from modal import App, Image, Secret, asgi_app

from modal_test.app import create_app

APP_NAME = "fastapi-hello-app"

"""
NOTES:
    - add_local_dir: copies local dir to remote
    - add_local_file: copies local file to remote
    - when using uv and uv sync, we need to add the modal_test to the image
      since uv sync will look for this folder.
    - alternately, if you are not using uv sync and instead using pip install
      with requirements.txt, you do not need to add this.
"""

image = (
    Image.debian_slim(python_version="3.10")
    .add_local_dir("modal_test", "/root/modal_test", copy=True)
    .add_local_file("pyproject.toml", "/root/pyproject.toml", copy=True)
    .add_local_file("uv.lock", "/root/uv.lock", copy=True)
    .pip_install("uv")
    .run_commands("cd /root && uv sync --frozen")  # runs shell commands
)

app = App(APP_NAME, image=image)


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
