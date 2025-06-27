-- 게시판 데이터베이스를 생성합니다 (이미 존재하면 생성하지 않음)
CREATE DATABASE IF NOT EXISTS board_db;
-- board_db 데이터베이스를 사용하도록 설정합니다
USE board_db;

-- 게시글을 저장할 테이블을 생성합니다 (이미 존재하면 생성하지 않음)
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- 게시글 고유 번호 (자동 증가)
    title VARCHAR(255) NOT NULL,        -- 게시글 제목 (최대 255자, 필수 입력)
    content TEXT NOT NULL,              -- 게시글 내용 (긴 텍스트, 필수 입력)
    author VARCHAR(100) NOT NULL,       -- 작성자 (최대 100자, 필수 입력)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 작성 시간 (현재 시간 자동 설정)
); 

-- posts 테이블의 모든 데이터를 조회합니다 (테스트용)
select * FROM posts