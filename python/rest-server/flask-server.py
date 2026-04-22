# Flask 서버
# Django에 비해 간결한 서버를 만들 수 있다.
# 추가기능은 import를 통해 구현한다.

from flask import Flask, request, jsonify

app = Flask(__name__)

# 인메모리 DB (딕셔너리)
# 구조: { id: { "name": str, "grade": int, "age": int } }
students = {
    1: {"id": 1, "name": "홍길동", "grade": 1, "age": 15},
    2: {"id": 2, "name": "김철수", "grade": 2, "age": 16},
    3: {"id": 3, "name": "이영희", "grade": 3, "age": 17},
}
next_id = 4


# 전체 학생 조회
@app.route("/students", methods=["GET"])
def get_students():
    # jsonify : 딕셔너리 객체를 JSON문자열로 만들어주는 함수
    return jsonify(list(students.values())), 200


# 특정 학생 조회
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = students.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


# 학생 등록
@app.route("/students", methods=["POST"])
def create_student():
    global next_id
    data = request.get_json()

    if not data or not all(k in data for k in ("name", "grade", "age")):
        return jsonify({"error": "name, grade, age 필드가 필요합니다"}), 400

    student = {
        "id": next_id,
        "name": data["name"],
        "grade": data["grade"],
        "age": data["age"],
    }
    students[next_id] = student
    next_id += 1

    return jsonify(student), 201


# 학생 정보 수정 (전체)
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    if not data or not all(k in data for k in ("name", "grade", "age")):
        return jsonify({"error": "name, grade, age 필드가 필요합니다"}), 400

    students[student_id].update(
        {
            "name": data["name"],
            "grade": data["grade"],
            "age": data["age"],
        }
    )
    return jsonify(students[student_id]), 200


# 학생 정보 수정 (부분)
@app.route("/students/<int:student_id>", methods=["PATCH"])
def patch_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "수정할 데이터가 없습니다"}), 400

    for key in ("name", "grade", "age"):
        if key in data:
            students[student_id][key] = data[key]

    return jsonify(students[student_id]), 200


# 학생 삭제
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404

    deleted = students.pop(student_id)
    return jsonify(deleted), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
