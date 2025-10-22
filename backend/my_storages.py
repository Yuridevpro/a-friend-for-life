# my_storages.py


# Este arquivo define classes de armazenamento personalizadas para o Django.
# A classe 'MediaStorage' é configurada para interagir com o Amazon S3.
# Ela especifica que os arquivos de mídia devem ser salvos em uma subpasta
# chamada 'media' dentro do bucket do S3 e garante que arquivos com o
# mesmo nome não sejam sobrescritos, o que é uma boa prática de segurança.

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'media' # Subpasta no bucket do S3 para os arquivos.
    file_overwrite = False # Impede que arquivos com o mesmo nome sejam sobrescritos.
    
    