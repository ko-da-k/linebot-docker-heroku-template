## Before deploy
``heroku container:login``

## How to build
``docker-compose -f docker-compose.heroku.yml build``

or

``docker -f Dockerfile.heroku build ``

## How to push
``docker tag <image> registry.heroku.com/<app>/<process-type>``

``docker push registry.heroku.com/<app>/<process-type>``

app is a name of application

process-type is usually used 'web' or 'worker'

## How to set environment variables
``heroku config:set ACCESS_TOKEN=hogehoge``