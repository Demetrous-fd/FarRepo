### Требования для запуска:
- Python 3.11
 
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

3. Создайте виртуальное окружение и активируйте его
   ```shell
   python -m venv venv
   ```

4. Установить зависимости
   ```shell
   pip install -r requirements.txt
   ```

5. Выполните миграцию
   ```shell
   alembic upgrade head
   ```

6. Запустить сервисы
    ```shell
    uvicorn app:app
    celery -A app:celery worker --loglevel=INFO
    celery -A app:celery beat --loglevel=INFO -S redbeat.RedBeatScheduler
    ```
    
7. Перейдите по адресу *http://<host_ip>:8000/docs*

