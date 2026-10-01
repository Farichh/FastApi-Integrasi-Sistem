from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 1. Menentukan isi data (Object) sesuai soal tugas[cite: 1]
class Student(BaseModel):
    nama: str
    alamat: str
    ipk: float
    semester: int
    hobi: str

class StudentUpdate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None

students_db = {}

@app.get("/students")
async def get_all_students():
    return {"data": students_db}

@app.get("/students/{student_id}")
async def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return {"student_id": student_id, "data": students_db[student_id]}

@app.post("/students/{student_id}")
async def create_student(student_id: int, student: Student):
    if student_id in students_db:
        raise HTTPException(status_code=400, detail="ID sudah ada")
    students_db[student_id] = student.dict()
    return {"message": "Berhasil menyimpan data", "data": students_db[student_id]}

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: StudentUpdate):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    
    update_data = student.dict(exclude_unset=True)
    students_db[student_id].update(update_data)
    return {"message": "Berhasil mengupdate data", "data": students_db[student_id]}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    del students_db[student_id]
    return {"message": "Berhasil menghapus data"}