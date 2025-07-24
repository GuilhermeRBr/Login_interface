import flet as ft
from ..utils.colors import Colors



class UIComponents:
    @staticmethod
    def create_text_field(label: str, password: bool = False, width: int = 300) -> ft.TextField:
        return ft.TextField(
            label=label,
            password=password,
            width=width,
            border_color=Colors.GRAY_LIGHT,
            focused_border_color=Colors.BLUE_LIGHT,
            label_style=ft.TextStyle(color=Colors.GRAY_LIGHT),
            text_style=ft.TextStyle(color=Colors.PURPLE_DARK),
            cursor_color=Colors.BLUE_LIGHT,
            bgcolor=Colors.WHITE,
            border_radius=8,
        )
    
    @staticmethod
    def create_button(text: str, on_click, primary: bool = True, width: int = 300) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            text=text,
            on_click=on_click,
            width=width,
            height=45,
            bgcolor=Colors.PURPLE_DARK if primary else Colors.BLUE_LIGHT,
            color=Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=2,
            )
        )
    
    @staticmethod
    def create_text_button(text: str, on_click) -> ft.TextButton:
        return ft.TextButton(
            text=text,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=Colors.BLUE_LIGHT,
            )
        )
    
    @staticmethod
    def create_container(content, width: int = 400, padding: int = 30) -> ft.Container:
        return ft.Container(
            content=content,
            width=width,
            bgcolor=Colors.WHITE,
            border_radius=12,
            padding=padding,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, Colors.PURPLE_DARK),
                offset=ft.Offset(0, 4),
            ),
        )
    
    @staticmethod
    def create_title(text: str, size: int = 32) -> ft.Text:
        return ft.Text(
            text,
            size=size,
            weight=ft.FontWeight.BOLD,
            color=Colors.PURPLE_DARK,
            text_align=ft.TextAlign.CENTER,
        )
    
    @staticmethod
    def create_subtitle(text: str, size: int = 16) -> ft.Text:
        return ft.Text(
            text,
            size=size,
            color=Colors.GRAY_LIGHT,
            text_align=ft.TextAlign.CENTER,
        )