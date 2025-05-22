import requests

def lista_livro():
    url = 'http://10.135.232.20:5000/livros'
    response_livros = requests.get(url)

    if response_livros.status_code == 200:
        dados_livro = response_livros.json()
        print(dados_livro)
    else:
        print(f"ERRO: status {response_livros.status_code}")

lista_livro()