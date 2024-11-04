# Usa a imagem do Node.js para construir o projeto
FROM node:18 as build

# Define o diretório de trabalho na imagem
WORKDIR /app

# Copia os arquivos package.json e package-lock.json
COPY package.json ./

# Instala as dependências do projeto
RUN npm install

# Copia todos os arquivos do cliente para o diretório de trabalho
COPY . .

# Compila o aplicativo para produção
RUN npm run build

# Usa uma imagem nginx para servir o conteúdo compilado
FROM nginx:stable-alpine

# Copia o build do React para o diretório de distribuição do Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Expõe a porta onde o Nginx estará servindo o React
EXPOSE 80

# Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]


# # Usa uma imagem base do Python
# FROM python:latest

# # Define o diretório de trabalho
# WORKDIR /app

# # Copia o código do cliente e o arquivo requirements.txt
# COPY . .

# # Variáveis de ambiente configuradas pelo Docker Compose
# ENV SERVERS=servidor_A:5001,servidor_B:5002,servidor_C:5003

# # Instala as dependências do requirements.txt
# RUN pip install -r requirements.txt

# # Comando para rodar o cliente
# CMD ["python", "client.py"]
