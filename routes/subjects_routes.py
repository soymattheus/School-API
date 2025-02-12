from flask import Blueprint, jsonify, request
from controllers.subject_controller import get_all_subjects_controller, create_subject_controller

from flasgger import swag_from

subject_bp = Blueprint("subject", __name__)

@subject_bp.route("/subjects", methods=["GET"])
@swag_from({
    "tags": ["Subject"],
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
            "description": "Lists all the subjects",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                        "name": {"type": "string", "example": "Computer Science"},
                        "workload": {"type": "number", "example": "3600"},
                        "course_id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"}
                    }
                }
            }
        }
    }
})
def get_students():
    """Route to list all the subjects."""
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

        subjects = get_all_subjects_controller()

        # Retorna os dados paginados
        return jsonify({
            "total": len(subjects),
            "page": page,
            "limit": limit,
            "subjects": subjects[start:end]
        })

    except ValueError:
        return jsonify({"error": "The parameters page and limit must be integer numbers"}), 400




@subject_bp.route("/subject", methods=["POST"])
@swag_from({
    "tags": ["Subject"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                        "name": {"type": "string", "example": "Computer Science"},
                        "workload": {"type": "number", "example": 3600},
                        "course_id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                    },
                "required": ["name", "workload", "course_id"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Subject created",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                    "name": {"type": "string", "example": "Computer Science"},
                    "workload": {"type": "number", "example": 3600},
                    "course_id": {"type": "string", "example": "123e4567-e89b-12d3-a456-426614174000"},
                }
            }
        },
        400: {
            "description": "Error in data sent"
        }
    }
})
def add_student():
    """Route to create a new subject."""
    data = request.get_json()
    name = data["name"]
    course_id = data["course_id"]
    workload = data["workload"]

    student = create_subject_controller(name=name, workload=workload, course_id=course_id)
    return jsonify(student), 201
