from fastapi.testclient import TestClient
from backend.main import app # Supondo que seu app FastAPI esteja em backend/main.py
from backend.testes.auth import registrar_novo_usuario # Importar a função auxiliar
from backend.testes.auth import UserCreate
from backend.testes.auth import login

client = TestClient(app)

TITULO_TESTE = "Meu Primeiro Post de Teste"
CONTEUDO_TESTE = "Este é o conteúdo do meu primeiro post de teste."
IMAGEM_URL_TESTE = "http://example.com/image.jpg"
EMAIL_TESTE = "testuser_post@example.com"
NOME_TESTE = "Usuário Criador de Post"
SENHA_TESTE = "senhaSegura123"

def test_create_post():
    # 1. Registrar um novo usuário para obter um token
    user: UserCreate = UserCreate(email=EMAIL_TESTE, nome=NOME_TESTE, senha=SENHA_TESTE)
    assert registrar_novo_usuario(client, user)
    headers = {"Authorization": f"Bearer {user.token}"}
    # 2. Criar o post usando o token do usuário registrado
    post_data = {
        "titulo": TITULO_TESTE,
        "conteudo": CONTEUDO_TESTE,
        "imagem_url": IMAGEM_URL_TESTE
    }
    response = client.post("/posts", json=post_data, headers=headers)   
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["titulo"] == TITULO_TESTE
    assert response_json["conteudo"] == CONTEUDO_TESTE
    assert response_json["imagem_url"] == IMAGEM_URL_TESTE   
    # 3. Verificar se o autor do post é o usuário que o criou
    assert response_json["autor"]["email"] == EMAIL_TESTE 

# def test_novo_usuario():
#     assert registrar_novo_usuario(
#         client, UserCreate(
#             email=EMAIL_TESTE, nome=NOME_TESTE, senha=SENHA_TESTE
#         )
#     )

# def test_login():
#     assert login(
#         client, UserCreate(
#             email=EMAIL_TESTE, nome=NOME_TESTE, senha=SENHA_TESTE
#         )
#     )

