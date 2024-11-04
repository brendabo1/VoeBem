# Usando uma imagem base Python
FROM python:latest

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do servidor e o requirements.txt
COPY server.py .
COPY rotas.json .
#COPY requirements.txt .
COPY ../compartilhado /app/compartilhado

# Instala as dependências
#RUN pip install --no-cache-dir -r requirements.txt

RUN pip install flask requests
# Expõe a porta do servidor (ajuste conforme a configuração do servidor)
EXPOSE 5002

# Comando para iniciar o servidor 
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5002", "server:app"]
