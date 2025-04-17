from fastapi import FastAPI


def create_app(name: str) -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"message": f"Hello {name} from FastAPI on Modal with App!"}

    return app
