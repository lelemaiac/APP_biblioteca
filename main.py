from tkinter.ttk import Style

import flet as ft
import requests
from flet import AppBar, Text, View, ElevatedButton
from flet.core.colors import Colors
from flet.core.dropdown import Option
from flet.core.types import CrossAxisAlignment, FontWeight
from dateutil.relativedelta import relativedelta
from datetime import datetime
from urllib3 import response

id_usuario_global = 0
id_emprestimo_global = 0
id_livro_global = 0
id_emprestimo_usuario_global = 0

def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de listas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    def salvar_livro(e):
        if (input_titulo.value == "" or input_isbn.value == ""
                or input_resumo.value == "" or input_autor.value == ""):
            msg_error.content = ft.Text("Preencha todos os campos")
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_livro = {
                "titulo": input_titulo.value,
                "autor": input_autor.value,
                "isbn": input_isbn.value,
                "resumo": input_resumo.value
            }

            resposta = post_cadastro_livro(novo_livro)

            if 'erro' in resposta:
                msg_error.content = ft.Text(resposta['erro'])
                page.overlay.append(msg_error)
                msg_error.open = True
                page.update()
            else:
                input_titulo.value = ""
                input_isbn.value = ""
                input_resumo.value = ""
                input_autor.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True

        page.update()


    def salvar_usuario(e):
        if (input_nome.value == "" or input_cpf.value == ""
                or input_endereco.value == "" or input_papel.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_usuario = {
                'nome': input_nome.value,
                'cpf': input_cpf.value,
                "endereco": input_endereco.value,
                "papel": input_papel.value,
            }

            resposta = cadastro_usuario(novo_usuario)

            if 'erro' in resposta:
                msg_error.content = ft.Text(resposta['erro'])
                page.overlay.append(msg_error)
                msg_error.open = True
                page.update()

            else:
                input_nome.value = ''
                input_cpf.value = ""
                input_endereco.value = ""
                input_papel.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
        page.update()


    def salvar_emprestimo(e):
        if (input_livro_id.value == "" or input_usuario_id.value == ""
                or input_data_emprestimo.value == "" or input_devolucao_prevista.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_emprestimo = {
                'livro_id': input_livro_id.value,
                'usuario_id': input_usuario_id.value,
                "data_emprestimo": input_data_emprestimo.value,
                "data_devolucao_prevista": input_devolucao_prevista.value,
            }

            resposta = cadastro_emprestimo(novo_emprestimo)

            if 'erro' in resposta:
                msg_error.content = ft.Text(resposta['erro'])
                page.overlay.append(msg_error)
                msg_error.open = True
                page.update()
            else:
                input_livro_id.value = ""
                input_usuario_id.value = ""
                input_data_emprestimo.value = ""
                input_devolucao_prevista.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
        page.update()

    def detalhes_livro(livro):
        txt_titulo.value = (f'Titulo: {livro["titulo"]}')
        txt_isbn.value = (f'ISBN: {livro["isbn"]}')
        txt_resumo.value = (f'Resumo: {livro["resumo"]}')
        txt_autor.value = (f'Autor: {livro["autor"]}')

        page.go("/detalhes_livros")

    def detalhes_usuario(usuario):
        txt_nome.value = (f'Nome: {usuario["nome"]}')
        txt_cpf.value = (f'CPF:{usuario["cpf"]}')
        txt_endereco.value = (f'Endereço: {usuario["endereco"]}')
        txt_papel.value = (f'Papel: {usuario["papel"]}')

        page.go("/detalhes_usuario")

    def detalhes_emprestimo(emprestimo):
        url_livro = f'http://10.135.232.20:5000/get_livro/{emprestimo["livro_id"]}'
        url_usuario = f'http://10.135.232.20:5000/get_usuario/{emprestimo["usuario_id"]}'

        response_livros = requests.get(url_livro)
        response_usuarios = requests.get(url_usuario)

        if response_livros.status_code and response_usuarios.status_code == 200:
            dados_livro = response_livros.json()
            dados_usuario = response_usuarios.json()

            txt_livroID.value = (f'Livro: {dados_livro["titulo"]}')
            txt_usuarioID.value = (f'Usuario: {dados_usuario["nome"]}')
            txt_data_emprestimo.value = (f'Data do emprestimo: {emprestimo["data_emprestimo"]}')
            txt_previsao_devolucao.value = (f'Devolução prevista: {emprestimo["data_devolucao_prevista"]}')

            page.go("/detalhes_emprestimo")

    def post_cadastro_livro(novo_livro):
        url = 'http://10.135.232.20:5000/cadastrar_livro'

        response = requests.post(url, json=novo_livro)

        if response.status_code == 201:
            dados_livros = response.json()

            return dados_livros
        else:
            return response.json()

    def cadastro_usuario(novo_usuario):
        url = 'http://10.135.232.20:5000/cadastrar_usuario'
        response = requests.post(url, json=novo_usuario)

        if response.status_code == 201:
            dados_usuario = response.json()

            return dados_usuario
        else:
            return response.json()

    def cadastro_emprestimo(novo_emprestimo):
        url = 'http://10.135.232.20:5000/cadastrar_emprestimo'
        response = requests.post(url, json=novo_emprestimo)

        if response.status_code == 201:
            dados_emprestimo = response.json()

            return dados_emprestimo
        else:
            return response.json()

    def lista_livros():
        url = 'http://10.135.232.20:5000/livros'
        response_livros = requests.get(url)

        if response_livros.status_code == 200:
            dados_livro = response_livros.json()
            return dados_livro ['livros']

        else:
            print(f'Erro: {response_livros.status_code}')
            return response.json()

    def lista_emprestimos():
        url = 'http://10.135.232.20:5000/emprestimos'
        response_emprestimos = requests.get(url)

        if response_emprestimos.status_code == 200:
            dados_emprestimos = response_emprestimos.json()
            return dados_emprestimos
        else:
            msg_error.open = True

    def lista_usuarios():
        url = 'http://10.135.232.20:5000/usuarios'
        response_usuarios = requests.get(url)

        if response_usuarios.status_code == 200:
            dados_usuario = response_usuarios.json()
            return dados_usuario["usuarios"]
        else:
            msg_error.open = True

    def lista_status():
        url = 'http://10.135.232.20:5000/status_livro'
        response_status = requests.get(url)

        if response_status.status_code == 200:
            dados_emprestimo = response_status.json()
            return dados_emprestimo
        else:
            msg_error.open = True

    # def get_livro(id):
    #     url = f'http://10.135.232.9:5000/get_livro/{id}'
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         dados_get_postagem = response.json()
    #         print(dados_get_postagem)
    #     else:
    #         print(f'Erro: {response.status_code}')


    def emprestimo_por_usuario():
        print("lllllllllllll")
        global id_emprestimo_usuario_global
        url = f'http://10.135.232.20:5000/emprestimos_usuario/{id_emprestimo_usuario_global}'
        response_emprestimo_usuario = requests.get(url)

        if response_emprestimo_usuario.status_code == 200:
            dados_emprestimo_usuario = response_emprestimo_usuario.json()
            print(dados_emprestimo_usuario["emprestimos"])
            return dados_emprestimo_usuario['emprestimos']
        else:
            msg_error.open = response_emprestimo_usuario.json()
            msg_error.open = True
            print(response_emprestimo_usuario.json())
            return response_emprestimo_usuario
    #
    # def get_livro():
    #     global id_livro_global
    #     url = f'http://10.135.232.20:5000/get_usuario/{id_livro_global}'
    #     response_get_livro = requests.get(url)
    #
    #     if response_get_livro.status_code == 200:
    #         dados_get_livro = response_get_livro.json()
    #         print(dados_get_livro["emprestimos"])
    #         return dados_get_livro
    #     else:
    #         msg_error.open = response_get_livro.json()
    #         msg_error.open = True
    #         return response_get_livro

    def atualizar_livros():
        global id_livro_global
        print(id_livro_global)
        url = f'http://10.135.232.20:5000/editar_livro/{id_livro_global}'

        livro_atualizado = {
            'titulo': input_titulo.value,
            'isbn': input_isbn.value,
            'resumo': input_resumo.value,
            'autor': input_autor.value,
        }

        response = requests.put(url, json=livro_atualizado)

        if response.status_code == 200:
            page.go("/lista_livro")
            page.update()
        else:
            print(f' Erro: {response.json()}')
            return {
                "error": response.json()
            }

    def popular_input_usuario(usuario):
        input_nome.value = usuario['nome']
        input_cpf.value = usuario['cpf']
        input_endereco.value = usuario['endereco']
        input_papel.value = usuario['papel']

        global id_usuario_global
        id_usuario_global = usuario['id']

        page.go("/editar_usuario")

    def popular_input_emprestimo(emprestimo):
        input_usuario_id.value = emprestimo['usuario_id']
        input_livro_id.value = emprestimo['livro_id']
        input_data_emprestimo.value = emprestimo['data_emprestimo']
        input_devolucao_prevista.value = emprestimo['data_devolucao_prevista']

        global id_emprestimo_global
        id_emprestimo_global = emprestimo['id']

        page.go("/editar_emprestimo")

    def popular_input_livro(livro):
        input_titulo.value = livro['titulo']
        input_isbn.value = livro['isbn']
        input_autor.value = livro['autor']
        input_resumo.value = livro['resumo']

        global id_livro_global
        id_livro_global = livro['id']

        page.go("/editar_livro")

    def popular_global_emprestimo_por_usuario(usuario):
        global id_emprestimo_usuario_global
        id_emprestimo_usuario_global = usuario['id']

        page.go("/lista_emprestimo_usuario")


    def atualizar_usuario():
        global id_usuario_global
        url = f'http://10.135.232.20:5000/editar_usuario/{id_usuario_global}'

        if input_nome == "" or input_cpf == "" or input_endereco == "" or input_papel == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            usuario_atualizado = {
                'nome': input_nome.value,
                'cpf': input_cpf.value,
                'endereco': input_endereco.value,
                'papel': input_papel.value,
            }

            response = requests.put(url, json=usuario_atualizado)

            if response.status_code == 200:
                page.go("/lista_usuario")
                page.update()
            else:
                return response.json()

    def atualizar_emprestimo():
        global id_emprestimo_global
        url = f'http://10.135.232.20:5000/editar_emprestimo/{id_emprestimo_global}'

        if input_data_emprestimo == "" or input_devolucao_prevista == "" or input_usuario_id == "" or input_livro_id == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()

        else:
            emprestimo_atualizado = {
                'livro_id': input_livro_id.value,
                'usuario_id': input_usuario_id.value,
                'data_emprestimo': input_data_emprestimo.value,
                'data_devolucao_prevista': input_devolucao_prevista.value
            }

            response = requests.put(url, json=emprestimo_atualizado)

            if response.status_code == 200:
                page.go("/lista_emprestimo")
                page.update()
            else:
                return {
                    "error": response.json()
                }


    def livros(e):
        lv.controls.clear()
        resultado_lista = lista_livros()
        for livro in resultado_lista:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f'Título: {livro["titulo"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, l=livro: detalhes_livro(l)),
                            ft.PopupMenuItem(text="EDITAR", on_click=lambda _, l=livro: popular_input_livro(l)),
                        ]
                    )
                )
            )

    def status(e):
        lv.controls.clear()
        resultado_status = lista_status()
        print(f' Status: {resultado_status["livros_emprestados"]}')
        for status in resultado_status['livros_emprestados']:
            lv_emprestados.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK_OUTLINED),
                    title=ft.Text(f'Título: {status["titulo"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, l=status: lista_status()),
                        ]
                    )
                )
            )

        for status_disponiveis in resultado_status['livros_disponiveis']:
            lv_disponiveis.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f'Título: {status_disponiveis["titulo"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, l=status: lista_status()),
                        ]
                    )
                )
            )

    def emprestimos_usuarios():
        lv.controls.clear()
        resultado_emprestimo_user = emprestimo_por_usuario()
        print(f' Emprestimo por usuário: {resultado_emprestimo_user}')
        for lista_por_usuario in resultado_emprestimo_user:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK_OUTLINED),
                    title=ft.Text(f'ID do usuário: {lista_por_usuario['usuario_id']}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, l=lista_por_usuario: detalhes_emprestimo(l)),
                        ]
                    )
                )
            )


    def emprestimos(e):
        lv.controls.clear()
        resultado_emprestimo = lista_emprestimos()
        print(f' Livros: {resultado_emprestimo["emprestimos"]}')
        for emprestimo in resultado_emprestimo['emprestimos']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f'Livro id: {emprestimo["livro_id"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, em=emprestimo: detalhes_emprestimo(em)),
                            ft.PopupMenuItem(text="EDITAR", on_click=lambda _, em=emprestimo: popular_input_emprestimo(em)),
                        ]
                    )
                )
            )

    def usuarios(e):
        lv.controls.clear()
        resultado_usuario = lista_usuarios()
        print(f' Usuarios: {resultado_usuario}')
        for usuario in resultado_usuario:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(f'Usuario: {usuario["nome"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES",
                                             on_click=lambda _, u=usuario: detalhes_usuario(u)),
                            ft.PopupMenuItem(text="EMPRESTIMOS",
                                             on_click=lambda _, u=usuario: popular_global_emprestimo_por_usuario(u)),
                            ft.PopupMenuItem(text="EDITAR",
                                             on_click=lambda _, u=usuario: popular_input_usuario(u)),
                        ]
                    )
                )
            )



    def gerenciar_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                (
                    ft.Container(
                        ft.Image(src="livro.png"),
                        margin=30,
                    ),

                    ElevatedButton(text="Cadastrar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/cadastros"),
                                       bgcolor=Colors.BLACK),

                    ElevatedButton(
                        text="Listar",
                        color=ft.Colors.BLACK,
                        on_click=lambda _: page.go("/listas"),
                        bgcolor=Colors.WHITE,
                    ),

                    ElevatedButton(
                        text="Status",
                        color=ft.Colors.WHITE,
                        on_click=lambda _: page.go("/status"),
                        bgcolor=Colors.BLACK,
                    ),
                ),
                bgcolor="#213D85",
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/cadastros":
            page.views.append(
                View(
                    "/cadastros",
                    [
                        AppBar(title=Text("Cadastros"), bgcolor="#2CC3FF"),
                        ElevatedButton(text="Livro",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/cadastrar_livro"),
                                       bgcolor="#2C30FF",
                                       width=page.window.width),

                        ElevatedButton(text="Usuário",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/cadastrar_usuario"),
                                       bgcolor="#2CC3FF",
                                       width=page.window.width),

                        ElevatedButton(text="Empréstimo",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/cadastrar_emprestimo"),
                                       bgcolor="#2C30FF",
                                       width=page.window.width)

                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/cadastrar_livro":
            page.views.append(
                View(
                    "/cadastrar_livro",
                    [
                        AppBar(title=Text("Cadastrar Livro"), bgcolor="#2CC3FF"),
                        input_titulo,
                        input_autor,
                        input_resumo,
                        input_isbn,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_livro(e),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width),
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/cadastros"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )


        if page.route == "/editar_usuario":
            page.views.append(
                View(
                    "/editar_usuario",
                    [
                        AppBar(title=Text("Editar usuário"), bgcolor="#2CC3FF"),
                        input_nome,
                        input_cpf,
                        input_endereco,
                        input_papel,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: atualizar_usuario(),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width),
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/lista_usuario"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width),

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/editar_livro":
            page.views.append(
                View(
                    "/editar_livro",
                    [
                        AppBar(title=Text("Editar livro"), bgcolor="#2CC3FF"),
                        input_titulo,
                        input_isbn,
                        input_autor,
                        input_resumo,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: atualizar_livros(),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width),
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/lista_livro"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width),

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/editar_emprestimo":
            page.views.append(
                View(
                    "/editar_emprestimo",
                    [
                        AppBar(title=Text("Editar emprestimo"), bgcolor="#2CC3FF"),
                        input_livro_id,
                        input_usuario_id,
                        input_data_emprestimo,
                        input_devolucao_prevista,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: atualizar_emprestimo(),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width),
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/lista_emprestimo"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width),

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/cadastrar_emprestimo":
            page.views.append(
                View(
                    "/cadastrar_emprestimo",
                    [
                        AppBar(title=Text("Cadastrar Emprestimo"), bgcolor="#2CC3FF"),
                        input_livro_id,
                        input_usuario_id,
                        input_data_emprestimo,
                        input_devolucao_prevista,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_emprestimo(e),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width),
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/cadastros"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/cadastrar_usuario":
            page.views.append(
                View(
                    "/cadastrar_usuario",
                    [
                        AppBar(title=Text("Cadastrar Usuário"), bgcolor="#6EC2F6"),
                        input_nome,
                        input_cpf,
                        input_endereco,
                        input_papel,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_usuario(e),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width),
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/cadastros"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/listas":
            page.views.append(
                View(
                    "/listas",
                    [
                        AppBar(title=Text("Listas"), bgcolor="#2CC3FF"),
                        ElevatedButton(text="Livro",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/lista_livro"),
                                       bgcolor="#2C30FF",
                                       width=page.window.width),

                        ElevatedButton(text="Usuário",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/lista_usuario"),
                                       bgcolor="#2CC3FF",
                                       width=page.window.width),

                        ElevatedButton(text="Empréstimo",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/lista_emprestimo"),
                                       bgcolor="#2C30FF",
                                       width=page.window.width)

                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/lista_livro":
            livros(e)
            page.views.append(
                View(
                    "/lista_livro",
                    [
                        AppBar(title=Text("Livros"), bgcolor="#2CC3FF"),
                        lv,
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/listas"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)
                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/lista_emprestimo_usuario":
            emprestimos_usuarios()
            page.views.append(
                View(
                    "/lista_emprestimo_usuario",
                    [
                        AppBar(title=Text("Emprestimo por usuário"), bgcolor="#2CC3FF"),
                        lv,
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/listas"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)
                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/lista_usuario":
            usuarios(e)
            page.views.append(
                View(
                    "/lista_usuario",
                    [
                        AppBar(title=Text("Usuários"), bgcolor="#2CC3FF"),
                        lv,
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/listas"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)
                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/lista_emprestimo":
            emprestimos(e)
            page.views.append(
                View(
                    "/lista_emprestimo",
                    [
                        AppBar(title=Text("Emprestimos"), bgcolor="#2CC3FF"),
                        lv,
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/listas"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)
                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )


        if page.route == "/detalhes_livros":
            page.views.append(
                View(
                    "/detalhes_livros",
                    [
                        AppBar(title=Text("Detalhes"), bgcolor="#2CC3FF"),
                        txt_titulo,
                        txt_resumo,
                        txt_isbn,
                        txt_autor,
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/lista_livro"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)
                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/detalhes_usuario":
            page.views.append(
                View(
                    "/detalhes_usuario",
                    [
                        AppBar(title=Text("Detalhes"), bgcolor="#2CC3FF"),
                        txt_nome,
                        txt_cpf,
                        txt_endereco,
                        txt_papel,
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/lista_usuario"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)
                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/detalhes_emprestimo":
            page.views.append(
                View(
                    "/detalhes_emprestimo",
                    [
                        AppBar(title=Text("Detalhes"), bgcolor="#2CC3FF"),
                        txt_livroID,
                        txt_usuarioID,
                        txt_data_emprestimo,
                        txt_previsao_devolucao,
                        ElevatedButton(text="Voltar",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/lista_emprestimo"),
                                       bgcolor=Colors.WHITE,
                                       width=page.window.width)
                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/status":
            status(e)
            page.views.append(
                View(
                    "/status",
                    [
                        AppBar(title=Text("Status"), bgcolor="#2CC3FF"),
                        text_disponiveis,
                        lv_disponiveis,
                        text_emprestados,
                        lv_emprestados,
                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                )
            )

        page.update()

    # Criação de componentes
    input_titulo = ft.TextField(label="Titulo", hint_text="Digite o título do livro")
    input_isbn = ft.TextField(label="ISBN", hint_text="Digite o ISBN")
    input_resumo = ft.TextField(label="Resumo", hint_text="Digite um breve resumo")
    input_autor = ft.TextField(label="Autor", hint_text="Digite o autor")

    text_disponiveis = ft.Text(value="Disponíveis", color=Colors.WHITE, size=20, weight=FontWeight.BOLD)
    text_emprestados = ft.Text(value="Emprestados", color=Colors.WHITE,  size=20, weight=FontWeight.BOLD)

    input_nome = ft.TextField(label="Nome", hint_text="Digite seu nome")
    input_cpf = ft.TextField(label="CPF", hint_text="Digite o seu CPF")
    input_endereco = ft.TextField(label="Endereço", hint_text="Digite o seu endereço")
    input_papel = ft.TextField(label="Papel", hint_text="Digite o seu papel")

    resultado_lista_livro = lista_livros()
    print(resultado_lista_livro)

    options = [Option(key=livro["id"], text=livro["titulo"]) for livro in resultado_lista_livro]

    input_livro_id = ft.Dropdown(
        label="Id do livro",
        width=page.window.width,
        options=options,)


    resultado_lista_usuario = lista_usuarios()
    print(resultado_lista_usuario)

    options = [Option(key=usuario["id"], text=usuario["nome"])for usuario in resultado_lista_usuario]

    input_usuario_id = ft.Dropdown(label="Id do usuário",
                                   width=page.window.width,
                                    fill_color="#213D85",
                                   options=options,
                                   filled=True)

    input_devolucao_prevista = ft.TextField(label="Data prevista para devolução", hint_text="Digite a data prevista de devolução")
    input_data_emprestimo = ft.TextField(label="Data do empréstimo", hint_text="Digite a data do empréstimo")

    lv = ft.ListView(
        height=500
    )

    lv_disponiveis = ft.ListView(
        height=250
    )

    lv_emprestados = ft.ListView(
        height=250
    )

    msg_sucesso = ft.SnackBar(
        bgcolor=Colors.GREEN,
        content=ft.Text("Informações salvas com sucesso")
    )

    msg_error = ft.SnackBar(
        bgcolor=Colors.RED,
        content=ft.Text("Dados não inseridos não podem ser salvos")
    )

    txt_titulo = ft.Text('Titulo:')
    txt_isbn = ft.Text()
    txt_autor = ft.Text()
    txt_resumo = ft.Text()

    txt_nome = ft.Text()
    txt_cpf = ft.Text()
    txt_endereco = ft.Text()
    txt_papel = ft.Text()


    txt_livroID = ft.Text()
    txt_usuarioID = ft.Text()
    txt_previsao_devolucao = ft.Text()
    txt_data_emprestimo = ft.Text()

    page.on_route_change = gerenciar_rotas
    page.go(page.route)


ft.app(main)