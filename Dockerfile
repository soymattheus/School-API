# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements.txt primeiro (otimização de cache)
COPY requirements.txt .

# Instala todas as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Configuração das variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DATABASE_URL=postgresql://postgres:matheus@db:5432/mydatabase
ENV DEBUG=False

# Comando para rodar o servidor Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
