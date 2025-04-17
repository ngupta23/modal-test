[![lint](https://github.com/ngupta23/modal_test/actions/workflows/lint.yaml/badge.svg)](https://github.com/ngupta23/modal_test/actions/workflows/lint.yaml)
[![CI](https://github.com/ngupta23/modal_test/actions/workflows/ci.yaml/badge.svg)](https://github.com/ngupta23/modal_test/actions/workflows/ci.yaml)

# modal_test
A repo for testing modal

## 🛠️ Create the Development Environment & 🔧 Install Pre-commit Hooks

* Pre-commit hooks help maintain code quality by running checks before commits.
* Update the .pre-commit-config.yaml if needed, then run the following command
  * `make devenv`
  * This will do both of these steps - create the dev env and install pre-commit.

```bash
# Install uv
pip install uv

# Create and activate a virtual environment
uv venv --python 3.10
source .venv/bin/activate

# # Initialize uv. NOTE: The following may not have an impact since we are already
# # adding a custom project.toml to this repository
# uv init

make devenv
```

## 🔄 Update Dependencies

If you want to add or update dependencies, you can do so using the `uv` command. This will update the `pyproject.toml` file and the lock file.

```bash
# Update dependencies for production
uv add <prod_lib>

# To add to dev dependency group
# https://docs.astral.sh/uv/concepts/projects/dependencies/#development-dependencies
uv add --dev <dev_lib>

# update the lock file
uv lock
```

## Setup Modal

* Check out the [Getting started](https://modal.com/docs/guide) section on Modal.

```bash
# Install modal (already done)
# uv add modal

# Authenticate with modal
uv run modal setup
```

## Run on Modal

* More details can be found in the [Modal documentation](https://modal.com/docs/guide/apps).

### Ephemeral Apps

> An ephemeral App is created when you use the modal run CLI command, or the app.run method. This creates a temporary App that only exists for the duration of your script.

> Ephemeral Apps are stopped automatically when the calling program exits, or when the server detects that the client is no longer connected. You can use --detach in order to keep an ephemeral App running even after the client exits.

```bash
# Runs ephemeral app remotely on modal
uv run modal run modal_test/ephemeral.py --num 10
```

#### Entrypoints for ephemeral Apps

> The code that runs first when you modal run an App is called the “entrypoint”.

> You can register a local entrypoint using the @app.local_entrypoint() decorator. You can also use a regular Modal function as an entrypoint, in which case only the code in global scope is executed locally.

#### Manually specifying an entrypoint

> If there is only one `local_entrypoint` registered, `modal run script.py` will automatically use it. If you have no entrypoint specified, and just one decorated Modal function, that will be used as a remote entrypoint instead. Otherwise, you can direct `modal run` to use a specific entrypoint.

For example, if you have a function decorated with `@app.function()` in your file:

```python
# script.py

@app.function()
def f():
    print("Hello world!")


@app.function()
def g():
    print("Goodbye world!")


@app.local_entrypoint()
def main():
    f.remote()
```

Running `modal run script.py` will execute the `main` function locally, which would call the `f` function remotely. However you can instead run `modal run script.py::app.f` or `modal run script.py::app.g` to execute `f` or `g` directly.


#### Argument parsing

> If your entrypoint function takes arguments with primitive types, modal run automatically parses them as CLI options. For example, the following function can be called with `modal run script.py --foo 1 --bar "hello"`:

```python
# script.py
@app.local_entrypoint()
def main(foo: int, bar: str):
    some_modal_function.remote(foo, bar)
```

### Deployed Apps

> A deployed App is created using the modal deploy CLI command. The App is persisted indefinitely until you delete it via the web UI. Functions in a deployed App that have an attached schedule will be run on a schedule. Otherwise, you can invoke them manually using web endpoints or Python.

> Deployed Apps are named via the App constructor. Re-deploying an existing App (based on the name) will update it in place.


## 🏃 Run tests

* pytest settings are in the `pyproject.toml` file so everything does not need to be specified in the command line.
* The tests are split and run in parallel to speed up the CI.
* Some tests can be flaky, for example when doing live testing with other systems without mocking. This issue can be overcome with the rerun option which is also enabled.
* Make sure that the tests are passing and that they pass the coverage requirement.

```bash
# to run all tests
uv run pytest

# to run specific splits of the tests (mostly useful for CI, not standalone).
make split-tests SPLITS=4 GROUP=2
```