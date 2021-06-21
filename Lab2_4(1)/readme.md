Чтоб создать индекс:
```gcloud datastore indexes create ```

Чтоб запустить:
1) нужен доступ к google cloud или по адресу:

Команды:
```
. ./venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=~/gcloud.json
export FLASK_ENV=development
export FLASK_APP=flaskr
flask run
```

Тесты:
```
export PYTHONPATH="/home/divaon/Рабочий стол/Lab2_4(1)"
pytest
```