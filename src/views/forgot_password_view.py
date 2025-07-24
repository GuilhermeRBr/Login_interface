import flet as ft
from ..components.ui_components import UIComponents
from ..utils.validators import validate_email, validate_password_length, passwords_match, generate_verification_code

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
            UIComponents.create_button("Enviar Código", self._on_send_code_click),
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
            UIComponents.create_button("Verificar Código", self._on_verify_code_click),
            ft.Container(height=10),
            UIComponents.create_text_button("Reenviar Código", self._on_resend_code_click),
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
            UIComponents.create_button("Alterar Senha", self._on_reset_password_click),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return UIComponents.create_container(content)
    
    def _on_send_code_click(self, e):
        email = self.reset_email_field.value or ""
        
        if not email:
            self.app_controller.show_snackbar("Digite seu email", error=True)
            return
        
        if not validate_email(email):
            self.app_controller.show_snackbar("Email inválido", error=True)
            return
        
        if not self.app_controller.user_model.user_exists(email):
            self.app_controller.show_snackbar("Email não encontrado", error=True)
            return
        
        code = generate_verification_code()
        self.app_controller.user_model.store_verification_code(email, code)
        self.current_reset_email = email
        self.reset_step = 2
        self.app_controller.show_snackbar(f"Código enviado para {email}. Código: {code}")
        self.app_controller.update_view()
    
    def _on_verify_code_click(self, e):
        code = self.verification_code_field.value or ""
        
        if not code:
            self.app_controller.show_snackbar("Digite o código de verificação", error=True)
            return
        
        if not self.app_controller.user_model.verify_code(self.current_reset_email, code):
            self.app_controller.show_snackbar("Código inválido", error=True)
            return
        
        self.reset_step = 3
        self.app_controller.update_view()
    
    def _on_resend_code_click(self, e):
        code = generate_verification_code()
        self.app_controller.user_model.store_verification_code(self.current_reset_email, code)
        self.app_controller.show_snackbar(f"Novo código enviado. Código: {code}")
    
    def _on_reset_password_click(self, e):
        new_password = self.new_password_field.value or ""
        confirm_new_password = self.confirm_new_password_field.value or ""
        
        if not new_password or not confirm_new_password:
            self.app_controller.show_snackbar("Preencha todos os campos", error=True)
            return
        
        if not validate_password_length(new_password):
            self.app_controller.show_snackbar("A senha deve ter pelo menos 6 caracteres", error=True)
            return
        
        if not passwords_match(new_password, confirm_new_password):
            self.app_controller.show_snackbar("As senhas não coincidem", error=True)
            return
        
        if self.app_controller.user_model.update_password(self.current_reset_email, new_password):
            self.app_controller.show_snackbar("Senha alterada com sucesso!")
            self.reset_step = 1
            self.app_controller.navigate_to("login")
        else:
            self.app_controller.show_snackbar("Erro ao alterar senha", error=True)
    
    def _on_back_to_login_click(self, e):
        self.reset_step = 1
        self.app_controller.navigate_to("login")
    
    def reset_state(self):
        self.reset_step = 1
        self.current_reset_email = ""