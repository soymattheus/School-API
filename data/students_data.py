from data.database import get_connection
import uuid

def get_all_students_db():
    """Busca todos os estudantes no banco de dados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM school.students
    ORDER BY registration_number
    ''')
    users = [{"id": row[0], "name": row[1], "birthDate": row[2], "cpf": row[3], "phone": row[4], "address": row[5], "email": row[6], "registration_number": f"{row[7]:010d}", "status_active": row[8], "status_delete": row[9]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return users

def create_student_db(name, birth_date, cpf, phone, address, email):
    """Insere um novo estudantes no banco."""
    id = str(uuid.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO school.students (id, name, birth_date, cpf, phone, address, email) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (id, name, birth_date, cpf, phone, address, email))
    # user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": id, "name": name}

def update_student_db(id, name, birth_date, phone, address, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE school.students
    SET name = %s, birth_date  = %s, phone = %s, address = %s, email = %s 
    WHERE id = %s
    RETURNING *
    ''', (name, birth_date, phone, address, email, id))

    updated_student = [{"id": row[0], "name": row[1], "birthDate": row[2], "cpf": row[3], "phone": row[4], "address": row[5],
              "email": row[6], "registration_number": f"{row[7]:010d}", "status_active": row[8], "status_delete": row[9]} for row in cursor.fetchall()]
    conn.commit()
    cursor.close()
    conn.close()

    return updated_student

def access_status_student_db(id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE school.students
    SET status_active = upper(%s)
    WHERE id = %s
    RETURNING *
    ''', (status, id))

    updated_student = [{"id": row[0], "name": row[1], "birthDate": row[2], "cpf": row[3], "phone": row[4], "address": row[5],
              "email": row[6], "registration_number": f"{row[7]:010d}", "status_active": row[8], "status_delete": row[9]} for row in cursor.fetchall()]
    conn.commit()
    cursor.close()
    conn.close()

    return updated_student

def logic_delete_status_student_db(id, status='D'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE school.students
    SET status_delete = %s
    WHERE id = %s
    RETURNING *
    ''', (status, id))

    deleted_student = [{"id": row[0], "name": row[1], "birthDate": row[2], "cpf": row[3], "phone": row[4], "address": row[5],
              "email": row[6], "registration_number": f"{row[7]:010d}", "status_active": row[8], "status_delete": row[9]} for row in cursor.fetchall()]
    conn.commit()
    cursor.close()
    conn.close()

    return deleted_student