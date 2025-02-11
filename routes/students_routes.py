from flask import Blueprint, jsonify, request
from controllers.student_controller import get_all_students, create_student, update_student_controller, access_status_student_controller, logic_delete_status_student_controller
from flasgger import swag_from

student_bp = Blueprint("student", __name__)

@student_bp.route("/students", methods=["GET"])
@swag_from({
    "tags": ["Student"],
    "parameters": [
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 1,
            "description": "Number of the page (starts at 1)"
        },
        {
            "name": "limit",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 10,
            "description": "Number of items per page"
        }
    ],
    "responses": {
        200: {
            "description": "Lists all the students",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                        "name": {"type": "string", "example": "Matheus"},
                        "birthDate": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"},
                        "cpf": {"type": "string", "example": "00011122233"},
                        "phone": {"type": "string", "example": "(11) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "address": {"type": "string", "example": "Rua A, 327"},
                        "registration_number": {"type": "number", "example": 1},
                        "status_active": {"type": "string", "example": "A"},
                        "status_delete": {"type": "string", "example": "I"}
                    }
                }
            }
        }
    }
})
def get_students():
    """Route to list all the students."""
    try:
        # Obtém valores da URL com padrão seguro
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        # Se os valores forem inválidos (negativos ou zero), define os padrões
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10

        # Valida valores mínimos
        if page < 1 or limit < 1:
            return jsonify({"error": "The values of page and limit must be positive"}), 400

        # Calcula índices de início e fim da página
        start = (page - 1) * limit
        end = start + limit

        students = get_all_students()

        # Retorna os dados paginados
        return jsonify({
            "total": len(students),
            "page": page,
            "limit": limit,
            "students": students[start:end]
        })

    except ValueError:
        return jsonify({"error": "The parameters page and limit must be integer numbers"}), 400

@student_bp.route("/student", methods=["POST"])
@swag_from({
    "tags": ["Student"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                        "name": {"type": "string", "example": "Matheus Tavares"},
                        "birth_date": {"type": "string", "example": "1996-03-26"},
                        "cpf": {"type": "string", "example": "00011122233"},
                        "phone": {"type": "string", "example": "(21) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "address": {"type": "string", "example": "Rua A, 327"}
                    },
                "required": ["name", "birth_date, cpf"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Students created",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "example": "789e1234-a567-b890-c123-456789defghi"},
                    "name": {"type": "string", "example": "Carlos"}
                }
            }
        },
        400: {
            "description": "Error in data sent"
        }
    }
})
def add_student():
    """Route to create a new student."""
    data = request.get_json()
    student = create_student(data["name"], data["birth_date"], data["cpf"], data["phone"], data["address"], data["email"])
    return jsonify(student), 201

# Rota para atualizar um estudante
@student_bp.route("/students/<string:id>", methods=["PUT"])
@swag_from({
    "tags": ["Student"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "type": "string",
            "required": False,
            "default": '102b8595-53ff-488e-9459-f80f1e789491',
            "description": "The id of the student"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                        "name": {"type": "string", "example": "Matheus Tavares"},
                        "birth_date": {"type": "string", "example": "1996-03-26"},
                        "phone": {"type": "string", "example": "(21) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "address": {"type": "string", "example": "Rua A, 327"}
                    },
                "required": ["name", "birth_date, phone", "address", "email"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Shows the updated student",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                        "name": {"type": "string", "example": "Matheus"},
                        "birthDate": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"},
                        "cpf": {"type": "string", "example": "00011122233"},
                        "phone": {"type": "string", "example": "(11) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "address": {"type": "string", "example": "Rua A, 327"},
                        "registration_number": {"type": "number", "example": 1},
                        "status_active": {"type": "string", "example": "A"},
                        "status_delete": {"type": "string", "example": "I"}
                    }
                }
            }
        },
        201: {
            "description": "Students created",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "example": "789e1234-a567-b890-c123-456789defghi"},
                    "name": {"type": "string", "example": "Carlos"}
                }
            }
        },
        400: {
            "description": "Error in data sent"
        }
    }
})
def update_student(id):
    """Update student by ID"""
    data = request.get_json()

    if not data or "name" not in data or "birth_date" not in data or "phone" not in data or "address" not in data or "email" not in data:
        return jsonify({"error": "Fields 'name', 'birth_date', 'phone', 'address' and 'email' are required"}), 400

    name = data["name"]
    birth_date = data["birth_date"]
    phone = data["phone"]
    address = data["address"]
    email = data["email"]

    if not isinstance(name, str) or not isinstance(name, str) or not isinstance(birth_date, str) or not isinstance(phone, str) or not isinstance(address, str) or not isinstance(email, str):
        return jsonify({"error": "Invalid type: 'name', 'birth_date', 'phone', address' and 'email' must be string"}), 400

    updated_student = update_student_controller(id=id, name=name, birth_date=birth_date, phone=phone, address=address, email=email)

    if updated_student:
        return jsonify({
            "message": "Students updated",
            "student": updated_student
        })
    else:
        return jsonify({"error": "Student not found"}), 404

# Rota para atualizar permissão de acesso de um estudante
@student_bp.route("/students/status/<string:id>/<string:status>", methods=["PUT"])
@swag_from({
    "tags": ["Student"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "type": "string",
            "required": False,
            "default": 'ed13eced-6ed2-42f5-9b47-f0476fdf4ed0',
            "description": "The id of the student"
        },
        {
            "name": "status",
            "in": "path",
            "type": "string",
            "required": False,
            "default": 'A',
            "description": "The status of student access"
        },
    ],
    "responses": {
        200: {
            "description": "Shows the updated student",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                        "name": {"type": "string", "example": "Matheus"},
                        "birthDate": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"},
                        "cpf": {"type": "string", "example": "00011122233"},
                        "phone": {"type": "string", "example": "(11) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "address": {"type": "string", "example": "Rua A, 327"},
                        "registration_number": {"type": "number", "example": 1},
                        "status_active": {"type": "string", "example": "A"},
                        "status_delete": {"type": "string", "example": "I"}
                    }
                }
            }
        },
        400: {
            "description": "Error in data sent"
        }
    }
})
def access_status_student(id, status):
    """Update student access status by ID"""
    updated_student = access_status_student_controller(id=id, status=status)

    if updated_student:
        return jsonify({
            "message": "Students updated",
            "student": updated_student
        })
    else:
        return jsonify({"error": "Student not found"}), 404

# Rota para atualizar exclusão lógica de um estudante
@student_bp.route("/students/delete/<string:id>", methods=["DELETE"])
@swag_from({
    "tags": ["Student"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "type": "string",
            "required": False,
            "default": 'ed13eced-6ed2-42f5-9b47-f0476fdf4ed0',
            "description": "The id of the student"
        }
    ],
    "responses": {
        200: {
            "description": "Shows the updated student",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                        "name": {"type": "string", "example": "Matheus"},
                        "birthDate": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"},
                        "cpf": {"type": "string", "example": "00011122233"},
                        "phone": {"type": "string", "example": "(11) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "address": {"type": "string", "example": "Rua A, 327"},
                        "registration_number": {"type": "number", "example": 1},
                        "status_active": {"type": "string", "example": "A"},
                        "status_delete": {"type": "string", "example": "I"}
                    }
                }
            }
        },
        400: {
            "description": "Error in data sent"
        }
    }
})
def logic_delete_status_student(id):
    """Make the logic deletetion of a student"""
    updated_student = logic_delete_status_student_controller(id=id)

    if updated_student:
        return jsonify({
            "message": "Students updated",
            "student": updated_student
        })
    else:
        return jsonify({"error": "Student not found"}), 404