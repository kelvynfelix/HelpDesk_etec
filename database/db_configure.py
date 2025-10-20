from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy.orm import relationship

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_folder = os.path.join(BASE_DIR, "database")
os.makedirs(db_folder, exist_ok=True)
caminho_db = os.path.join(db_folder, "db_etec.db")
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
    pendente = Column("pendente", Boolean, default=True)
    descricao = Column("descricao", String, nullable=False)
    anexos = relationship("Anexo", back_populates="chamado")

    def __init__(self, nome, local, data, pc, descricao, anexos=None, pendente=True):
        self.nome = nome
        self.local = local
        self.data = data
        self.pc = pc
        self.pendente = pendente
        self.descricao = descricao
        self.anexos = anexos or []


class Aluno(Base):
    __tablename__ = "alunos"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String)
    nome = Column("nome", String)
    senha = Column("senha", String)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


class Anexo(Base):
    __tablename__ = "anexos"

    id = Column(Integer, primary_key=True)
    nome_arquivo = Column("Nome_Anexo", String)
    conteudo = Column("conteudo", LargeBinary)
    chamado_id = Column("chamadoID", Integer, ForeignKey("chamados.id"))

    chamado = relationship("Chamado", back_populates="anexos")


Base.metadata.create_all(bind=db)
