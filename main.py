import tkinter as tk
from tkinter import messagebox

janela = tk.Tk()
janela.title("Cadastro de Produtos")

tk.Label(janela, text="Nome do Produto:").grid(row=0, column=0)
nome_entry = tk.Entry(janela)
nome_entry.grid(row=0, column=1)

tk.Label(janela, text="Código do Produto:").grid(row=1, column=0)
codigo_entry = tk.Entry(janela)
codigo_entry.grid(row=1, column=1)

tk.Label(janela, text="Preço do Produto:").grid(row=2, column=0)
preco_entry = tk.Entry(janela)
preco_entry.grid(row=2, column=1)

tk.Label(janela, text="Quantidade em Estoque:").grid(row=3, column=0)
quantidade_entry = tk.Entry(janela)
quantidade_entry.grid(row=3, column=1)

produtos = []  # Declarar antes de usar

def cadastrar_produto():
    nome = nome_entry.get()
    codigo = codigo_entry.get()
    preco = preco_entry.get()
    quantidade = quantidade_entry.get()

    if not nome or not codigo or not preco or not quantidade:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    produto = {
        "nome": nome,
        "codigo": codigo,
        "preco": preco,
        "quantidade": quantidade
    }

    def consultar_produtos():
        if not produtos:
            messagebox.showinfo("Consulta", "Nenhum produto cadastrado.")
            return

        janela_consulta = tk.Toplevel(janela)
        janela_consulta.title("Produtos Cadastrados")

        for i, p in enumerate(produtos):
            info = f"{i + 1}. Nome: {p['nome']}, Código: {p['codigo']}, Preço: {p['preco']}, Quantidade: {p['quantidade']}"
            tk.Label(janela_consulta, text=info).pack(anchor='w')

    tk.Button(janela, text="Consultar Produtos", command=consultar_produtos).grid(row=5, column=0, columnspan=2,
                                                                                  pady=10)
    produtos.append(produto)

    print("Produto cadastrado com sucesso!")
    print(produtos)

    nome_entry.delete(0, tk.END)
    codigo_entry.delete(0, tk.END)
    preco_entry.delete(0, tk.END)
    quantidade_entry.delete(0, tk.END)

tk.Button(janela, text="Cadastrar", command=cadastrar_produto).grid(row=4, column=0, columnspan=2)

#Botao para buscar produto pelo código
tk.Label(janela, text='Buscar por código:').grid(row=6, column=0)
busca_entry = tk.Entry(janela)
busca_entry.grid(row=6, column=1)

def buscar_produto():
    codigo_buscado = busca_entry.get()

    for p in produtos:
        if p["codigo"] == codigo_buscado:
            mensagem = f"Nome: {p['nome']}\nPreço: {p['preco']}\nQuantidade: {p['quantidade']}"
            messagebox.showinfo("Produto Encontrado", mensagem)
            return

    messagebox.showwarning("Não encontrado", "Produto com esse código não encontrado.")

tk.Button(janela, text="Buscar Produto", command=buscar_produto).grid(row=7, column=0, columnspan=2, pady=5)

janela.mainloop()
