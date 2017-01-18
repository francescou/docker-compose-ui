FROM node:7-alpine

WORKDIR /opt

RUN npm install redis express

EXPOSE 8080

ADD ./app.js /opt/

CMD ["node", "/opt/app.js"]
