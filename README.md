# 심플 게시판 프로젝트

## 구성
- 백엔드: Python (FastAPI)
- 프론트엔드: HTML (Jinja2 템플릿)
- 데이터베이스: MySQL

## 실행 방법

1. MySQL에서 `database/schema.sql` 실행
2. Python 패키지 설치
   ```
   pip install fastapi pymysql uvicorn jinja2
   ```
3. 서버 실행
   ```
   uvicorn backend.main:app --reload
   ```
4. 웹브라우저에서 [http://localhost:8000/](http://localhost:8000/) 접속

5. **서버 종료 방법**
   - 터미널(명령 프롬프트, PowerShell 등)에서 실행 중인 서버를 종료하려면 `Ctrl + C`를 누르세요.
   - 서버가 정상적으로 종료되었다는 메시지가 출력됩니다.

## 주요 기능
- 게시글 목록 보기
- 게시글 작성
- 게시글 내용 보기
- 게시글 수정
- 게시글 삭제 