# Модуль з допоміжними функціями
- `HEADER_LENGHT = 90` - ширина заголовків;
- `print_header(_text)` - виводить в консоль заголовок;
- `print_footer (_text)` - виводить в консоль повідомленн про завершення;
- `print_execution_time(func)` - декоратор, що вимірює та виводить час виконання декорованої функції;
- `Application` - шаблон класу застосунку.

## Збірка модуля
Перед збіркою та інсталяцією модуля за допомогою команди `pip list | grep wheel` переконуємось, що в системі встановлено `wheel`.

Далі виконуємо збірку:
```
cd helpers
python setup.py sdist bdist_wheel
pip install .
```
## Генерація списку залежностей
- Створення списку: `pip freeze > requirements.txt` 
- Інсталювання залежностей: `pip install -r requirements.txt`