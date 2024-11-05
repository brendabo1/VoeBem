# Usa a imagem do Node.js para construir o projeto
FROM node:18 as build

# Define o diretório de trabalho na imagem
WORKDIR /app

# Copia os arquivos package.json e package-lock.json
COPY package.json ./
COPY package-lock.json ./

# Instala as dependências do projeto
RUN npm install

# Copia todos os arquivos do cliente para o diretório de trabalho
COPY . .

# Compila o projeto React para o diretório /app/build
RUN npm run build

# Usa uma imagem nginx para servir o conteúdo compilado
FROM nginx:stable-alpine

# Copia o build do React para o diretório de distribuição do Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Expõe a porta onde o Nginx estará servindo o React
EXPOSE 80

# Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]
