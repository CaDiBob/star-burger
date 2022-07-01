#!/bin/bash -eu
git pull
/home/cad/star-burger/venv/bin/pip install -r requirements.txt
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
/home/cad/star-burger/venv/bin/python3 manage.py collectstatic --noinput
/home/cad/star-burger/venv/bin/python3 manage.py migrate --noinput

sudo systemctl daemon-reload
sudo systemctl restart www.service
sudo systemctl reload nginx

curl -H "X-Rollbar-Access-Token: c136f76c85a3445daa9ea7690a0e4ead" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "prod", "revision": "'$(git rev-parse --short HEAD)'", "local_username": "cad", "comment": "auto deployment", "status": "succeeded"}'


echo $'\ndeploy completed'

