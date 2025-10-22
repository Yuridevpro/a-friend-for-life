# backend/generate_schema.py

import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect('db.sqlite3')

# Abre o arquivo de destino para escrita
with open('../database/schema.sql', 'w') as f:
    # Itera sobre cada linha do dump do banco e escreve no arquivo
    for line in conn.iterdump():
        f.write('%s\n' % line)

print("Arquivo schema.sql gerado com sucesso na pasta 'database'!")

# Fecha a conexão
conn.close()