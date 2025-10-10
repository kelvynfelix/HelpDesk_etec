from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import os

caminho_db = os.path.abspath("C:/Dev/Projetos/HelpDesk/database/db_etec.db")
db = create_engine(f"sqlite:///{caminho_db}")
Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()


class Admin(Base):
    __tablename__ = "admin"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    senha = Column("senha", String, nullable=False)
    email = Column("email", String, nullable=False)

    def __init__(self, nome, senha, email):
        self.nome = nome
        self.senha = senha
        self.email = email


class Chamado(Base):
    __tablename__ = "chamados"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    local = Column("local", String, nullable=False)
    data = Column("data", String, nullable=False)
    pc = Column("pc", String, nullable=False)
    pendente = Column("pendente", Boolean)
    descricao = Column("descricao", String, nullable=False)
    anexo = Column("anexo", Boolean)

    def __init__(self, nome, local, data, pc, descricao, anexo, pendente=True):
        self.nome = nome
        self.local = local
        self.data = data
        self.pc = pc
        self.pendente = pendente
        self.descricao = descricao
        self.anexo = anexo


Base.metadata.create_all(bind=db)
