from data.courses_data import get_all_students_db, create_course_db

def get_all_courses_controller():
    courses = get_all_students_db()
    return courses

def create_course_controller(name, description, workload):
    course = create_course_db(name=name, description=description, workload=workload)
    return course