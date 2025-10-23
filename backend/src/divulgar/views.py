# divulgar/views.py

# Este arquivo contém as views para o app 'divulgar'.
# Ele gerencia a lógica para o cadastro de novos pets, a visualização
# detalhada de um pet específico e a edição das informações de um pet já cadastrado.
# As views aqui são protegidas para garantir que apenas usuários logados
# e proprietários dos pets possam realizar ações de criação e modificação.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pet, PetImage
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def novo_pet(request):
    """
    Processa o formulário de cadastro de um novo pet.
    - Se a requisição for GET, exibe o formulário em branco.
    - Se a requisição for POST, valida todos os dados enviados. Se válidos, cria o registro
      do Pet e suas imagens, salvando-as no S3. Se inválidos, retorna o
      formulário com as mensagens de erro.
    """
    if request.method == 'POST':
        # Coleta de dados do formulário. Listas são obtidas com 'getlist'.
        especie = request.POST.get('especie')
        sexo = request.POST.get('sexo')
        tamanho = request.POST.get('tamanho')
        nome_pet = request.POST.get('nome_pet')
        historia_pet = request.POST.get('historia_pet')
        cuidados = request.POST.getlist('cuidados')
        vive_bem_em = request.POST.getlist('vive_bem_em')
        temperamento = request.POST.getlist('temperamento')
        sociavel_com = request.POST.getlist('sociavel_com')
       

        # Bloco de validação de todos os campos obrigatórios.
        errors = []
        if not request.FILES.get('foto_principal'):
            errors.append('Foto principal é obrigatória.')
        if not especie:
            errors.append('Espécie é obrigatória.')
        if not sexo:
            errors.append('Sexo é obrigatório.')
        if not tamanho:
            errors.append('Tamanho é obrigatório.')
        if not nome_pet:
            errors.append('Nome do Pet é obrigatório.')
        if not cuidados:
            errors.append('Cuidados são obrigatórios.')
        if not vive_bem_em:
            errors.append('Vive bem em é obrigatório.')
        if not temperamento:
            errors.append('Temperamento é obrigatório.')
        if not sociavel_com:
            errors.append('Sociável com é obrigatório.')
        
        # Validação do número de imagens secundárias.
        secondary_images = request.FILES.getlist('fotos_secundarias')
        if len(secondary_images) > 5:
            errors.append('Você pode enviar no máximo 5 imagens secundárias.')
        
        # Se houver erros, renderiza o formulário novamente com os erros e dados já preenchidos.
        if errors:
            return render(request, 'divulgar/novo_pet.html', {
                'especie': especie,
                'sexo': sexo,
                'tamanho': tamanho,
                'cuidados': cuidados,
                'vive_bem_em': vive_bem_em,
                'temperamento': temperamento,
                'sociavel_com': sociavel_com,
                'nome_pet': nome_pet,
                'historia_pet': historia_pet,
                'errors': errors,
            })

        # Cria a instância do Pet e salva no banco.
        pet = Pet(
            especie=especie,
            sexo=sexo,
            tamanho=tamanho,
            nome_pet=nome_pet,
            historia_pet=historia_pet,
            usuario=request.user, # Associa o pet ao usuário logado.
            cuidados=cuidados,
            vive_bem_em=vive_bem_em,
            temperamento=temperamento,
            sociavel_com=sociavel_com,
           
        )
        pet.save()

        # Salva a imagem principal.
        main_image = request.FILES.get('foto_principal')
        if main_image:
            pet.foto_principal = main_image
            pet.save()

        # Salva as imagens secundárias, limitando a 5.
        secondary_images = request.FILES.getlist('fotos_secundarias')
        for image in secondary_images[:5]:
            secondary_image = PetImage.objects.create(pet=pet, image=image)
            pet.fotos_secundarias.add(secondary_image)

        messages.success(request, 'Pet cadastrado com sucesso!')
        return redirect(reverse('listar_pets'))

    # Se a requisição for GET, apenas renderiza o formulário vazio.
    return render(request, 'divulgar/novo_pet.html')





def ver_pet(request, id):
    """
    Exibe a página de detalhes de um pet específico.
    - Se GET, mostra as informações do pet.
    - Se POST, permite que o dono do pet o marque como "Adotado".
    """
    pet = get_object_or_404(Pet, id=id)
    
    if request.method == "GET":
        return render(request, 'divulgar/ver_pet.html', {'pet': pet})

    if request.method == "POST":
        # Verifica se o usuário que está fazendo a requisição é o dono do pet.
        if pet.usuario != request.user:
            messages.add_message(request, messages.ERROR, 'Esse pet não é seu!')
            return redirect('ver_pet', id=id)

        # Atualiza o status do pet para "Adotado".
        pet.status = 'A'
        pet.save()

        messages.success(request, 'Pet marcado como adotado com sucesso.')
        return redirect('ver_pet', id=id)


@login_required
def editar_pet(request, id):
    """
    Processa a edição de um pet existente.
    - Garante que apenas o dono do pet possa editá-lo.
    - Se GET, exibe o formulário pré-preenchido com os dados atuais do pet.
    - Se POST, valida e salva as alterações, incluindo a remoção e adição de imagens.
    """
    pet = get_object_or_404(Pet, id=id)

    # Verifica se o usuário logado é o proprietário do pet.
    if pet.usuario != request.user:
        messages.error(request, 'Você não tem permissão para editar este pet.')
        return redirect('meu_perfil')

    if request.method == "POST":
        # Coleta os dados do formulário de edição.
        nome_pet = request.POST.get('nome_pet')
        historia_pet = request.POST.get('historia_pet')
        especie = request.POST.get('especie')
        sexo = request.POST.get('sexo')
        tamanho = request.POST.get('tamanho')
        cuidados = request.POST.getlist('cuidados')
        vive_bem_em = request.POST.getlist('vive_bem_em')
        temperamento = request.POST.getlist('temperamento')
        sociavel_com = request.POST.getlist('sociavel_com')
        foto_principal = request.FILES.get('foto_principal')
        remover_foto_principal = request.POST.get('remover_foto_principal')
        
        novas_fotos_secundarias = request.FILES.getlist('fotos_secundarias')
        ids_fotos_remover = request.POST.getlist('remover_fotos_secundarias')

        # Validação dos campos obrigatórios.
        errors = []
        if not nome_pet: errors.append('Nome do Pet é obrigatório.')
        if not historia_pet: errors.append('A história do Pet é obrigatória.')
        if not especie: errors.append('Espécie é obrigatória.')
        if not sexo: errors.append('Sexo é obrigatório.')
        if not tamanho: errors.append('Tamanho é obrigatório.')
        if not cuidados: errors.append('Cuidados são obrigatórios.')
        if not vive_bem_em: errors.append('Vive bem em é obrigatório.')
        if not temperamento: errors.append('Temperamento é obrigatório.')
        if not sociavel_com: errors.append('Sociável com é obrigatório.')
        if (not pet.foto_principal or remover_foto_principal) and not foto_principal:
            errors.append('A foto principal é obrigatória. Adicione uma antes de salvar.')

        
        # Validação da contagem de fotos secundárias.
        fotos_existentes_count = pet.images.count()
        fotos_a_remover_count = len(ids_fotos_remover)
        fotos_novas_count = len(novas_fotos_secundarias)
        total_fotos_final = (fotos_existentes_count - fotos_a_remover_count) + fotos_novas_count

        if total_fotos_final > 5:
            errors.append(f'O pet só pode ter no máximo 5 fotos secundárias. Você está tentando salvar com {total_fotos_final}.')

        if errors:
            context = {
                'pet': pet,
                'choices_especie': Pet.choices_especie,
                'choices_sexo': Pet.choices_sexo,
                'choices_tamanho': Pet.choices_tamanho,
                'errors': errors,
            }
            return render(request, 'divulgar/editar_pet.html', context)
        
        # Atualização dos dados do objeto pet.
        pet.nome_pet = nome_pet
        pet.historia_pet = historia_pet
        pet.especie = especie
        pet.sexo = sexo
        pet.tamanho = tamanho
        pet.cuidados = cuidados
        pet.vive_bem_em = vive_bem_em
        pet.temperamento = temperamento
        pet.sociavel_com = sociavel_com

        # Lógica para atualizar a foto principal.
        if foto_principal:
            pet.foto_principal = foto_principal
        elif remover_foto_principal:
            # Só remove se o usuário marcou para remover.
            if pet.foto_principal:
                pet.foto_principal.delete(save=False)
                pet.foto_principal = None

        
        pet.save()

        # 1. Remove as fotos secundárias marcadas para exclusão.
        if ids_fotos_remover:
            fotos_remover = PetImage.objects.filter(id__in=ids_fotos_remover, pet=pet)
            for foto in fotos_remover:
                pet.fotos_secundarias.remove(foto)  # Remove da relação ManyToMany.
                foto.delete()  # Deleta o objeto e o arquivo do S3.

        # 2. Adiciona as novas fotos secundárias enviadas.
        for foto in novas_fotos_secundarias:
            nova_foto = PetImage.objects.create(pet=pet, image=foto)
            pet.fotos_secundarias.add(nova_foto)  # Adiciona na relação ManyToMany.

        
        messages.success(request, f'As informações de {pet.nome_pet} foram atualizadas com sucesso!')
        return redirect('meu_perfil')
    
    else: # Requisição GET
        # Se GET, apenas prepara o contexto com os dados do pet para preencher o formulário.
        context = {
            'pet': pet,
            'choices_especie': Pet.choices_especie,
            'choices_sexo': Pet.choices_sexo,
            'choices_tamanho': Pet.choices_tamanho,
        }
        return render(request, 'divulgar/editar_pet.html', context)