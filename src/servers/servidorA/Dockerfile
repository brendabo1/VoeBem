# Usando uma imagem base Python
FROM python:latest

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do servidor e o requirements.txt
COPY server.py .
COPY rotas.json .
COPY ../compartilhado /app/compartilhado
# COPY requirements.txt .
#COPY . .
# Instala dependências
# COPY requirements.txt requirements.txt
RUN pip install flask requests
# RUN pip install -r requirements.txt

# Expõe a porta do servidor (ajuste conforme a configuração do servidor)
EXPOSE 5001

# Comando para iniciar o servidor (ajuste conforme necessário)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "server:app"]
