# Idaproject image_resizer

1. Склонируйте к себе данный репо при помощи команды:

    ```code
    git clone https://github.com/kupuk090/idaproject_test.git
    ```

1. Перейдите в папку проекта:

    ```code
    cd idaproject_test
    ```

1. Выполните команду для создания виртуального окружения:

    ```code
    python3 -m venv ./venv
    ```

1. Активируйте созданное виртуальтое окружение при помощи команды:

    ```code
    source venv/bin/activate
    ```

1. Установите необходимые пакеты в активированное окружение при помощи команды:

    ```code
    pip install -r requirements.txt
    ```

1. Проведите миграции БД при помощи команды:

    ```code
    python manage.py makemigrations resizer
    python manage.py migrate resizer
    ```
