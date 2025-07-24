import flet as ft
from ..components.ui_components import UIComponents
from ..utils.validators import validate_email

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
            UIComponents.create_button("Entrar", self._on_login_click),
            ft.Container(height=15),
            ft.Row([
                UIComponents.create_text_button("Registrar-se", self._on_register_click),
                UIComponents.create_text_button("Esqueceu a senha?", self._on_forgot_password_click),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return UIComponents.create_container(content)
    
    def _on_login_click(self, e):
        email = self.email_field.value or ""
        password = self.password_field.value or ""
        
        if not email or not password:
            self.app_controller.show_snackbar("Preencha todos os campos", error=True)
            return
        
        if not validate_email(email):
            self.app_controller.show_snackbar("Email inválido", error=True)
            return
        
        if self.app_controller.user_model.authenticate_user(email, password):
            self.app_controller.show_snackbar("Login realizado com sucesso!")
        else:
            self.app_controller.show_snackbar("Email ou senha incorretos", error=True)
    
    def _on_register_click(self, e):
        self.app_controller.navigate_to("register")
    
    def _on_forgot_password_click(self, e):
        self.app_controller.navigate_to("forgot_password")