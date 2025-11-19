# Imagem base enxuta já com Python 3.12
FROM python:3.12-slim

# Todas as operações posteriores acontecem em /app
WORKDIR /app

# Instala dependências primeiro para aproveitar cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

ENV FLASK_APP=wsgi.py

# Sobe a API servida pelo Flask embutido
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
