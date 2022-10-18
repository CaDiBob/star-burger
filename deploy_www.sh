#!/bin/bash -eu
git pull
docker-compose -f docker-compose.prod.yml exec web ./manage.py collectstatic --noinput
docker-compose -f docker-compose.prod.yml exec web ./manage.py migrate --noinput
sudo systemctl daemon-reload

curl -H "X-Rollbar-Access-Token: c136f76c85a3445daa9ea7690a0e4ead" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "prod", "revision": "'$(git rev-parse --short HEAD)'", "local_username": "cad", "comment": "auto deployment", "status": "succeeded"}'


echo $'\ndeploy completed'
