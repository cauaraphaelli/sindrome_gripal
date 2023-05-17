# -*- coding: utf-8 -*-

"""
# Bibliotecas
"""

import requests
import csv


"""# Coleta de Dados por meio da API"""

url = 'https://elasticsearch-saps.saude.gov.br/desc-esus-notifica-estado-*/_search'

params = {
    'size': 1500
}
auth = ('user-public-notificacoes', 'Za4qNXdyQNSa9YaA')

response = requests.get(url, params=params, auth=auth)
data = response.json()

"""# Tratamento de Dados e salvamento em CSV"""

# Extrair os dados relevantes da resposta da API
records = data['hits']['hits']
data_to_save = []
for record in records:
    source = record['_source']
    testes = source.get('testes', [])
    if testes:
        primeiro_teste = testes[0]
        tipo_teste = primeiro_teste.get('tipoTeste')
        resultado_teste = primeiro_teste.get('resultadoTeste')
    else:
        tipo_teste = None
        resultado_teste = None

    row = {
        '_id': record['_id'],
        'municipio': source['municipio'],
        'dataNotificacao': source['dataNotificacao'],
        'estadoNotificacao': source['estadoNotificacao'],
        'idade': source['idade'],
        'tipoTeste': tipo_teste,
        'resultadoTeste': resultado_teste,
        'sintomas': source['sintomas'],
        'sexo': source['sexo'],
        'dataPrimeiraDose': source['dataPrimeiraDose'],


        
    }
    data_to_save.append(row)

# Salvar os dados em um arquivo CSV
fieldnames = ['_id', 'municipio', 'dataNotificacao', 'estadoNotificacao', 'idade', 'tipoTeste', 'resultadoTeste', 'sintomas', 'sexo', 'dataPrimeiraDose']
filename = 'dados_notificacoes.csv'

with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_to_save)
