import customtkinter as ctk
from database import db_configure as mydb
from database.db_configure import Admin
from utils.auth import codigo
from tkinter import filedialog
import tkinter as tk
import os


def tela_auth():
    tela_autencicacao = ctk.CTkToplevel(app)
    tela_autencicacao.geometry("500x400")
    tela_autencicacao.title("Autenticação de 2 fatores")

    def verificar_codigo_auth():
        codigo_digitado = campo_codigo.get()
        if codigo.verify(codigo_digitado):
            resultado_auth.configure(text="Autenticação bem sucedida!", text_color="green")
        else:
            resultado_auth.configure(text="Autenticação falhou", text_color="red")

    campo_codigo = ctk.CTkEntry(tela_autencicacao, placeholder_text="digite seu codigo aqui", width=220, height=70,
                                font=("Arial", 18), justify="center")
    campo_codigo.place(x=(500 - 220) / 2, y=150)

    btn_auth = ctk.CTkButton(tela_autencicacao, text="Verificar", width=140, height=30, command=verificar_codigo_auth)
    btn_auth.place(x=(500 - 140) / 2, y=240)
    resultado_auth = ctk.CTkLabel(tela_autencicacao, text="")
    resultado_auth.place(x=190, y=325)


# noinspection PyTypeChecker


def abrir_login_admin():
    app.withdraw()

    def verificar_login():
        email_digitado = campo_email.get()
        senha_digitada = campo_senha.get()
        admin_db = mydb.session.query(Admin).filter_by(email=email_digitado, senha=senha_digitada).first()
        if admin_db:
            if email_digitado == admin_db.email and senha_digitada == admin_db.senha:
                tela_auth()
                mostrar_mensagem_app("Login feito com sucesso!", "green")
            else:
                mostrar_mensagem_app("Login incorreto!")
        else:
            mostrar_mensagem_app("Usuário não encontrado!")

    # noinspection PyTypeChecker
    def mostrar_mensagem_app(texto, cor="red"):
        resultado_login.configure(text=texto, text_color=cor)
        app.after(2000, lambda: resultado_login.configure(text=""))

    tela_login_admin = ctk.CTkToplevel(app)
    tela_login_admin.geometry("300x300")
    tela_login_admin.title("Login de Administrador")
    label_email = ctk.CTkLabel(tela_login_admin, text="Email: ")
    label_email.pack(pady=10)
    campo_email = ctk.CTkEntry(tela_login_admin, placeholder_text="Digite seu email", width=200)
    campo_email.pack(pady=10)
    label_senha = ctk.CTkLabel(tela_login_admin, text="Senha: ")
    label_senha.pack(pady=10)
    campo_senha = ctk.CTkEntry(tela_login_admin, placeholder_text="Digite sua senha", show="*", width=200)
    campo_senha.pack(pady=10)
    botao_login = ctk.CTkButton(tela_login_admin, text="login", command=verificar_login)
    botao_login.pack(pady=10)
    resultado_login = ctk.CTkLabel(tela_login_admin, text="")
    resultado_login.pack(pady=10)


# Criação da GUI
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Sistema de login")
app.geometry("800x780")
app.resizable(False, False)

card = ctk.CTkFrame(app, corner_radius=15, width=450, height=750)
card.pack(pady=30)
card.pack_propagate(False)

label_chamados_titulo = ctk.CTkLabel(card, text="Chamados", text_color="#00BFFF", font=("Arial", 18, "bold"))
label_chamados_titulo.pack(pady=10)
label_nome = ctk.CTkLabel(card, text="Nome Completo:", text_color="#898989")
label_nome.pack(side="top", anchor="w", padx="100")
campo_nome = ctk.CTkEntry(card, placeholder_text="Digite seu nome Completo", width=300, justify="center", height=40)
campo_nome.pack()

label_num_pc = ctk.CTkLabel(card, text="Número do pc:", text_color="#898989")
label_num_pc.pack(side="top", anchor="w", padx="100")

campo_num_pc = ctk.CTkEntry(card, placeholder_text="Informe o número da maquina com problema", width=300,
                            justify="center", height=40)
campo_num_pc.pack()

label_obs_num_pc = ctk.CTkLabel(card, text="Esse número fica identificado no topo da maquina, em branco.",
                                text_color="#898989", font=("Arial", 10, "bold"))
label_obs_num_pc.pack()

frame_local = ctk.CTkFrame(card, fg_color="transparent")
frame_local.pack(pady=(5, 0))

label_opc_local = ctk.CTkLabel(frame_local, text="Local do problema:", text_color="#898989")
label_opc_local.pack(pady=(0, 5))

locais = ["laboratório 1", "laboratório 2", "laboratório 3", "laboratório 4", "Sala Maker", "Outro"]


def ao_mudar_local(valor):
    if valor == "Outro":
        label_outra_opc.pack(pady=(10, 0))
        campo_outra_opc.pack(pady=(0, 10))
        return True
    else:
        label_outra_opc.pack_forget()
        campo_outra_opc.pack_forget()
        return False


options_local = ctk.CTkOptionMenu(frame_local, values=locais, command=ao_mudar_local, width=180)
options_local.set("Selecione o Local")
options_local.pack()

label_outra_opc = ctk.CTkLabel(frame_local, text="Outro local:", text_color="#898989")
campo_outra_opc = ctk.CTkEntry(frame_local, placeholder_text="Digite o Local", width=250, height=35)

frame_textarea = ctk.CTkFrame(card, corner_radius=10)
frame_textarea.pack(padx=35, pady=10, fill="both", expand=True)

campo_descricao = tk.Text(
    frame_textarea,
    width=50,
    height=8,
    wrap="word",
    font=("Arial", 13),
    bg="#333333",
    fg="white",
    insertbackground="white",
    bd=0

)
campo_descricao.pack(padx=5, pady=5)
campo_descricao.pack_propagate(False)

placeholder = "Descreva o problema encontrado no computador..."
campo_descricao.insert("1.0", placeholder)


def on_focus_in(event):
    if campo_descricao.get("1.0", "end-1c") == placeholder:
        campo_descricao.delete("1.0", "end")


def on_focus_out(event):
    if campo_descricao.get("1.0", "end-1c").strip() == "":
        campo_descricao.insert("1.0", placeholder)


def abrir_popup(mensagem, txt_btn="OK", titulo="Aviso", tamanho="400x170", expansivel=False):
    popup = ctk.CTkToplevel(app)
    popup.title(titulo)
    popup.geometry(tamanho)
    popup.resizable(expansivel, expansivel)

    # ctk.CTkLabel(popup, text=mensagem).pack(pady=20)
    # ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=10)
    popup.grab_set()  # impede interação com a janela principal
    popup.attributes("-topmost", True)
    frame_msg = ctk.CTkFrame(popup, fg_color="transparent")
    frame_msg.pack(pady=15, padx=10, fill="x")

    # Ícone de aviso
    icone_label = ctk.CTkLabel(frame_msg, text="⚠️", font=("Arial", 30))
    icone_label.pack(side="left", padx=10)

    msg_label = ctk.CTkLabel(frame_msg, text=mensagem, font=("Arial", 12))
    msg_label.pack(side="left", padx=10)

    btn_ok = ctk.CTkButton(popup, text=txt_btn, width=110, command=popup.destroy)
    btn_ok.pack(pady=10)


# noinspection PyGlobalUndefined
def limpar_formulario():
    global caminho_anexo
    for campo in [campo_nome, campo_num_pc, campo_outra_opc]:  # apenas Entry aqui
        campo.delete(0, "end")
    campo_descricao.delete("1.0", "end")
    options_local.set("Selecione o Local")
    caminho_anexo = None
    label_ver_anexo.configure(text="Nenhum arquivo anexado", text_color="white")


def enviar_chamado():
    nome_digitado = campo_nome.get()
    num_pc_digitado = campo_num_pc.get()
    local_escolhido = options_local.get()
    outro_local_digitado = campo_outra_opc.get()
    descricao_digitada = campo_descricao.get("1.0", "end-1c")

    if nome_digitado == "":
        abrir_popup("É necessário preencher o campo nome")
        return
    elif num_pc_digitado == "":
        abrir_popup("É necessário preencher o campo número da máquina")
        return
    elif local_escolhido == "Selecione o Local":
        abrir_popup("Você deve selecionar um Local!")
        return
    elif outro_local_digitado == "" and local_escolhido == "Outro":
        abrir_popup("É necessário preencher o campo Local")
        return
    elif descricao_digitada == "":
        abrir_popup("É necessário preencher o campo com uma descrição")
        return
    limpar_formulario()
    # Configuração de envio para o DB
    #teste

campo_descricao.bind("<FocusIn>", on_focus_in)
campo_descricao.bind("<FocusOut>", on_focus_out)

label_anexo = ctk.CTkLabel(card, text="Anexo (opcional):", text_color="#898989")
label_anexo.pack()


def anexar_arquivo():
    global label_ver_anexo
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[("Todos os arquivos", "*.*")]
    )
    nome_arquivo = os.path.basename(caminho)
    label_ver_anexo.configure(text=f"arquivo anexado: {nome_arquivo}", text_color="#90EE90")


botao = ctk.CTkButton(card, text="Anexar arquivo", command=anexar_arquivo)
botao.pack(pady=10)
label_ver_anexo = ctk.CTkLabel(card, text="Nenhum arquivo Anexado")
label_ver_anexo.pack(pady=3)
btn_enviar_chamado = ctk.CTkButton(card, text="Enviar Chamado", command=enviar_chamado)
btn_enviar_chamado.pack(pady=10)

btn_abrir_Login_admin = ctk.CTkButton(app, text="Login Admin", command=abrir_login_admin)
btn_abrir_Login_admin.place(x=645, y=35)

app.mainloop()
