# FastAPI 서버
# Flask보다 자동 문서화(Swagger UI)와 타입 검증 기능이 강력하다.
# RestAPI 테스트(개발자용)
# Swagger UI: http://localhost:8000/docs
# API명세확인(사용자, 외부개발자)
# ReDoc UI:   http://localhost:8000/redoc

# pip install fastapi
# pip install uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Student REST API",
    description="인메모리 딕셔너리 기반 학생 관리 REST API",
    version="1.0.0",
)

# 인메모리 DB (딕셔너리)
# 구조: { id: { "id": int, "name": str, "grade": int, "age": int } }
students = {
    1: {"id": 1, "name": "홍길동", "grade": 1, "age": 15},
    2: {"id": 2, "name": "김철수", "grade": 2, "age": 16},
    3: {"id": 3, "name": "이영희", "grade": 3, "age": 17},
}
next_id = 4


# Pydantic 모델 (요청 바디 유효성 검사 + Swagger 문서 자동 생성)
class StudentCreate(BaseModel):
    name: str
    grade: int
    age: int

    model_config = {
        "json_schema_extra": {"example": {"name": "박민준", "grade": 1, "age": 15}}
    }


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    grade: Optional[int] = None
    age: Optional[int] = None

    model_config = {
        "json_schema_extra": {"example": {"name": "박민준", "grade": 2, "age": 16}}
    }


# 전체 학생 조회
@app.get("/students", summary="전체 학생 조회", tags=["Students"])
def get_students():
    return list(students.values())


# 특정 학생 조회
@app.get("/students/{student_id}", summary="특정 학생 조회", tags=["Students"])
def get_student(student_id: int):
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# 학생 등록
@app.post("/students", summary="학생 등록", tags=["Students"], status_code=201)
def create_student(body: StudentCreate):
    global next_id
    student = {
        "id": next_id,
        "name": body.name,
        "grade": body.grade,
        "age": body.age,
    }
    students[next_id] = student
    next_id += 1
    return student


# 학생 정보 전체 수정 (PUT)
@app.put("/students/{student_id}", summary="학생 정보 전체 수정", tags=["Students"])
def update_student(student_id: int, body: StudentCreate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id].update(
        {
            "name": body.name,
            "grade": body.grade,
            "age": body.age,
        }
    )
    return students[student_id]


# 학생 정보 부분 수정 (PATCH)
@app.patch("/students/{student_id}", summary="학생 정보 부분 수정", tags=["Students"])
def patch_student(student_id: int, body: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="수정할 데이터가 없습니다")
    students[student_id].update(update_data)
    return students[student_id]


# 학생 삭제
@app.delete("/students/{student_id}", summary="학생 삭제", tags=["Students"])
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students.pop(student_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi-server:app", host="0.0.0.0", port=8000, reload=True)
