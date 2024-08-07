FROM node:22-bullseye-slim

WORKDIR /frontend

COPY . .

RUN npm install -g serve

EXPOSE 3000

CMD ["serve"]