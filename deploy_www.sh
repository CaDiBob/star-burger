#!/bin/bash -eu
git pull
/home/cad/star-burger/venv/bin/pip install -r requirements.txt
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
/home/cad/star-burger/venv/bin/python3 manage.py collectstatic --noinput
/home/cad/star-burger/venv/bin/python3 manage.py migrate
sudo sh -c ' systemctl daemon-reload && systemctl restart www.service && systemctl reload nginx'
echo $'\ndeploy completed'

