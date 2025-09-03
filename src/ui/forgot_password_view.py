import flet as ft
from ..components.ui_components import UIComponents
from ..controllers.auth_controller import send_code_click, verify_code_click,resend_code_click, reset_password_click

class ForgotPasswordView:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.reset_step = 1
        self.current_reset_email = ""
        
        self.reset_email_field = None
        self.verification_code_field = None
        self.new_password_field = None
        self.confirm_new_password_field = None
    
    def create_view(self) -> ft.Container:
        if self.reset_step == 1:
            return self._create_email_step()
        elif self.reset_step == 2:
            return self._create_verification_step()
        else:
            return self._create_new_password_step()
    
    def _create_email_step(self) -> ft.Container:
        self.reset_email_field = UIComponents.create_text_field("Email")
        
        content = ft.Column([
            UIComponents.create_title("Recuperar Senha"),
            UIComponents.create_subtitle("Digite seu email para receber o código"),
            ft.Container(height=20),
            self.reset_email_field,
            ft.Container(height=20),
            UIComponents.create_button("Enviar Código", lambda e: send_code_click(e, self)),
            ft.Container(height=15),
            UIComponents.create_text_button("← Voltar ao Login", self._on_back_to_login_click),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return UIComponents.create_container(content)
    
    def _create_verification_step(self) -> ft.Container:
        self.verification_code_field = UIComponents.create_text_field("Código de Verificação")
        
        content = ft.Column([
            UIComponents.create_title("Verificação"),
            UIComponents.create_subtitle("Digite o código enviado para seu email"),
            ft.Container(height=20),
            self.verification_code_field,
            ft.Container(height=20),
            UIComponents.create_button("Verificar Código", lambda e: verify_code_click(e, self)),
            ft.Container(height=10),
            UIComponents.create_text_button("Reenviar Código", lambda e: resend_code_click(e, self)),
            ft.Container(height=15),
            UIComponents.create_text_button("← Voltar ao Login", self._on_back_to_login_click),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return UIComponents.create_container(content)
    
    def _create_new_password_step(self) -> ft.Container:
        self.new_password_field = UIComponents.create_text_field("Nova Senha", password=True)
        self.confirm_new_password_field = UIComponents.create_text_field("Confirmar Nova Senha", password=True)
        
        content = ft.Column([
            UIComponents.create_title("Nova Senha"),
            UIComponents.create_subtitle("Digite sua nova senha"),
            ft.Container(height=20),
            self.new_password_field,
            self.confirm_new_password_field,
            ft.Container(height=20),
            UIComponents.create_button("Alterar Senha", lambda e: reset_password_click(e, self)),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return UIComponents.create_container(content)
    
    def _on_back_to_login_click(self, e):
        self.reset_step = 1
        self.app_controller.navigate_to("login")
    
    def reset_state(self):
        self.reset_step = 1
        self.current_reset_email = ""