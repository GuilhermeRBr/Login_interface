from fastapi import FastAPI
import flet as ft
from src.controller.app_controller import AppController

api = FastAPI()
from src.routes.auth_routes import auth_router

api.include_router(auth_router)

def main(page: ft.Page):

    app = AppController()
    app.initialize(page)

if __name__ == "__main__":
    ft.app(target=main)
