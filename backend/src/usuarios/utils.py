# usuarios/utils.py

# Este arquivo contém funções utilitárias para o app 'usuarios'.
# A principal funcionalidade aqui é o envio de e-mails de forma assíncrona,
# ou seja, em uma thread separada. Isso evita que a aplicação principal
# fique "travada" esperando o envio do e-mail, melhorando a experiência
# do usuário ao se cadastrar ou solicitar uma nova senha.

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import threading

class EmailThread(threading.Thread):
    """
    Classe auxiliar que executa o envio de e-mail em uma thread separada.
    Isso previne que a requisição do usuário fique aguardando a conclusão do envio,
    o que poderia causar timeouts e uma má experiência.
    """
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        """
        Este método é executado quando a thread é iniciada.
        Ele tenta enviar o e-mail e registra o sucesso ou a falha no console.
        """
        try:
            self.email.send()
            # Log de sucesso (útil para depuração em ambientes de produção como o Render)
            print(f"Email para {self.email.to} enviado com sucesso em segundo plano.")
        except Exception as e:
            # Log de erro
            print(f"ERRO ao enviar e-mail em segundo plano para {self.email.to}: {e}")

def enviar_email_com_template(request, subject, template_name, context, recipient_list):
    """
    Função principal para enviar e-mails.
    Ela renderiza um template HTML, cria o objeto de e-mail e dispara a
    EmailThread para enviá-lo em segundo plano.
    """
    # Adiciona o host (ex: '127.0.0.1:8000' ou 'seu-site.onrender.com') ao contexto
    # para que os links de confirmação/reset nos e-mails sejam gerados corretamente.
    context['host'] = request.get_host()
    
    # Renderiza o template HTML (ex: email_confirmacao.html) com os dados do contexto
    html_content = render_to_string(template_name, context)
    
    # Cria o objeto de e-mail
    email = EmailMultiAlternatives(
        subject=subject,
        body='', # O corpo principal será o HTML, então o corpo de texto plano pode ser vazio
        from_email=settings.DEFAULT_FROM_EMAIL, # Usa o remetente configurado no settings.py
        to=recipient_list
    )
    # Anexa a versão HTML ao e-mail
    email.attach_alternative(html_content, "text/html")

    # Inicia a thread para enviar o e-mail sem bloquear a aplicação principal
    EmailThread(email).start()