import flet as ft
from .models.user import UserModel
from .views.login_view import LoginView
from .views.register_view import RegisterView
from .views.forgot_password_view import ForgotPasswordView
from .utils.colors import Colors

class AppController:
  
    def __init__(self):
        self.page = None
        self.current_view = "login"
        
        self.user_model = UserModel()
        
        self.login_view = LoginView(self)
        self.register_view = RegisterView(self)
        self.forgot_password_view = ForgotPasswordView(self)
    
    def initialize(self, page: ft.Page):

        self.page = page
  
        page.title = "Sistema de Login"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = Colors.WHITE
        page.window.width = 450
        page.window.height = 650
        page.window.resizable = False
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.update_view()
    
    def navigate_to(self, view_name: str):
        if view_name == "forgot_password" and self.current_view != "forgot_password":
            self.forgot_password_view.reset_state()
        
        self.current_view = view_name
        self.update_view()
    
    def update_view(self):
        self.page.controls.clear()
        
        main_container = ft.Container(
            content=ft.Column([
                ft.Container(height=50), 
                self._get_current_view(),
                ft.Container(height=50), 
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=self.page.width,
            height=self.page.height,
            gradient=ft.LinearGradient([
                ft.Colors.with_opacity(0.1, Colors.PURPLE_DARK),
                ft.Colors.with_opacity(0.05, Colors.BLUE_LIGHT),
            ]),
        )
        
        self.page.add(main_container)
        self.page.update()
    
    def _get_current_view(self):
        if self.current_view == "login":
            return self.login_view.create_view()
        elif self.current_view == "register":
            return self.register_view.create_view()
        elif self.current_view == "forgot_password":
            return self.forgot_password_view.create_view()
    
    def show_snackbar(self, message: str, error: bool = False):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=Colors.WHITE),
            bgcolor=Colors.ERROR if error else Colors.BLUE_LIGHT,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()