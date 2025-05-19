from headphones import Headphones, InvalidProductData

# Корректный пример
valid_data = {
    'brand': 'Sony',
    'wireless': True,
    'impedance': 32,
    'color': 'black',
    'form_factor': 'накладные',
    'noise_cancelling': True,
    'weight': 250
}

try:
    headphones = Headphones(valid_data)
    print("Успешный успех")
    print("Портативки?", "Да" if headphones.is_portable() else "Нет")
except InvalidProductData as e:
    print("Ошибка:", e)


# Пример с ошибкой: неверный тип impedance
invalid_data = {
    'brand': 'Sony',
    'wireless': True,
    'impedance': 'сильно',
    'color': 'black',
    'form_factor': 'накладные',
}

try:
    headphones = Headphones(invalid_data)
except InvalidProductData as e:
    print("Ошибка при создании:", e)



# pydantic

from headphones_pydantic import HeadphonesPydantic
from pydantic import ValidationError

print("\n--- Проверка через pydantic ---")

data = {
    'brand': 'JBL',
    'wireless': True,
    'impedance': 24,
    'color': 'blue',
    'form_factor': 'вставные',
    'weight': 180
}

try:
    hp = HeadphonesPydantic(**data)
    print("Создали, ура. Портативки?", hp.is_portable())
except ValidationError as e:
    print("Ошибка валидации:\n", e)