from fastapi import FastAPI


class App:
    def __init__(self):
        self.app = FastAPI(title="OOP FastAPI Example")

    def get_app(self):
        return self.app


app_instance = App()
app = app_instance.get_app()
