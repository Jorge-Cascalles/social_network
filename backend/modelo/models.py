from py2neo.ogm import GraphObject, Property, RelatedTo
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(GraphObject):
    __primarykey__ = "email"

    email = Property()
    nome = Property()
    foto = Property()
    senha_hash = Property()
    data_criacao = Property()

    amigos = RelatedTo("User", "AMIGO_DE")
    postagens = RelatedTo("Post", "CRIADO_POR")

    def __init__(self, email, nome, senha, foto=None):
        self.email = email
        self.nome = nome
        self.senha_hash = pwd_context.hash(senha)
        self.foto = foto
        self.data_criacao = datetime.now().isoformat()

    def verificar_senha(self, senha):
        return pwd_context.verify(senha, self.senha_hash)

class Post(GraphObject):
    __primarykey__ = "id"

    id = Property()
    titulo = Property()
    conteudo = Property()
    imagem_url = Property()
    data_criacao = Property()

    criado_por = RelatedTo("User", "CRIADO_POR")
    respostas = RelatedTo("Post", "RESPONDE_A")

    def __init__(self, titulo, conteudo, imagem_url=None):
        self.id = str(datetime.now().timestamp())
        self.titulo = titulo
        self.conteudo = conteudo
        self.imagem_url = imagem_url
        self.data_criacao = datetime.now().isoformat() 