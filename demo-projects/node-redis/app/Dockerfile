FROM node:5-slim

WORKDIR /opt

RUN npm install redis

EXPOSE 8080

ADD ./app.js /opt/

CMD ["node", "/opt/app.js"]
