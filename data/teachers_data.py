from data.database import get_connection
import uuid

def get_all_teachers_db():
    """Busca todos os estudantes no banco de dados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM school.teachers
    ORDER BY registration_number ASC
    ''')
    teachers = [{"id": row[0], "name": row[1], "specialization": row[2], "phone": row[3], "email": row[4], "registration_number": f"{row[5]:010d}", "status_active": row[6], "status_delete": row[7], "date_status_delete": row[8]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return teachers

def create_teacher_db(name, specialization, phone, email):
    """Insere um novo estudantes no banco."""
    id = str(uuid.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO school.teachers (id, name, specialization, phone, email) 
    VALUES (%s, %s, %s, %s, %s)
    RETURNING *
    ''', (id, name, specialization, phone, email))

    updated_teacher = [
        {"id": row[0], "name": row[1], "specialization": row[2], "phone": row[3], "email": row[4], "registration-number": row[5],
         "status_active": row[6], "status_delete": row[7], "date_status_delete": row[8]} for
        row in cursor.fetchall()]

    conn.commit()
    cursor.close()
    conn.close()
    return updated_teacher

def update_teacher_db(id, name, specialization, phone, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE school.teachers
    SET name = %s, specialization  = %s, phone = %s, email = %s
    WHERE id = %s
    RETURNING *
    ''', (name, specialization, phone, email, id))

    updated_teacher = [
        {"id": row[0], "name": row[1], "specialization": row[2], "phone": row[3], "email": row[4],
         "registration-number": row[5],
         "status_active": row[6], "status_delete": row[7], "date_status_delete": row[8]} for
        row in cursor.fetchall()]

    conn.commit()
    cursor.close()
    conn.close()

    return updated_teacher

def access_status_teacher_db(id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE school.teachers
    SET status_active = upper(%s)
    WHERE id = %s
    RETURNING *
    ''', (status, id))

    updated_teacher = [
        {"id": row[0], "name": row[1], "specialization": row[2], "phone": row[3], "email": row[4],
         "registration-number": row[5],
         "status_active": row[6], "status_delete": row[7], "date_status_delete": row[8]} for
        row in cursor.fetchall()]

    conn.commit()
    cursor.close()
    conn.close()

    return updated_teacher

def logic_delete_status_student_db(id, status='D'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE school.teachers
    SET status_delete = %s, date_status_delete = NOW()
    WHERE id = %s
    RETURNING *
    ''', (status, id))

    updated_teacher = [
        {"id": row[0], "name": row[1], "specialization": row[2], "phone": row[3], "email": row[4],
         "registration-number": row[5],
         "status_active": row[6], "status_delete": row[7], "date_status_delete": row[8]} for
        row in cursor.fetchall()]

    conn.commit()
    cursor.close()
    conn.close()

    return updated_teacher