FROM node:18
WORKDIR /code/frontend
COPY ./package.json /code/frontend/package.json
COPY ./package-lock.json /code/frontend/package-lock.json
RUN npm ci --dev
RUN npm install
COPY . /code/frontend
