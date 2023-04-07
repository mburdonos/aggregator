# aggregator
Система, принимающая ставки на различные события. 

Для запуска необходимо:

1. переименовать файлы
.env.example -> .env
.env.dev.example -> .env.dev
2. запустить docker-compose.yml:
docker-compose up -d
3. применить миграции:
docker-compose --env-file .env exec --workdir /src/db/migrations bet_maker alembic upgrade head