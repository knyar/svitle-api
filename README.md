# API for Svitle Radio

This repository contains API backend code for [Svitle
Radio](https://svitle.org), a Christian radio station in Kyiv, Ukraine.

## Deployment

Build a docker image:

```bash
docker build -t svitle_api .
```

Start redis (if not running) and the app container:

```bash
docker network create svitle_api_redis
docker run -d --restart always --network svitle_api_redis \
  --name svitle_redis redis
docker run -d --restart always --network svitle_api_redis \
  -p 8087:5000 -e 'REDIS_URL=redis://svitle_redis:6379' \
  --name svitle_api svitle_api
```

The app will be available on port 8087

## Development

Install dependencies:

```bash
pip install pipenv
pipenv install
```

Start redis:

```bash
docker run --name svitle_redis -p 16379:6379 -d redis
```

Start development server:

```bash
REDIS_URL=redis://localhost:16379 pipenv run python app.py
```
