# aggregator
Система, принимающая ставки на различные события.

Для запуска необходимо:

1. переименовать файлы
.env.example -> .env
.env.dev.example -> .env.dev

2. запустить все сервисы:
docker-compose -f docker-compose-line_provider.yml up -d
docker-compose -f docker-compose-bet_maker.yml up -d
docker-compose -f docker-compose-worker.yml up -d

3. применить миграции, чтобы создать таблицы в хранилищах:
docker-compose -f docker-compose-bet_maker.yml --env-file .env exec --workdir /src/db/migrations bet_maker alembic upgrade head
docker-compose -f docker-compose-line_provider.yml --env-file .env exec --workdir /src/db/migrations line_provider alembic upgrade head

4. Записать в таблицу данные по умолчанию:
docker-compose -f docker-compose-line_provider.yml --env-file .env exec --workdir /src/utils line_provider python base_data.py