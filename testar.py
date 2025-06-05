import requests


def lista_livros():
    url = 'http://10.135.232.20:5000/livros'
    response_livros = requests.get(url)

    if response_livros.status_code == 200:
        dados_livro = response_livros.json()
        print(dados_livro)
        return dados_livro['livros']

    else:
        print(f'Erro: {response_livros.status_code}')
        return response_livros.json()

lista_livros()
