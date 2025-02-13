# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements.txt primeiro para otimizar cache
COPY requirements.txt .

# Instala todas as dependências antes de copiar o resto do código
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Define variáveis de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando para rodar o servidor Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
