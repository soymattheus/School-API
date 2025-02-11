from data.database import get_connection
import uuid

def get_all_students_db():
    """Busca todos os estudantes no banco de dados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM school.courses
    ORDER BY id
    ''')
    courses = [{"id": row[0], "name": row[1], "description": row[2], "workload": row[3], "status_active": row[4]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return courses

def create_course_db(name, description, workload):
    """Insere um novo estudantes no banco."""
    id = str(uuid.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO school.Courses (id, name, description, workload) 
    VALUES (%s, %s, %s, %s)
    ''', (id, name, description, workload))
    # user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": id, "name": name, "description": description, "workload": workload, "status_active": "A"}