-- MySQL 초보자용 스키마 + 예시 SQL
-- 테이블은 3개만 사용: 과목(courses), 학생(students), 수강신청(enrollments)
-- 외래키(FOREIGN KEY) 제약조건은 사용하지 않습니다.

-- (선택) DB 만들기/선택하기
-- CREATE DATABASE IF NOT EXISTS courses_app DEFAULT CHARACTER SET utf8mb4;
-- USE courses_app;

-- 다시 실행해도 되게 기존 테이블 삭제
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

-- 1) 과목 테이블
CREATE TABLE courses (
  id INT NOT NULL,
  code VARCHAR(20) NOT NULL,
  name VARCHAR(100) NOT NULL,
  professor VARCHAR(50) NOT NULL,
  credits INT NOT NULL,
  time_text VARCHAR(50) NOT NULL,
  capacity INT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (code)
);

-- 2) 학생 테이블
CREATE TABLE students (
  id INT NOT NULL,
  student_no VARCHAR(20) NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (student_no)
);

-- 3) 수강신청 테이블
-- student_id / course_id 는 "번호로 연결"만 하고, 외래키 제약은 걸지 않습니다.
CREATE TABLE enrollments (
  id INT NOT NULL AUTO_INCREMENT,
  student_id INT NOT NULL,
  course_id INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE (student_id, course_id)
);

-- =========================
-- 초기 데이터 넣기 (INSERT)
-- =========================

-- 과목 데이터 (courses.html의 과목 목록)
INSERT INTO courses (id, code, name, professor, credits, time_text, capacity) VALUES
  (1, 'CS201', '자료구조', '김철수', 3, '월/수 10:30-12:00', 40),
  (2, 'CS301', '알고리즘', '이영희', 3, '화/목 13:00-14:30', 35),
  (3, 'CS302', '데이터베이스', '박민수', 3, '월/수 14:00-15:30', 45),
  (4, 'CS303', '운영체제', '정수진', 3, '화/목 09:00-10:30', 40),
  (5, 'CS304', '컴퓨터네트워크', '최준호', 3, '월/수 16:00-17:30', 35),
  (6, 'CS305', '소프트웨어공학', '강지훈', 3, '화/목 15:00-16:30', 30);

-- 학생 데이터
INSERT INTO students (id, student_no, name) VALUES
  (1, '20260001', '홍길동');

-- 수강신청(선택) 데이터: 홍길동이 1번 과목 신청
INSERT INTO enrollments (student_id, course_id) VALUES (1, 1);

-- =========================
-- 조회(SELECT) 예시
-- =========================

-- (1) 개설 과목 목록
SELECT * FROM courses ORDER BY id;

-- (2) 과목별 신청 인원(= enrolled) 구하기
SELECT
  c.id,
  c.code,
  c.name,
  c.capacity,
  COUNT(e.id) AS enrolled
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
GROUP BY c.id, c.code, c.name, c.capacity
ORDER BY c.id;

-- (3) 특정 학생의 "내 수강 목록"
SELECT
  c.*
FROM enrollments e
JOIN courses c ON c.id = e.course_id
WHERE e.student_id = 1
ORDER BY e.created_at DESC;

-- =========================
-- 추가(INSERT) 예시
-- =========================

-- (1) 과목 추가
-- INSERT INTO courses (id, code, name, professor, credits, time_text, capacity)
-- VALUES (7, 'CS401', '인공지능 개론', '최교수', 3, '금 10:00-12:00', 25);

-- (2) 수강신청 추가 (학생 1이 과목 2 신청)
INSERT INTO enrollments (student_id, course_id) VALUES (1, 2);

-- =========================
-- 수정(UPDATE) 예시
-- =========================

-- (1) 과목 정보 수정
UPDATE courses
SET professor = '김철수(수정)', time_text = '월/수 11:00-12:30', capacity = 45
WHERE id = 1;

-- (2) 학생 이름 수정
UPDATE students
SET name = '홍길동(수정)'
WHERE id = 1;

-- =========================
-- 삭제(DELETE) 예시
-- =========================

-- (1) 수강신청 취소 (학생 1이 과목 2 취소)
DELETE FROM enrollments
WHERE student_id = 1 AND course_id = 2;

-- (2) 과목 삭제 (주의: 외래키가 없으므로 enrollments에 "고아 데이터"가 남을 수 있어요)
-- DELETE FROM courses WHERE id = 6;

-- (선택) 고아 데이터 정리 예시: 존재하지 않는 과목을 가리키는 신청 삭제
-- DELETE e
-- FROM enrollments e
-- LEFT JOIN courses c ON c.id = e.course_id
-- WHERE c.id IS NULL;

