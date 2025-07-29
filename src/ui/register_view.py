import flet as ft
from ..components.ui_components import UIComponents
from ..controllers.auth_controller import register_click

class RegisterView:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.email_field = None
        self.password_field = None
        self.confirm_password_field = None
    
    def create_view(self) -> ft.Container:
        self.email_field = UIComponents.create_text_field("Email")
        self.password_field = UIComponents.create_text_field("Senha", password=True)
        self.confirm_password_field = UIComponents.create_text_field("Confirmar Senha", password=True)
        
        content = ft.Column([
            UIComponents.create_title("Criar Conta"),
            UIComponents.create_subtitle("Preencha os dados para se registrar"),
            ft.Container(height=20),
            self.email_field,
            self.password_field,
            self.confirm_password_field,
            ft.Container(height=20),
            UIComponents.create_button("Cadastrar", lambda e: register_click(e, self)),
            ft.Container(height=15),
            UIComponents.create_text_button("← Voltar ao Login", self._on_back_to_login_click),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return UIComponents.create_container(content)
    
    def _on_back_to_login_click(self, e):
        self.app_controller.navigate_to("login")