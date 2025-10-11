import customtkinter as ctk
from database import db_configure as mydb
from database.db_configure import Admin
from utils.auth import codigo


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


def tela_auth():
    tela_autencicacao = ctk.CTkToplevel(app)
    tela_autencicacao.geometry("500x400")
    tela_autencicacao.title("Autenticação de 2 fatores")

    def apagar_tela():
        tela_autencicacao.destroy()

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
def mostrar_mensagem_app(texto, cor="red"):
    resultado_login.configure(text=texto, text_color=cor)
    app.after(2000, lambda: resultado_login.configure(text=""))


ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Sistema de login")
app.geometry("300x300")

label_email = ctk.CTkLabel(app, text="Email: ")
label_email.pack(pady=10)
campo_email = ctk.CTkEntry(app, placeholder_text="Digite seu email", width=200)
campo_email.pack(pady=10)
label_senha = ctk.CTkLabel(app, text="Senha: ")
label_senha.pack(pady=10)
campo_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*", width=200)
campo_senha.pack(pady=10)

botao_login = ctk.CTkButton(app, text="login", command=verificar_login)
botao_login.pack(pady=10)
resultado_login = ctk.CTkLabel(app, text="")
resultado_login.pack(pady=10)

app.mainloop()
