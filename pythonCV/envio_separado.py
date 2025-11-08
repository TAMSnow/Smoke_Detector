import win32com.client as win32
import pandas as pd
import os
def enviar_emails(dataHora, imagem):
    # 1. Carregar o arquivo
    contatos = pd.read_csv('contatos.csv')
    print(contatos.columns.tolist())
    imagem_path = os.path.abspath(imagem)

    # 2. Inicializar o Outlook (fora do loop, é mais eficiente)
    outlook = win32.Dispatch('outlook.application')

    # 3. Iterar sobre as linhas do DataFrame para enviar emails individuais
    for index, linha in contatos.iterrows():
        # 'linha' é um objeto Series que contém os valores da linha atual
        nome_do_contato = linha['nomes']  # Assumindo que a coluna se chama 'nomes'
        email_do_contato = linha['email'] # Assumindo que a coluna se chama 'email'

        # 4. Criar o corpo do email personalizado
        # Usamos uma f-string (string formatada) para inserir o nome
        corpo_email_personalizado = f"Olá, {nome_do_contato}\n\tUm fumante em área proibida foi detectado durante {dataHora}."

        # 5. Criar e configurar o email
        email = outlook.CreateItem(0)
        email.To = email_do_contato  # Apenas o e-mail do contato atual
        email.Subject = "URGENTE: alerta de Fumante"
        email.Body = corpo_email_personalizado
        email.Attachments.Add(imagem_path)

        # 6. Enviar o emailq
        email.Send()
        print(f"E-mail de Alerta enviado com sucesso para: {nome_do_contato} ({email_do_contato})")

    print("\nProcesso de envio concluído.")