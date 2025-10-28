import win32com.client as win32
import pandas as pd

contatos = pd.read_csv('contatos.csv')
print(contatos.columns)
lista_emails = ';'.join(contatos['email;'])

corpo_email = """Olá,
Um fumante em área proibida foi detectado."""

outlook = win32.Dispatch('outlook.application')
email = outlook.CreateItem(0)
email.To = lista_emails
email.Subject = "Alerta"
email.Body = corpo_email
email.Send()
print("E-mail enviado com sucesso")