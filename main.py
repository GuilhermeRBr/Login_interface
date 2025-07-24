import flet as ft
from src.app_controller import AppController

def main(page: ft.Page):
    app = AppController()
    app.initialize(page)

if __name__ == "__main__":
    ft.app(target=main)