import requests


def lista_livros():
    url = 'http://10.135.232.20:5000/livros'
    response_livros = requests.get(url)

    if response_livros.status_code == 200:
        dados_livro = response_livros.json()
        # return dados_livro['livros']
        print(dados_livro)

    else:
        print(f'Erro: {response_livros.status_code}')

lista_livros()