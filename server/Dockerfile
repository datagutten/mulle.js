FROM node:18-bookworm-slim
EXPOSE 8765
WORKDIR /server

COPY server.js .
RUN npm install ws colors moment

ENTRYPOINT ["node", "server.js"]