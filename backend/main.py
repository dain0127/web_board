from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import pymysql
import os

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend", "templates"))

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='black72',  # 본인 MySQL 비밀번호로 변경
        database='board_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
def board_list(request: Request):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = cur.fetchall()
    conn.close()
    return templates.TemplateResponse("list.html", {"request": request, "posts": posts})

@app.get("/write")
def write_form(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})

@app.post("/write")
def write_post(title: str = Form(...), author: str = Form(...), content: str = Form(...)):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO posts (title, author, content) VALUES (%s, %s, %s)", (title, author, content))
        conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=302)

@app.get("/view/{post_id}")
def view_post(request: Request, post_id: int):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cur.fetchone()
    conn.close()
    return templates.TemplateResponse("view.html", {"request": request, "post": post})

@app.get("/edit/{post_id}")
def edit_form(request: Request, post_id: int):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cur.fetchone()
    conn.close()
    return templates.TemplateResponse("edit.html", {"request": request, "post": post})

@app.post("/edit/{post_id}")
def edit_post(post_id: int, title: str = Form(...), author: str = Form(...), content: str = Form(...)):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("UPDATE posts SET title=%s, author=%s, content=%s WHERE id=%s", (title, author, content, post_id))
        conn.commit()
    conn.close()
    return RedirectResponse(f"/view/{post_id}", status_code=302)

@app.get("/delete/{post_id}")
def delete_post(post_id: int):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM posts WHERE id=%s", (post_id,))
        conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=302) 