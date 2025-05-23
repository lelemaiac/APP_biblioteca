import requests


def lista_status():
    url = 'http://10.135.232.20:5000/status_livro'
    response_status = requests.get(url)

    if response_status.status_code == 200:
        dados_emprestimo = response_status.json()
        print(dados_emprestimo)
        return dados_emprestimo
    else:
        print(response_status.json())

lista_status()