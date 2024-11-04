# Usa uma imagem base do Python
FROM python:latest

# Define o diretório de trabalho
WORKDIR /app

# Copia o código do cliente e o arquivo requirements.txt
COPY . .

# Variáveis de ambiente configuradas pelo Docker Compose
ENV SERVERS=servidor_A:5001,servidor_B:5002,servidor_C:5003

# Instala as dependências do requirements.txt
RUN pip install -r requirements.txt

# Comando para rodar o cliente
CMD ["python", "client.py"]
