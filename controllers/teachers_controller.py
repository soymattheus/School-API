from data.teachers_data import get_all_teachers_db, create_teacher_db, update_teacher_db, access_status_teacher_db, logic_delete_status_student_db

def get_all_teachers_controller():
    teachers = get_all_teachers_db()
    return teachers

def create_teacher_controller(name, specialization, phone, email):
    teacher = create_teacher_db(name=name, specialization=specialization, phone=phone, email=email)
    return teacher

def update_teacher_controller(id, name, specialization, phone, email):
    teacher = update_teacher_db(id=id, name=name, specialization=specialization, phone=phone, email=email)
    return teacher

def access_status_active_controller(id, status):
    teacher = access_status_teacher_db(id=id, status=status)
    return teacher

def update_status_delete_controller(id):
    teacher = logic_delete_status_student_db(id=id)
    return teacher