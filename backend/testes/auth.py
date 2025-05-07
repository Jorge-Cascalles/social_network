from fastapi.testclient import TestClient
from ..rotas.auth import register, UserCreate
import uuid # Para gerar emails únicos

# Poderíamos também definir dados de usuário padrão aqui ou passá-los como argumentos
DEFAULT_TEST_USER_NOME = "Usuário de Teste"
DEFAULT_TEST_USER_SENHA = "senhaSegura123"

def registrar_novo_usuario(client: TestClient, user_data: UserCreate) -> bool:
    """
    Registra um novo usuário e retorna os dados da resposta, incluindo o token de acesso.
    """
    response = client.post("/register", json=user_data)
    user_data.token = response.json()["access_token"]
    return response.status_code == 200
