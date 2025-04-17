import modal

app = modal.App("example-get-started")


@app.function()
def square(x):
    print("This code is running on a remote worker!")
    return x**2


@app.local_entrypoint()
def main(num: int):  # mention datatype so command line args can be processed correctly.
    print(f"The square of {num} is {square.remote(num)}")
