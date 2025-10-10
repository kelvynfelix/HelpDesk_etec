import customtkinter as ctk
from database import db_configure as mydb
from database.db_configure import Admin


def verificar_login():
    email_digitado = campo_email.get()
    senha_digitada = campo_senha.get()
    admin_db = mydb.session.query(Admin).filter_by(email=email_digitado, senha=senha_digitada).first()
    if admin_db:
        if email_digitado == admin_db.email and senha_digitada == admin_db.senha:
            mostrar_mensagem("Login feito com sucesso!", "green")
        else:
            mostrar_mensagem("Login incorreto!")
    else:
        mostrar_mensagem("Usuário não encontrado!")


# noinspection PyTypeChecker
def mostrar_mensagem(texto, cor="red"):
    resultado_login.configure(text=texto, text_color=cor)
    app.after(2000, lambda: resultado_login.configure(text=""))


ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Sistema de login")
app.geometry("300x300")

label_email = ctk.CTkLabel(app, text="Email: ")
label_email.pack(pady=10)
campo_email = ctk.CTkEntry(app, placeholder_text="Digite seu email")
campo_email.pack(pady=10)
label_senha = ctk.CTkLabel(app, text="Senha: ")
label_senha.pack(pady=10)
campo_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha")
campo_senha.pack(pady=10)

botao_login = ctk.CTkButton(app, text="login", command=verificar_login)
botao_login.pack(pady=10)
resultado_login = ctk.CTkLabel(app, text="")
resultado_login.pack(pady=10)

app.mainloop()
