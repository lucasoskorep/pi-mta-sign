FROM docker.io/library/node:21-alpine
LABEL authors="lucasoskorep"

WORKDIR /app

COPY mta-sign-ui/* .

RUN corepack enable

RUN yarn set version stable
RUN yarn --version
RUN yarn

