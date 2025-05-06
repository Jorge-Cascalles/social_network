from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from ..modelo.models import User, Post
from ..modelo.database import get_graph
from .auth import get_current_user

router = APIRouter()

class PostCreate(BaseModel):
    titulo: str
    conteudo: str
    imagem_url: Optional[str] = None

class PostResponse(BaseModel):
    id: str
    titulo: str
    conteudo: str
    imagem_url: Optional[str]
    data_criacao: str
    autor: dict

@router.post("/posts", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user)
):
    graph = get_graph()
    post = Post(
        titulo=post_data.titulo,
        conteudo=post_data.conteudo,
        imagem_url=post_data.imagem_url
    )
    post.criado_por.add(current_user)
    graph.create(post)
    
    return {
        "id": post.id,
        "titulo": post.titulo,
        "conteudo": post.conteudo,
        "imagem_url": post.imagem_url,
        "data_criacao": post.data_criacao,
        "autor": {
            "email": current_user.email,
            "nome": current_user.nome,
            "foto": current_user.foto
        }
    }

@router.get("/timeline", response_model=List[PostResponse])
async def get_timeline(current_user: User = Depends(get_current_user)):
    graph = get_graph()
    query = """
    MATCH (u:User {email: $email})-[:AMIGO_DE]->(friend:User)-[:CRIADO_POR]->(p:Post)
    RETURN p, friend
    ORDER BY p.data_criacao DESC
    """
    results = graph.run(query, email=current_user.email)
    
    posts = []
    for record in results:
        post = record["p"]
        author = record["friend"]
        posts.append({
            "id": post["id"],
            "titulo": post["titulo"],
            "conteudo": post["conteudo"],
            "imagem_url": post["imagem_url"],
            "data_criacao": post["data_criacao"],
            "autor": {
                "email": author["email"],
                "nome": author["nome"],
                "foto": author["foto"]
            }
        })
    
    return posts

@router.post("/users/{email}/friend-request")
async def send_friend_request(
    email: str,
    current_user: User = Depends(get_current_user)
):
    if email == current_user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send friend request to yourself"
        )
    
    graph = get_graph()
    target_user = User.match(graph, email).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if friendship already exists
    query = """
    MATCH (u1:User {email: $email1})-[r:AMIGO_DE]->(u2:User {email: $email2})
    RETURN r
    """
    result = graph.run(query, email1=current_user.email, email2=email).data()
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Friendship already exists"
        )
    
    # Create friendship
    current_user.amigos.add(target_user)
    graph.push(current_user)
    
    return {"message": "Friend request sent successfully"}

@router.get("/users/search")
async def search_users(
    query: str,
    current_user: User = Depends(get_current_user)
):
    graph = get_graph()
    search_query = """
    MATCH (u:User)
    WHERE u.nome CONTAINS $query OR u.email CONTAINS $query
    RETURN u
    LIMIT 10
    """
    results = graph.run(search_query, query=query)
    
    users = []
    for record in results:
        user = record["u"]
        users.append({
            "email": user["email"],
            "nome": user["nome"],
            "foto": user["foto"]
        })
    
    return users 