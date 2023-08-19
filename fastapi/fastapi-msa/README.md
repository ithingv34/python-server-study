# Simple FastAPI MSA with docker-compose

**backend**
- user service, port: 8000:8000
- order service, port: 8001:8000
- product service, port: 8002:8000

**frontend**
- react client, port: 3000

**Usage**

```bash
$ docker-compose up up 
or
$ docker-compose up -d # If you want to run the services in background 
```