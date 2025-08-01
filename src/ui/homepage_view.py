import flet as ft
from ..components.ui_components import UIComponents


class HomepageView:
    def __init__(self, app_controller):
        self.app_controller = app_controller

    def create_view(self, email:str) -> ft.Container:
        content = ft.Column([
            UIComponents.create_title("Bem-vindo ao Sistema"),
            UIComponents.create_subtitle(f"Você está logado!\n{email}"),
            ft.Container(height=20),
            UIComponents.create_button("Sair", self._on_logout_click, primary=False),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        return UIComponents.create_container(content)

    def _on_logout_click(self, e):
        self.app_controller.navigate_to("login")