# REST API Server (Flask)

인메모리 딕셔너리를 DB로 사용하는 간단한 Flask REST API 서버입니다.

## 학생(Student) 데이터 구조

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | int | 자동 생성 고유 번호 |
| `name` | string | 학생 이름 |
| `grade` | int | 학년 |
| `age` | int | 나이 |

## 실행 방법

```bash
pip install flask
python flask-server.py
```

서버는 기본적으로 `http://localhost:5000` 에서 실행됩니다.

## API 엔드포인트

| Method | URL | 설명 |
|--------|-----|------|
| `GET` | `/students` | 전체 학생 조회 |
| `GET` | `/students/<id>` | 특정 학생 조회 |
| `POST` | `/students` | 학생 등록 |
| `PUT` | `/students/<id>` | 학생 정보 전체 수정 |
| `PATCH` | `/students/<id>` | 학생 정보 부분 수정 |
| `DELETE` | `/students/<id>` | 학생 삭제 |

## 테스트 (curl)

### 학생 등록

```bash
curl -X POST http://localhost:5000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "홍길동", "grade": 2, "age": 16}'
```

### 전체 학생 조회

```bash
curl http://localhost:5000/students
```

### 특정 학생 조회

```bash
curl http://localhost:5000/students/1
```

### 학생 정보 전체 수정 (PUT)

```bash
curl -X PUT http://localhost:5000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "홍길동", "grade": 3, "age": 17}'
```

### 학생 정보 부분 수정 (PATCH)

```bash
curl -X PATCH http://localhost:5000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"age": 17}'
```

### 학생 삭제

```bash
curl -X DELETE http://localhost:5000/students/1
```

## 응답 예시

### POST /students (201 Created)

```json
{
  "id": 1,
  "name": "홍길동",
  "grade": 2,
  "age": 16
}
```

### GET /students (200 OK)

```json
[
  { "id": 1, "name": "홍길동", "grade": 2, "age": 16 },
  { "id": 2, "name": "김철수", "grade": 3, "age": 17 }
]
```

### 404 Not Found

```json
{
  "error": "Student not found"
}
```
