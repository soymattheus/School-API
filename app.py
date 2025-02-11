from flask import Flask
from routes.students_routes import student_bp
from routes.courses_routes import courses_bp
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "School API",
        "description": "API to manage school.",
        "version": "1.0.0"
    },
    "host": "127.0.0.1:5000",  # Alterar se for rodar em outro host
    "basePath": "/",
})


# Registrando Blueprint
app.register_blueprint(student_bp, url_prefix="/api/v1")
app.register_blueprint(courses_bp, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(debug=True)
