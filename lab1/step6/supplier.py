import json
import re


class Supplier:
    def __init__(
        self,
        supplier_id: int,
        name: str,
        address: str,
        phone: str,
    ) -> None:
        supplier_id = Supplier.validate_supplier_id(supplier_id)
        name = Supplier.validate_name(name)
        address = Supplier.validate_address(address)
        phone = Supplier.validate_phone(phone)

        self.__supplier_id = supplier_id
        self.__name = name
        self.__address = address
        self.__phone = phone

    @classmethod
    def from_string(cls, text: str) -> "Supplier":
        """Формат: идентификатор;название;адрес;телефон."""
        if not isinstance(text, str):
            raise TypeError("Данные должны быть строкой")
        fields = text.split(";")
        if len(fields) != 4:
            raise ValueError("Ожидается формат: идентификатор;название;адрес;телефон")
        try:
            supplier_id = int(fields[0])
        except ValueError:
            raise ValueError("Идентификатор должен быть целым числом") from None
        return cls(supplier_id, fields[1], fields[2], fields[3])

    @classmethod
    def from_json(cls, text: str) -> "Supplier":
        if not isinstance(text, str):
            raise TypeError("JSON должен быть строкой")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("Некорректный JSON") from None
        if not isinstance(data, dict):
            raise ValueError("JSON должен содержать объект")
        if set(data) != {"supplier_id", "name", "address", "phone"}:
            raise ValueError("JSON должен содержать только supplier_id, name, address и phone")
        return cls(**data)

    @staticmethod
    def __validate_text(value: str, field: str, max_length: int) -> str:
        if not isinstance(value, str):
            raise TypeError(f"Поле «{field}» должно быть строкой")
        value = value.strip()
        if not value:
            raise ValueError(f"Поле «{field}» не должно быть пустым")
        if len(value) > max_length:
            raise ValueError(f"Поле «{field}» должно содержать не более {max_length} символов")
        return value

    @staticmethod
    def validate_supplier_id(value: int) -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Идентификатор должен быть целым числом")
        if not 1 <= value <= 9223372036854775807:
            raise ValueError("Идентификатор должен быть от 1 до 9223372036854775807")
        return value

    @staticmethod
    def validate_name(value: str) -> str:
        return Supplier.__validate_text(value, "Название", 200)

    @staticmethod
    def validate_address(value: str) -> str:
        return Supplier.__validate_text(value, "Адрес", 300)

    @staticmethod
    def validate_phone(value: str) -> str:
        value = Supplier.__validate_text(value, "Телефон", 30)
        if re.fullmatch(r"\+?[0-9]{7,15}", value) is None:
            raise ValueError("Телефон должен содержать 7–15 цифр и необязательный + в начале")
        return value

    @property
    def supplier_id(self) -> int:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = Supplier.validate_name(value)

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str) -> None:
        self.__address = Supplier.validate_address(value)

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        self.__phone = Supplier.validate_phone(value)


if __name__ == "__main__":
    from_text = Supplier.from_string("2;Автоснаб;Тула;+74871234567")
    from_json = Supplier.from_json(
        '{"supplier_id": 3, "name": "Автомир", "address": "Казань", "phone": "+78431234567"}'
    )
    print("Из строки:", from_text.supplier_id, from_text.name, from_text.address, from_text.phone)
    print("Из JSON:", from_json.supplier_id, from_json.name, from_json.address, from_json.phone)
    supplier = Supplier(1, "Автодеталь", "Москва", "+74951234567")
    print("Создан:", supplier.supplier_id, supplier.name, supplier.address, supplier.phone)
    supplier.name = "Автоснаб"
    print("Новое название:", supplier.name)
    try:
        supplier.phone = "123"
    except ValueError as error:
        print("Ошибка:", error)
    print("Телефон остался прежним:", supplier.phone)
