# Модуль `AddressBook` з допоміжними класами
**Класи:**
- `Field`
- `Name`
- `Phone`
- `Record`
- `AddressBook`

## Збірка модуля
Перед збіркою та інсталяцією модуля за допомогою команди `pip list | grep wheel` переконуємось, що в системі встановлено `wheel`.

Далі виконуємо збірку:
```
cd AddressBook
python setup.py sdist bdist_wheel
pip install .
```
## Генерація списку залежностей
- Створення списку: `pip freeze > requirements.txt` 
- Інсталювання залежностей: `pip install -r requirements.txt`