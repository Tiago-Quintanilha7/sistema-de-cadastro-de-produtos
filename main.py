import tkinter as tk
from tkinter import messagebox
import json
import os

# Carregar os produtos do arquivo JSON
produtos = []
if os.path.exists("produtos.json"):
    with open("produtos.json", "r") as f:
        produtos = json.load(f)


# Função para excluir por código
def abrir_tela_excluir_codigo():
    janela_excluir = tk.Toplevel(janela)
    janela_excluir.title('Excluir produto por código')

    tk.Label(janela_excluir, text='Digite o código do produto:').pack(padx=10, pady=(10, 5))
    codigo_entry = tk.Entry(janela_excluir)
    codigo_entry.pack(padx=10, pady=5)

    # Pressionar Enter no campo também aciona a exclusão
    codigo_entry.bind("<Return>", lambda event: excluir_por_codigo(codigo_entry))

    tk.Button(janela_excluir, text='Excluir', command=lambda: excluir_por_codigo(codigo_entry)).pack(pady=10)


# Função para consultar produto por nome
def consultar_por_nome():
    nome_buscado = busca_nome_entry.get().strip()

    encontrados = [p for p in produtos if nome_buscado.lower() in p['nome'].lower()]

    if not encontrados:
        messagebox.showinfo("Consulta", "Nenhum produto encontrado com esse nome.")
        return

    janela_consulta = tk.Toplevel(janela)
    janela_consulta.title("Produtos Encontrados por Nome")

    for p in encontrados:
        info = f"Nome: {p['nome']}, Código: {p['codigo']}, Preço: {p['preco']}, Quantidade: {p['quantidade']}"
        tk.Label(janela_consulta, text=info).pack(anchor='w')


# Função para consultar produto por código
def consultar_por_codigo():
    codigo_buscado = busca_codigo_entry.get().strip()

    encontrados = [p for p in produtos if p['codigo'] == codigo_buscado]

    if not encontrados:
        messagebox.showinfo("Consulta", "Nenhum produto encontrado com esse código.")
        return

    janela_consulta = tk.Toplevel(janela)
    janela_consulta.title("Produtos Encontrados por Código")

    for p in encontrados:
        info = f"Nome: {p['nome']}, Código: {p['codigo']}, Preço: {p['preco']}, Quantidade: {p['quantidade']}"
        tk.Label(janela_consulta, text=info).pack(anchor='w')


# Função para excluir produto (recebe o entry de código como argumento)
def excluir_por_codigo(entry_codigo):
    codigo_buscado = entry_codigo.get().strip()

    if not codigo_buscado:
        messagebox.showwarning('Erro', 'Digite um código válido para excluir')
        return

    produto_encontrado = next((p for p in produtos if p['codigo'] == codigo_buscado), None)

    if not produto_encontrado:
        messagebox.showinfo('Não encontrado', 'Nenhum produto encontrado com esse código')
        return

    confirmar = messagebox.askyesno('Confirmação', f"Deseja excluir o produto '{produto_encontrado['nome']}'?")
    if not confirmar:
        return

    produtos.remove(produto_encontrado)

    with open('produtos.json', 'w') as f:
        json.dump(produtos, f, indent=4)

    messagebox.showinfo('Sucesso', 'Produto excluído com sucesso')


# Função para abrir a janela de cadastro
def abrir_tela_cadastro():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title('Cadastro de Produtos')

    tk.Label(janela_cadastro, text='Nome do Produto:').grid(row=0, column=0, padx=5, pady=5)
    nome_entry = tk.Entry(janela_cadastro)
    nome_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(janela_cadastro, text="Código do Produto:").grid(row=1, column=0, padx=5, pady=5)
    codigo_entry = tk.Entry(janela_cadastro)
    codigo_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(janela_cadastro, text="Preço do Produto:").grid(row=2, column=0, padx=5, pady=5)
    preco_entry = tk.Entry(janela_cadastro)
    preco_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(janela_cadastro, text="Quantidade:").grid(row=3, column=0, padx=5, pady=5)
    quantidade_entry = tk.Entry(janela_cadastro)
    quantidade_entry.grid(row=3, column=1, padx=5, pady=5)

    def cadastrar_produto():
        nome = nome_entry.get().strip()
        codigo = codigo_entry.get().strip()
        preco_texto = preco_entry.get().strip()
        quantidade_texto = quantidade_entry.get().strip()

        if not nome or not codigo or not preco_texto or not quantidade_texto:
            messagebox.showwarning('Erro', 'Preencha todos os campos')
            return

        try:
            preco = float(preco_texto)
            quantidade = int(quantidade_texto)
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser número decimal e Quantidade um número inteiro.")
            return

        for p in produtos:
            if p['codigo'] == codigo:
                messagebox.showerror("Erro", "Código já existe. Use outro código.")
                return

        novo_produto = {
            'nome': nome,
            'codigo': codigo,
            'preco': preco,
            'quantidade': quantidade
        }

        produtos.append(novo_produto)

        with open("produtos.json", "w") as f:
            json.dump(produtos, f, indent=4)

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

        nome_entry.delete(0, tk.END)
        codigo_entry.delete(0, tk.END)
        preco_entry.delete(0, tk.END)
        quantidade_entry.delete(0, tk.END)

    tk.Button(janela_cadastro, text="Salvar Produto", command=cadastrar_produto).grid(row=4, column=0, columnspan=2, pady=10)

    # Botão para excluir por código
    tk.Button(janela_cadastro, text='Excluir por Código', command=abrir_tela_excluir_codigo).grid(row=5, column=0, columnspan=2, pady=5)


# Criar a janela principal (Tela de Consulta)
janela = tk.Tk()
janela.title("CONTROLE DE ESTOQUE")
janela.geometry('300x220')
janela.config(bg='lightblue')
janela.resizable(False, False)

tk.Label(janela, text="Buscar Produto por Nome:", bg='lightblue').pack(pady=(10, 0))
busca_nome_entry = tk.Entry(janela, width=15)
busca_nome_entry.pack(pady=(0, 0))
busca_nome_entry.bind("<Return>", lambda event: consultar_por_nome())  # Enter ativa busca por nome
tk.Button(janela, text="Consultar por Nome", command=consultar_por_nome, bg='#98FB98').pack(pady=5)

tk.Label(janela, text="Buscar Produto por Código:", bg='lightblue').pack(pady=(10, 0))
busca_codigo_entry = tk.Entry(janela, width=10)
busca_codigo_entry.pack(pady=(0, 0))
busca_codigo_entry.bind("<Return>", lambda event: consultar_por_codigo())  # Enter ativa busca por código
tk.Button(janela, text="Consultar por Codigo", command=consultar_por_codigo, bg='#98FB98').pack(pady=5)

tk.Button(janela, text="Cadastrar ou Remover Produto", command=abrir_tela_cadastro, bg='#9370DB').pack(pady=10)

janela.mainloop()
