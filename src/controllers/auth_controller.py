from flet import ControlEvent
from ..utils.validators import validate_email, validate_password_length, passwords_match
import requests

def register_click(e: ControlEvent, view):
    email = view.email_field.value or ""
    password = view.password_field.value or ""
    confirm_password = view.confirm_password_field.value or ""

    print(email, password, confirm_password)

    if not email or not password or not confirm_password:
        view.app_controller.show_snackbar("Preencha todos os campos", error=True)
        return

    if not validate_email(email):
        view.app_controller.show_snackbar("Email inválido", error=True)
        return

    if not validate_password_length(password):
        view.app_controller.show_snackbar("A senha deve ter pelo menos 6 caracteres", error=True)
        return

    if not passwords_match(password, confirm_password):
        view.app_controller.show_snackbar("As senhas não coincidem", error=True)
        return

    if view.app_controller.user_model.user_exists(email):
        view.app_controller.show_snackbar("Email já cadastrado", error=True)
        return

    if view.app_controller.user_model.create_user(email, password):
        view.app_controller.show_snackbar("Usuário cadastrado com sucesso!")

        payload = {
            "email": email,
            "password": password
        }
        url = 'http://127.0.0.1:8000/auth/register'
        response = requests.post(url, json=payload)

        print('Status:', response.status_code)
        print('Resposta:', response.json())


        view.app_controller.navigate_to("login")
    else:
        view.app_controller.show_snackbar("Erro ao cadastrar usuário", error=True)

def login_click(e: ControlEvent, view):
    email = view.email_field.value or ""
    password = view.password_field.value or ""

    print(email, password)

    payload = {
        "email": email,
        "password": password
    }

    url = 'http://127.0.0.1:8000/auth/login'

    response = requests.post(url, json=payload)

    print('Status:', response.status_code)
    print('Resposta:', response.json())
    if not email or not password:
        view.app_controller.show_snackbar("Preencha todos os campos", error=True)
        return
    
    if not validate_email(email):
        view.app_controller.show_snackbar("Email inválido", error=True)
        return
    
    if view.app_controller.user_model.authenticate_user(email, password):
        view.app_controller.show_snackbar("Login realizado com sucesso!")
    else:
        view.app_controller.show_snackbar("Email ou senha incorretos", error=True)