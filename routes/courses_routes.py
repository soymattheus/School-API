from flask import Blueprint, jsonify, request
from controllers.courses_controller import get_all_courses_controller, create_course_controller

from flasgger import swag_from

courses_bp = Blueprint("course", __name__)

@courses_bp.route("/courses", methods=["GET"])
@swag_from({
    "tags": ["Course"],
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
                        "name": {"type": "string", "example": "Computer Science"},
                        "description": {"type": "string", "example": "Software development and programming"},
                        "workload": {"type": "number", "example": "3600"},
                        "status_active": {"type": "string", "example": "A"}
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

        courses = get_all_courses_controller()

        # Retorna os dados paginados
        return jsonify({
            "total": len(courses),
            "page": page,
            "limit": limit,
            "students": courses[start:end]
        })

    except ValueError:
        return jsonify({"error": "The parameters page and limit must be integer numbers"}), 400

@courses_bp.route("/course", methods=["POST"])
@swag_from({
    "tags": ["Course"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                        "name": {"type": "string", "example": "Computer Science"},
                        "description": {"type": "string", "example": "Software development and programming"},
                        "workload": {"type": "number", "example": 3600}
                    },
                "required": ["name", "description, workload"]
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
    """Route to create a new course."""
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    workload = data["workload"]

    student = create_course_controller(name=name, description=description, workload=workload)
    return jsonify(student), 201
