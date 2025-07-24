import flet as ft
from ..components.ui_components import UIComponents
from ..utils.validators import validate_email, validate_password_length, passwords_match

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
            UIComponents.create_button("Cadastrar", self._on_register_submit_click),
            ft.Container(height=15),
            UIComponents.create_text_button("← Voltar ao Login", self._on_back_to_login_click),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return UIComponents.create_container(content)
    
    def _on_register_submit_click(self, e):
        email = self.email_field.value or ""
        password = self.password_field.value or ""
        confirm_password = self.confirm_password_field.value or ""
        
        if not email or not password or not confirm_password:
            self.app_controller.show_snackbar("Preencha todos os campos", error=True)
            return
        
        if not validate_email(email):
            self.app_controller.show_snackbar("Email inválido", error=True)
            return
        
        if not validate_password_length(password):
            self.app_controller.show_snackbar("A senha deve ter pelo menos 6 caracteres", error=True)
            return
        
        if not passwords_match(password, confirm_password):
            self.app_controller.show_snackbar("As senhas não coincidem", error=True)
            return
        
        if self.app_controller.user_model.user_exists(email):
            self.app_controller.show_snackbar("Email já cadastrado", error=True)
            return
        
        if self.app_controller.user_model.create_user(email, password):
            self.app_controller.show_snackbar("Usuário cadastrado com sucesso!")
            self.app_controller.navigate_to("login")
        else:
            self.app_controller.show_snackbar("Erro ao cadastrar usuário", error=True)
    
    def _on_back_to_login_click(self, e):
        self.app_controller.navigate_to("login")