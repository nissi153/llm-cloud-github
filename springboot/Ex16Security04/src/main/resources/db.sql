USE mydb;

-- 회원가입 테이블 만들기

DROP TABLE member_security;

CREATE TABLE member_security (
                 id 			BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                 username 	VARCHAR(255) NOT NULL,  -- 아이디
                 password  	VARCHAR(255) NOT NULL,  -- 암호
                 nick_name   VARCHAR(255),
                 user_role   VARCHAR(255) DEFAULT 'ROLE_USER',
                 join_date   DATE DEFAULT (CURRENT_DATE)
);

-- 암호는 Bcrypt 암호화하여 저장한다.
-- bcrypt-generator.com  강도 10으로 '1234'로 만들기
-- $2a$10$PFjmCpG/nMO6.0VkIayN/e9gTYL6AMAfs3o.c3b0IR2RLWL/p5v9C

INSERT INTO member_security VALUES
    (0, 'hong', '$2a$10$PFjmCpG/nMO6.0VkIayN/e9gTYL6AMAfs3o.c3b0IR2RLWL/p5v9C',
     '홍길동', 'ROLE_USER', '2026-03-12' );

SELECT * FROM member_security;

-- SNS 회원가입은 간편하게 빨리 회원가입시키는 목적,
-- SNS는 필요한 회원정보에 제한이 있다. 몇개 안준다.
-- 내 사이트는 SNS 로그인만 지원하겠다? 가능하다.

-- 정식 회원가입은 절차가 까다롭고, 입력할 내용이 많음.
--  추가적인 정보가 필요하지 않는 장점이 있다.
-- 개인정보보호관리자가 있어야 하고, 유출에 대한 책임도 져야 한다.

-- 대안 : 제3의 인증 사이트를 이용한다.
-- 예) Supabase, Firebase, CloudFlare

-- 서비스 구축시 : Google / 카카오 회원가입/인증만 지원한다.

-- sns-db.sql

-- 1. DB 연결
USE mydb;

DROP TABLE sns_user;

CREATE TABLE sns_user(
         id      BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
         name    VARCHAR(255) NOT NULL, -- 닉네임(별명)
         email   VARCHAR(255) NOT NULL, -- 이메일(계정)
         picture VARCHAR(255) NOT NULL, -- 프로필이미지 경로
         user_role   VARCHAR(255) DEFAULT 'ROLE_USER',
         created_date  DATE DEFAULT (current_date)
);

INSERT INTO sns_user VALUES (0, 'hong', 'hong@gmail.com', '', 'ROLE_USER', default );
INSERT INTO sns_user VALUES (0, 'tom', 'tom@gmail.com', '', 'ROLE_USER', default );

SELECT * FROM sns_user;

-- commit;