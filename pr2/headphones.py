class InvalidProductData(Exception):
    """Исключение, если ввели какие-то кривые данные"""
    pass


class Headphones:
    ALLOWED_FORM_FACTORS = {'вкладыши', 'накладные', 'вставные', 'полноразмерные'}

    def __init__(self, data: dict):
        try:
            self.brand = self._validate_str(data, 'brand', required=True)
            self.wireless = self._validate_bool(data, 'wireless', required=True)
            self.impedance = self._validate_number(data, 'impedance', required=True)
            self.color = self._validate_str(data, 'color', required=True)
            self.form_factor = self._validate_choice(data, 'form_factor', self.ALLOWED_FORM_FACTORS, required=True)
            self.noise_cancelling = self._validate_bool(data, 'noise_cancelling', required=False)
            self.weight = self._validate_number(data, 'weight', required=False)
        except Exception as e:
            raise InvalidProductData(f"Ошибка валидации: {e}")

    def _validate_str(self, data, key, required):
        value = data.get(key)
        if value is None:
            if required:
                raise ValueError(f"Поле '{key}' обязательно и должно быть строкой")
            return None
        if not isinstance(value, str):
            raise ValueError(f"Поле '{key}' должно быть строкой")
        return value

    def _validate_bool(self, data, key, required):
        value = data.get(key)
        if value is None:
            if required:
                raise ValueError(f"Поле '{key}' обязательно и должно быть логическим")
            return None
        if not isinstance(value, bool):
            raise ValueError(f"Поле '{key}' должно быть булевым")
        return value

    def _validate_number(self, data, key, required):
        value = data.get(key)
        if value is None:
            if required:
                raise ValueError(f"Поле '{key}' обязательно и должно быть числом")
            return None
        if not isinstance(value, (int, float)):
            raise ValueError(f"Поле '{key}' должно быть интом или флоатом")
        return value

    def _validate_choice(self, data, key, choices, required):
        value = data.get(key)
        if value is None:
            if required:
                raise ValueError(f"Поле '{key}' обязательно и должно быть одним из: {choices}.")
            return None
        if value not in choices:
            raise ValueError(f"Поле '{key}' должно быть одним из: {choices}.")
        return value

    def is_portable(self):
        """Портативки, если уши беспроводные и весят до 300 грамм"""
        return self.wireless and (self.weight is not None and self.weight <= 300)
