from data.students_data import get_all_students_db, create_student_db, update_student_db, access_status_student_db, logic_delete_status_student_db
from flask import Blueprint, jsonify, request

def get_all_students():
    students = get_all_students_db()
    return students

def create_student(name, birth_date, cpf, phone, address, email):
    student = create_student_db(name, birth_date, cpf, phone, address, email)
    return student

def update_student_controller(id, name, birth_date, phone, address, email):
    student = update_student_db(id=id, name=name, birth_date=birth_date, phone=phone, address=address, email=email)
    return student

def access_status_student_controller(id, status):
    student = access_status_student_db(id=id, status=status)
    return student

def logic_delete_status_student_controller(id):
    student = logic_delete_status_student_db(id=id)
    return student