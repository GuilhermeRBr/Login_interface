import flet as ft
from ..components.ui_components import UIComponents
from ..controllers.auth_controller import login_click

class LoginView:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.email_field = None
        self.password_field = None
    
    def create_view(self) -> ft.Container:
        self.email_field = UIComponents.create_text_field("Email")
        self.password_field = UIComponents.create_text_field("Senha", password=True)
        
        content = ft.Column([
            UIComponents.create_title("Bem-vindo"),
            UIComponents.create_subtitle("Faça login para continuar"),
            ft.Container(height=20),
            self.email_field,
            self.password_field,
            ft.Container(height=10),
            UIComponents.create_button("Entrar", lambda e: login_click(e, self)),
            ft.Container(height=15),
            ft.Row([
                UIComponents.create_text_button("Registrar-se", self._on_register_click),
                UIComponents.create_text_button("Esqueceu a senha?", self._on_forgot_password_click),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return UIComponents.create_container(content)
    
    def _on_register_click(self, e):
        self.app_controller.navigate_to("register")
    
    def _on_forgot_password_click(self, e):
        self.app_controller.navigate_to("forgot_password")