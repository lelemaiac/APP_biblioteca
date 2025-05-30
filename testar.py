import requests


def emprestimo_usuario(id):
    url = f'http://10.135.232.20:5000/emprestimos_usuario/{id}'
    response_emprestimo_usuario = requests.get(url)

    if response_emprestimo_usuario.status_code == 200:
        dados_emprestimo_usuario = response_emprestimo_usuario.json()
        print(dados_emprestimo_usuario)
    else:
        print(response_emprestimo_usuario.status_code)

emprestimo_usuario(1)
#
# def lista_status():
#     url = 'http://10.135.232.20:5000/status_livro'
#     response_status = requests.get(url)
#
#     if response_status.status_code == 200:
#         dados_emprestimo = response_status.json()
#         print(dados_emprestimo)
#     else:
#         print("erro")
#
# lista_status()