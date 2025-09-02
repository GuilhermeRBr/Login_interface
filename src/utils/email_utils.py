import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

def smtp_send_code(generate_code, email):
    load_dotenv()
    sender = os.getenv("EMAIL")
    app_password = os.getenv("APP_PASSWORD")
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(sender, app_password)

            subject = 'Código de verificação'
            body = f'Seu código de verificação é: {generate_code}'

            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = email

            smtp.sendmail(sender, email, msg.as_string())

            return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {str(e)}")
        return False