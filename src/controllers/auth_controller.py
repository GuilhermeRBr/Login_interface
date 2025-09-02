from flet import ControlEvent
import requests
from ..utils.validators import validate_email, validate_password_length, passwords_match, generate_verification_code
from ..utils.email_utils import smtp_send_code


generate_code = None

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

        view.app_controller.navigate_to("login")
    else:
        view.app_controller.show_snackbar("Erro ao cadastrar usuário", error=True)

def login_click(e: ControlEvent, view):
    email = view.email_field.value or ""
    password = view.password_field.value or ""

    print(email, password)

    if not email or not password:
        view.app_controller.show_snackbar("Preencha todos os campos", error=True)
        return
    
    if not validate_email(email):
        view.app_controller.show_snackbar("Email inválido", error=True)
        return
    
    payload = {
    "email": email,
    "password": password
    }

    url = 'http://127.0.0.1:8000/auth/login'

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            view.app_controller.show_snackbar("Login realizado com sucesso!")
            print('Resposta:', response.json())
            # Aqui você pode armazenar o token de acesso ou realizar outras ações necessárias
            view.app_controller.logged_user_email = email
            view.app_controller.navigate_to("homepage")
        elif response.status_code == 401:
            view.app_controller.show_snackbar("Email ou senha incorretos", error=True)
        else:
            view.app_controller.show_snackbar("Erro ao realizar login", error=True)
    except requests.exceptions.RequestException as e:
        view.app_controller.show_snackbar("Erro de conexão com o servidor", error=True)
        print(f"Erro de conexão: {str(e)}")

def send_code_click(e: ControlEvent, view):
    global generate_code

    email = view.reset_email_field.value or ""

    if not email:
        view.app_controller.show_snackbar("Digite seu email", error=True)
        return
    if not validate_email(email):
        view.app_controller.show_snackbar("Email inválido", error=True)
        return 
    generate_code = generate_verification_code()


    if smtp_send_code(generate_code, email):
        print("E-mail enviado com sucesso!")
    else:
        view.app_controller.show_snackbar("Erro ao enviar e-mail. Tente novamente mais tarde.", error=True)
        return

    view.app_controller.show_snackbar(f"Se o e-mail estiver cadastrado, enviaremos as instruções para recuperação de senha.")

    view.reset_step = 2
    view.app_controller.update_view()

def verify_code_click(e: ControlEvent, view):
    code = view.verification_code_field.value or ""

    if not code:
        view.app_controller.show_snackbar("Digite o código de verificação", error=True)
        return

    if code != generate_code:
        view.app_controller.show_snackbar("Código inválido", error=True)
        return

    view.reset_step = 3
    view.app_controller.update_view()

def resend_code_click(e: ControlEvent, view):
    global generate_code

    generate_code = generate_verification_code()
    email = view.reset_email_field.value or ""

    if smtp_send_code(generate_code, email):
        print("E-mail enviado com sucesso!")
    else:
        view.app_controller.show_snackbar("Erro ao enviar e-mail. Tente novamente mais tarde.", error=True)
        return

    view.app_controller.show_snackbar("Novo código enviado. Verifique seu e-mail.")

def reset_password_click(e: ControlEvent, view):
    new_password = view.new_password_field.value or ""
    confirm_new_password = view.confirm_new_password_field.value or ""

    if not new_password or not confirm_new_password:
        view.app_controller.show_snackbar("Preencha todos os campos", error=True)
        return

    if not validate_password_length(new_password):
        view.app_controller.show_snackbar("A senha deve ter pelo menos 6 caracteres", error=True)
        return

    if not passwords_match(new_password, confirm_new_password):
        view.app_controller.show_snackbar("As senhas não coincidem", error=True)
        return
    
    
    payload = {
        "email": view.reset_email_field.value,
        "password": new_password
    }
    url = 'http://127.0.0.1:8000/auth/reset_password'
    response = requests.post(url, json=payload)


    view.app_controller.show_snackbar("Senha alterada com sucesso!")
    view.reset_step = 1
    view.app_controller.navigate_to("login")
