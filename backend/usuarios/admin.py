# usuarios/admin.py


# Este arquivo personaliza a interface de administração do Django para os modelos
# do app 'usuarios'. Ao registrar os modelos 'ResetSenha' e 'Ativacao' aqui,
# eles se tornam visíveis e gerenciáveis na área de administração do site,
# permitindo que os administradores visualizem e gerenciem os tokens de
# redefinição de senha e de ativação de contas.

from django.contrib import admin
from .models import ResetSenha, Ativacao

admin.site.register(ResetSenha)
admin.site.register(Ativacao)