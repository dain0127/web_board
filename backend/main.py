# FastAPI 웹 프레임워크와 필요한 모듈들을 가져옵니다
from fastapi import FastAPI, Form, Request
# 리다이렉트 응답을 위한 모듈을 가져옵니다
from fastapi.responses import RedirectResponse
# Jinja2 템플릿 엔진을 가져옵니다
from fastapi.templating import Jinja2Templates
# MySQL 데이터베이스 연결을 위한 모듈을 가져옵니다
import pymysql
# 운영체제 관련 기능을 사용하기 위한 모듈을 가져옵니다
import os

# FastAPI 애플리케이션 인스턴스를 생성합니다
app = FastAPI()
# 프로젝트의 기본 디렉토리 경로를 설정합니다
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Jinja2 템플릿 디렉토리를 설정합니다
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend", "templates"))

# 데이터베이스 연결을 생성하는 함수입니다
def get_db():
    # MySQL 데이터베이스에 연결합니다
    return pymysql.connect(
        host='localhost',  # 데이터베이스 호스트 주소
        user='root',  # 데이터베이스 사용자명
        password='black72',  # 본인 MySQL 비밀번호로 변경
        database='board_db',  # 사용할 데이터베이스명
        charset='utf8mb4',  # 문자 인코딩 설정
        cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리 형태로 반환
    )

'''
# 게시판 메인 페이지 (게시글 목록) 라우트
@app.get("/")
def board_list(request: Request):
    # 데이터베이스에 연결합니다
    conn = get_db()
    # 커서를 생성하여 SQL 쿼리를 실행합니다
    with conn.cursor() as cur:
        # 모든 게시글을 최신순으로 조회합니다
        cur.execute("SELECT * FROM posts ORDER BY id DESC")
        # 조회 결과를 가져옵니다
        posts = cur.fetchall()
    # 데이터베이스 연결을 종료합니다
    conn.close()
    
    # 게시글 목록 템플릿을 렌더링하여 반환합니다
    return templates.TemplateResponse("list.html", {"request": request, "posts": posts})
'''

#!!!!!!!!!!!!!!!!!!!!!!!!!
#내가 추가한 게시글 검색 웹 페이지
@app.get("/{page_num}")
def search_list(request: Request, page_num: int, query : str = ""):
    DB_query = ""
    IsBlank = True
    number_of_board_per_page = 3
    
    if query != "" :
        DB_query = " WHERE title LIKE" +" '%"+query+"%'"
        IsBlank = False
    else :
        DB_query = ""
        IsBlank = True


    # 데이터베이스에 연결합니다
    conn = get_db()
    # 커서를 생성하여 SQL 쿼리를 실행합니다
    with conn.cursor() as cur:
        # 모든 게시글을 최신순으로 조회합니다
        cur.execute("SELECT * FROM posts"+ DB_query +
                    " ORDER BY id DESC")
        #cur.execute("SELECT * FROM posts WHERE title LIKE " +"'%"+query+"%'"+" ORDER BY id DESC")
        # 조회 결과를 가져옵니다
        posts = cur.fetchall()

        page_count = range(len(posts) // number_of_board_per_page)

        cur.execute("SELECT * FROM posts"+ DB_query +
                    " ORDER BY id DESC LIMIT" +" "+str(number_of_board_per_page)+" "
                    +"OFFSET"+" "+str(number_of_board_per_page * (page_num - 1)))
        posts = cur.fetchall()
        
    # 데이터베이스 연결을 종료합니다
    conn.close()

    
    # 게시글 목록 템플릿을 렌더링하여 반환합니다
    return templates.TemplateResponse("list.html", {"request": request, "posts": posts,
                                                    "IsBlank": IsBlank, "page_count" : page_count,
                                                    "page_num" : page_num})



# 글쓰기 폼 페이지 라우트
@app.get("/write")
def write_form(request: Request):
    # 글쓰기 폼 템플릿을 렌더링하여 반환합니다
    return templates.TemplateResponse("write.html", {"request": request})


# 글쓰기 처리 라우트 (POST 요청)
@app.post("/write")
def write_post(title: str = Form(...), author: str = Form(...), content: str = Form(...)):
    # 데이터베이스에 연결합니다
    conn = get_db()
    # 커서를 생성하여 SQL 쿼리를 실행합니다
    with conn.cursor() as cur:
        # 새로운 게시글을 데이터베이스에 삽입합니다
        cur.execute("INSERT INTO posts (title, author, content) VALUES (%s, %s, %s)", (title, author, content))
        # 변경사항을 데이터베이스에 저장합니다
        conn.commit()
    # 데이터베이스 연결을 종료합니다
    conn.close()
    # 메인 페이지로 리다이렉트합니다
    return RedirectResponse("/", status_code=302)

# 게시글 상세보기 라우트
@app.get("/view/{post_id}")
def view_post(request: Request, post_id: int):
    # 데이터베이스에 연결합니다
    conn = get_db()
    # 커서를 생성하여 SQL 쿼리를 실행합니다
    with conn.cursor() as cur:
        # 특정 ID의 게시글을 조회합니다
        cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        # 조회 결과를 가져옵니다
        post = cur.fetchone()
    # 데이터베이스 연결을 종료합니다
    conn.close()
    # 게시글 상세보기 템플릿을 렌더링하여 반환합니다
    return templates.TemplateResponse("view.html", {"request": request, "post": post})

# 게시글 수정 폼 라우트
@app.get("/edit/{post_id}")
def edit_form(request: Request, post_id: int):
    # 데이터베이스에 연결합니다
    conn = get_db()
    # 커서를 생성하여 SQL 쿼리를 실행합니다
    with conn.cursor() as cur:
        # 수정할 게시글을 조회합니다
        cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        # 조회 결과를 가져옵니다
        post = cur.fetchone()
    # 데이터베이스 연결을 종료합니다
    conn.close()
    # 게시글 수정 폼 템플릿을 렌더링하여 반환합니다
    return templates.TemplateResponse("edit.html", {"request": request, "post": post})

# 게시글 수정 처리 라우트 (POST 요청)
@app.post("/edit/{post_id}")
def edit_post(post_id: int, title: str = Form(...), author: str = Form(...), content: str = Form(...)):
    # 데이터베이스에 연결합니다
    conn = get_db()
    # 커서를 생성하여 SQL 쿼리를 실행합니다
    with conn.cursor() as cur:
        # 게시글 정보를 업데이트합니다
        cur.execute("UPDATE posts SET title=%s, author=%s, content=%s WHERE id=%s", (title, author, content, post_id))
        # 변경사항을 데이터베이스에 저장합니다
        conn.commit()
    # 데이터베이스 연결을 종료합니다
    conn.close()
    # 수정된 게시글 상세보기 페이지로 리다이렉트합니다
    return RedirectResponse(f"/view/{post_id}", status_code=302)

# 게시글 삭제 라우트
@app.get("/delete/{post_id}")
def delete_post(post_id: int):
    # 데이터베이스에 연결합니다
    conn = get_db()
    # 커서를 생성하여 SQL 쿼리를 실행합니다
    with conn.cursor() as cur:
        # 특정 ID의 게시글을 삭제합니다
        cur.execute("DELETE FROM posts WHERE id=%s", (post_id,))
        # 변경사항을 데이터베이스에 저장합니다
        conn.commit()
    # 데이터베이스 연결을 종료합니다
    conn.close()
    # 메인 페이지로 리다이렉트합니다
    return RedirectResponse("/", status_code=302) 