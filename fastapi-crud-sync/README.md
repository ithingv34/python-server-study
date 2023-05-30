# Fastapi CRUD with Async Database 

### Usage

1. 저장소 clone or fork
2. 도커 이미지 빌드 및 컨테이너 실행
```bash
$ cd fastapi-crud
$ docker-compose up -d --build
```
3. 테스트 코드 실행
```bash
$ cd src
$ docker-compose exec web pytest .
```

---
- psql shell 접속
```bash
$ docker-compose exec db psql --username=fastapi --dbname=fastapi

# 모든 데이터베이스 출력
$ \l

# fastapi user 이름으로 데이터베이스 연결
$ \c fastapi

# 테이블 확인
$ \dt
```