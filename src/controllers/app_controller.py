import flet as ft
from ..ui.login_view import LoginView
from ..ui.register_view import RegisterView
from ..ui.forgot_password_view import ForgotPasswordView
from ..ui.homepage_view import HomepageView
from ..utils.colors import Colors


class AppController:
  
    def __init__(self):

        self.page = None
        self.current_view = "login"
        self.login_view = LoginView(self)
        self.register_view = RegisterView(self)
        self.forgot_password_view = ForgotPasswordView(self)
        self.homepage_view = HomepageView(self)

        self.logged_user_email = None
    
    def initialize(self, page: ft.Page):

        self.page = page
  
        page.title = "Sistema de Login"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = None
        page.padding = 0
        page.spacing = 0
        page.window.width = 500
        page.window.height = 700
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
            expand=True,
            content=ft.Column([
                ft.Container(height=50), 
                self._get_current_view(),
                ft.Container(height=50), 
            ],
                alignment=ft.MainAxisAlignment.CENTER,
             horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            gradient=ft.LinearGradient([
                ft.Colors.with_opacity(0.1, "PURPLE"),
                ft.Colors.with_opacity(0.05, 'BLUE'),
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
        elif self.current_view == "homepage":
            return self.homepage_view.create_view(self.logged_user_email)
    
    def show_snackbar(self, message: str, error: bool = False):
        self.page.open(ft.SnackBar(
            content=ft.Text(message, color=Colors.WHITE),
            bgcolor=Colors.ERROR if error else Colors.BLUE_LIGHT,
            duration=3000
        ))
        
        self.page.update()
