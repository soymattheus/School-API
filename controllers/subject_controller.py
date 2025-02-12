from data.sbjects_data import get_all_subjects_db, create_subject_db

def get_all_subjects_controller():
    subjects = get_all_subjects_db()
    return subjects

def create_subject_controller(name, workload, course_id):
    subject = create_subject_db(name=name, workload=workload, course_id=course_id)
    return subject