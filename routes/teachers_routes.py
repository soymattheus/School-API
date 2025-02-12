from flask import Blueprint, jsonify, request
from controllers.teachers_controller import get_all_teachers_controller, create_teacher_controller, update_teacher_controller, access_status_active_controller, update_status_delete_controller
from flasgger import swag_from

teachers_bp = Blueprint("teacher", __name__)

@teachers_bp.route("/teachers", methods=["GET"])
@swag_from({
    "tags": ["Teacher"],
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
            "description": "Lists all the teachers",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                        "name": {"type": "string", "example": "Carlos Souza"},
                        "specialization": {"type": "string", "example": "Programming"},
                        "phone": {"type": "string", "example": "(21) 98877-6655"},
                        "email": {"type": "string", "example": "carlos@email.com"},
                        "registration_number": {"type": "string", "example": "0000000001"},
                        "status_active": {"type": "string", "example": "A"},
                        "status_delete": {"type": "string", "example": "A"},
                        "date_status_delete": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"}
                    }
                }
            }
        }
    }
})
def get_teachers():
    """Route to list all the teachers."""
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

        teachers = get_all_teachers_controller()

        # Retorna os dados paginados
        return jsonify({
            "total": len(teachers),
            "page": page,
            "limit": limit,
            "students": teachers[start:end]
        })

    except ValueError:
        return jsonify({"error": "The parameters page and limit must be integer numbers"}), 400

@teachers_bp.route("/teacher", methods=["POST"])
@swag_from({
    "tags": ["Teacher"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                        "name": {"type": "string", "example": "Matheus Tavares"},
                        "specialization": {"type": "string", "example": "Programing"},
                        "phone": {"type": "string", "example": "(21) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"}
                    },
                "required": ["name", "specialization, email"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Teacher created",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Matheus Tavares"},
                    "specialization": {"type": "string", "example": "Programing"},
                    "phone": {"type": "string", "example": "(21) 98765-4321"},
                    "email": {"type": "string", "example": "matheus@email.com"},
                    "registration_number": {"type": "string", "example": "0000000001"},
                    "status_active": {"type": "string", "example": "A"},
                    "status_dalete": {"type": "string", "example": "A"},
                    "date_ststaus_dalete": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"}
                }
            }
        },
        400: {
            "description": "Error in data sent"
        }
    }
})
def add_teacher():
    """Route to create a new teacher."""
    data = request.get_json()
    name = data["name"]
    specialization = data["specialization"]
    phone = data["phone"]
    email = data["email"]

    teacher = create_teacher_controller(name=name, specialization=specialization, phone=phone, email=email)
    return jsonify(teacher), 201

@teachers_bp.route("/teacher/<string:id>", methods=["PUT"])
@swag_from({
    "tags": ["Teacher"],
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
                        "specialization": {"type": "string", "example": "Programming"},
                        "phone": {"type": "string", "example": "(21) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"}
                    },
                "required": ["name", "specialization", "email"]
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
                        "specialization": {"type": "string", "example": "Programming"},
                        "phone": {"type": "string", "example": "(11) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "registration_number": {"type": "string", "example": "0000000001"},
                        "status_active": {"type": "string", "example": "A"},
                        "status_delete": {"type": "string", "example": "I"},
                        "date_status_delete": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"},
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
    """Update a teacher by ID"""
    data = request.get_json()

    if not data or "name" not in data or "specialization" not in data or "phone" not in data or "email" not in data:
        return jsonify({"error": "Fields 'name', 'specialization', 'phone' and 'email' are required"}), 400

    name = data["name"]
    specialization = data["specialization"]
    phone = data["phone"]
    email = data["email"]

    if not isinstance(name, str) or not isinstance(name, str) or not isinstance(specialization, str) or not isinstance(phone, str) or not isinstance(email, str):
        return jsonify({"error": "Invalid type: 'name', 'birth_date', 'phone', address' and 'email' must be string"}), 400

    updated_teacher = update_teacher_controller(id=id, name=name, specialization=specialization, phone=phone, email=email)

    if updated_teacher:
        return jsonify({
            "message": "Students updated",
            "teacher": updated_teacher
        })
    else:
        return jsonify({"error": "Teacher not found"}), 404

@teachers_bp.route("/teacher/status/<string:id>/<string:status>", methods=["PUT"])
@swag_from({
    "tags": ["Teacher"],
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
            "description": "Shows the updated teacher",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                        "name": {"type": "string", "example": "Matheus"},
                        "specialization": {"type": "string", "example": "Programming"},
                        "phone": {"type": "string", "example": "(11) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "registration_number": {"type": "string", "example": "0000000001"},
                        "status_active": {"type": "string", "example": "A"},
                        "status_delete": {"type": "string", "example": "A"},
                        "date_status_delete": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"},
                    }
                }
            }
        },
        400: {
            "description": "Error in data sent"
        }
    }
})
def access_status_teacher(id, status):
    """Update teacher access status by ID"""
    updated_teacher = access_status_active_controller(id=id, status=status)

    if updated_teacher:
        return jsonify({
            "message": "Teacher status updated",
            "teacher": updated_teacher
        })
    else:
        return jsonify({"error": "Teacher not found"}), 404

@teachers_bp.route("/teacher/delete/<string:id>", methods=["DELETE"])
@swag_from({
    "tags": ["Teacher"],
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
                        "specialization": {"type": "string", "example": "Programming"},
                        "phone": {"type": "string", "example": "(11) 98765-4321"},
                        "email": {"type": "string", "example": "matheus@email.com"},
                        "registration_number": {"type": "string", "example": "0000000001"},
                        "status_active": {"type": "string", "example": "A"},
                        "status_delete": {"type": "string", "example": "A"},
                        "date_status_delete": {"type": "string", "example": "Tue, 15 Mar 2005 00:00:00 GMT"},
                    }
                }
            }
        },
        400: {
            "description": "Error in data sent"
        }
    }
})
def logic_delete_status_teacher(id):
    """Make the logic deletetion of a teacher"""
    updated_teacher = update_status_delete_controller(id=id)

    if updated_teacher:
        return jsonify({
            "message": "Teacher updated",
            "teacher": updated_teacher
        })
    else:
        return jsonify({"error": "Teacher not found"}), 404