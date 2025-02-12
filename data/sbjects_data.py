from data.database import get_connection
import uuid

def get_all_subjects_db():
    """Busca todos as matérias no banco de dados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM school.subjects
    ORDER BY id
    ''')
    subjects = [{"id": row[0], "name": row[1], "workload": row[2], "course_id": row[3]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return subjects

def create_subject_db(name, workload, course_id):
    """Insere um nova matéria no banco."""
    id = str(uuid.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO school.subjects (id, name, workload, course_id) 
    VALUES (%s, %s, %s, %s)
    RETURNING *
    ''', (id, name, workload, course_id))

    updated_subject = [
        {"id": row[0], "name": row[1], "workload": row[2], "course_id": row[3]} for
        row in cursor.fetchall()]

    conn.commit()
    cursor.close()
    conn.close()
    return updated_subject