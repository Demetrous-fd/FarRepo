### Требования для запуска:
- Python 3.11
- Docker, Docker compose
 
### Запуск вручную:

1. Склонируйте репозиторий
    ```shell
    git clone https://github.com/Demetrous-fd/FarRepo.git
    ```

2. Перейти в папку проекта
    ```shell
    cd FarRepo
    ```

3. Создать и заполнить .env
    ```shell
    cp .env.example .env 
    ```

4. Создайте виртуальное окружение и активируйте его
   ```shell
   python -m venv venv
   ```

5. Установить зависимости
   ```shell
   pip install -r requirements.txt
   ```

6. Выполните миграцию
   ```shell
   alembic upgrade head
   ```

7. Запустить сервисы
    ```shell
    uvicorn app:app
    celery -A app:celery worker --loglevel=INFO
    celery -A app:celery beat --loglevel=INFO -S redbeat.RedBeatScheduler
    ```

8. Перейдите по адресу *http://<host_ip>:8000/docs*

### Запуск через docker:

1. Склонируйте репозиторий
    ```shell
    git clone https://github.com/Demetrous-fd/FarRepo.git
    ```

2. Перейти в папку проекта
    ```shell
    cd FarRepo
    ```

3. Создать и заполнить .env
    ```shell
    cp .env.example .env 
    ```

4. Запустить сервисы
    ```shell
    docker-compose up -d
    ```

5. Перейдите по адресу *http://<host_ip>:8000/docs*
