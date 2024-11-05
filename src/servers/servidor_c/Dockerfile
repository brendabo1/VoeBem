# Usando uma imagem base Python
FROM python:latest

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do servidor e o requirements.txt
COPY server.py .
COPY rotas.json .
COPY raft_algoritmo.py .
COPY usuarios.json .

# Instala as dependências
#RUN pip install -r requirements.txt
RUN pip install flask requests gunicorn flask_cors

# Expõe a porta do servidor (ajuste conforme a configuração do servidor)
EXPOSE 5003

# Comando para iniciar o servidor 
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5003", "server:app"]

