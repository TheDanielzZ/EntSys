import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import registrar_entrada, registrar_saida, exportar_excel, fechar_conexao, buscar_setores
import os
import sys

def registrar_entrada_gui():
    placa_veiculo = entrada_placa_veiculo.get()
    placa_carreta = entrada_placa_carreta.get()
    motorista = entrada_motorista.get()
    cpf = entrada_cpf.get()
    nota_fiscal = entrada_nota_fiscal.get()
    setor = entrada_setor.get()
    transportadora = entrada_transportadora.get()
    empresa = entrada_empresa.get()
    agente = entrada_agente.get()
    if placa_veiculo and placa_carreta and motorista and cpf and nota_fiscal and setor and transportadora and empresa:
        registrar_entrada(placa_veiculo, placa_carreta, motorista, cpf, nota_fiscal, setor, transportadora, empresa, agente)
        messagebox.showinfo("Sucesso", f"Caminhão {placa_veiculo} registrado na entrada.")
        entrada_placa_veiculo.delete(0, tk.END)
        entrada_placa_carreta.delete(0, tk.END)
        entrada_motorista.delete(0, tk.END)
        entrada_cpf.delete(0, tk.END)
        entrada_nota_fiscal.delete(0, tk.END)
        entrada_setor.delete(0, tk.END)
        entrada_transportadora.delete(0, tk.END)
        entrada_empresa.delete(0, tk.END)
        entrada_agente.delete(0, tk.END)
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def registrar_saida_gui():
    placa_veiculo = saida_placa_veiculo.get()
    placa_carreta = saida_placa_carreta.get()
    if placa_veiculo and placa_carreta:
        try:
            registrar_saida(placa_veiculo, placa_carreta)
            messagebox.showinfo("Sucesso", f"Caminhão {placa_veiculo} registrado na saída.")
            saida_placa_veiculo.delete(0, tk.END)
            saida_placa_carreta.delete(0, tk.END)
        except ValueError as e:
            messagebox.showwarning("Erro", str(e))
    else:
        messagebox.showwarning("Erro", "Por favor, insira as placas do caminhão e da carreta.")

def exportar_excel_gui():
    exportar_excel()
    messagebox.showinfo("Sucesso", "Dados exportados para Excel.")

def sair_app():
    fechar_conexao()
    app.destroy()

app = tk.Tk()
app.title("Controle de Caminhões")

# Caminho da imagem .ico (compatível com tkinter)
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(base_path, "CIE.ico")
app.iconbitmap(icon_path)

# Frame principal com canvas e barra de rolagem
container = tk.Frame(app)
canvas = tk.Canvas(container, height=500)  # altura fixa, pode ajustar
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

container.pack(fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Colocando widgets dentro do frame rolável
tk.Label(scrollable_frame, text="Registrar Entrada").grid(row=0, column=0, padx=10, pady=10)
tk.Label(scrollable_frame, text="Placa Veículo").grid(row=1, column=0, padx=10, pady=10)
entrada_placa_veiculo = tk.Entry(scrollable_frame)
entrada_placa_veiculo.grid(row=1, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Placa Carreta").grid(row=2, column=0, padx=10, pady=10)
entrada_placa_carreta = tk.Entry(scrollable_frame)
entrada_placa_carreta.grid(row=2, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Motorista").grid(row=3, column=0, padx=10, pady=10)
entrada_motorista = tk.Entry(scrollable_frame)
entrada_motorista.grid(row=3, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="CPF").grid(row=4, column=0, padx=10, pady=10)
entrada_cpf = tk.Entry(scrollable_frame)
entrada_cpf.grid(row=4, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Nota Fiscal").grid(row=5, column=0, padx=10, pady=10)
entrada_nota_fiscal = tk.Entry(scrollable_frame)
entrada_nota_fiscal.grid(row=5, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Setor").grid(row=6, column=0, padx=10, pady=10)
setores = buscar_setores()
entrada_setor = ttk.Combobox(scrollable_frame, values=setores, state="readonly")
entrada_setor.grid(row=6, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Transportadora").grid(row=7, column=0, padx=10, pady=10)
entrada_transportadora = tk.Entry(scrollable_frame)
entrada_transportadora.grid(row=7, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Empresa").grid(row=8, column=0, padx=10, pady=10)
entrada_empresa = tk.Entry(scrollable_frame)
entrada_empresa.grid(row=8, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Agente").grid(row=9, column=0, padx=10, pady=10)
entrada_agente = tk.Entry(scrollable_frame)
entrada_agente.grid(row=9, column=1, padx=10, pady=10)

tk.Button(scrollable_frame, text="Registrar Entrada", command=registrar_entrada_gui).grid(row=10, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Registrar Saída").grid(row=11, column=0, padx=10, pady=10)
tk.Label(scrollable_frame, text="Placa Veículo").grid(row=12, column=0, padx=10, pady=10)
saida_placa_veiculo = tk.Entry(scrollable_frame)
saida_placa_veiculo.grid(row=13, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="Placa Carreta").grid(row=14, column=0, padx=10, pady=10)
saida_placa_carreta = tk.Entry(scrollable_frame)
saida_placa_carreta.grid(row=15, column=1, padx=10, pady=10)

tk.Button(scrollable_frame, text="Registrar Saída", command=registrar_saida_gui).grid(row=16, column=1, padx=10, pady=10)
tk.Button(scrollable_frame, text="Exportar para Excel", command=exportar_excel_gui).grid(row=17, column=1, padx=10, pady=10)
tk.Button(scrollable_frame, text="Sair", command=sair_app).grid(row=18, column=1, padx=10, pady=10)

app.protocol("WM_DELETE_WINDOW", sair_app)
# app.mainloop()
