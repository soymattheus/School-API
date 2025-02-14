import os

print(os.getenv("DB_HOST_DOCKER"))
print(os.getenv("DB_HOST"))
print(os.getenv("DB_PORT"))
print(os.getenv("DB_NAME"))
print(os.getenv("DB_USER"))
print(os.getenv("DB_PASSWORD"))

class Config:
    # Detecta se está rodando dentro de um container Docker
    if os.path.exists("/.dockerenv"):
        DB_HOST = os.getenv("DB_HOST_DOCKER", "host.docker.internal")  # Docker
    else:
        DB_HOST = os.getenv("DB_HOST", "127.0.0.1")  # Localhost

    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "matheus")
