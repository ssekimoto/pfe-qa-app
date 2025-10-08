
import os
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# --- インメモリDB ---
class Post(BaseModel):
    id: int
    title: str
    content: str

class PostCreate(BaseModel):
    title: str
    content: str

db: Dict[int, Post] = {
    1: Post(id=1, title="FastAPI入門", content="FastAPIは高速なWebフレームワークです。"),
    2: Post(id=2, title="geminiCLIの使い方", content="geminiCLIはコマンドラインからGeminiを利用できます。"),
}
next_post_id = 3

@app.get("/api/posts", response_model=List[Post])
async def get_posts():
    """全記事を取得"""
    return list(db.values())

@app.get("/api/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    """IDを指定して単一記事を取得"""
    post = db.get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@app.post("/api/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_create: PostCreate):
    """新しい記事を作成"""
    global next_post_id
    new_post = Post(id=next_post_id, title=post_create.title, content=post_create.content)
    db[next_post_id] = new_post
    next_post_id += 1
    return new_post

@app.put("/api/posts/{post_id}", response_model=Post)
async def update_post(post_id: int, post_update: PostCreate):
    """IDを指定して記事を更新"""
    if post_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post = db[post_id]
    post.title = post_update.title
    post.content = post_update.content
    db[post_id] = post
    return post

@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    """IDを指定して記事を削除"""
    if post_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    del db[post_id]
    return

@app.get("/")
async def read_root():
    """フロントエンドのHTMLを返す"""
    return FileResponse('index.html')
