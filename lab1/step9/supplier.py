import json
import re


class SupplierShort:
    def __init__(self, supplier_id: int, name: str, phone: str) -> None:
        supplier_id = SupplierShort.validate_supplier_id(supplier_id)
        name = SupplierShort.validate_name(name)
        phone = SupplierShort.validate_phone(phone)

        self.__supplier_id = supplier_id
        self.__name = name
        self.__phone = phone

    @staticmethod
    def from_supplier(supplier: "Supplier") -> "SupplierShort":
        if not isinstance(supplier, Supplier):
            raise TypeError("Ожидается объект Supplier")
        return SupplierShort(supplier.supplier_id, supplier.name, supplier.phone)

    @staticmethod
    def _validate_text(value: str, field: str, max_length: int) -> str:
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
        return SupplierShort._validate_text(value, "Название", 200)

    @staticmethod
    def validate_phone(value: str) -> str:
        value = SupplierShort._validate_text(value, "Телефон", 30)
        if re.fullmatch(r"\+?[0-9]{7,15}", value) is None:
            raise ValueError("Телефон должен содержать 7–15 цифр и необязательный + в начале")
        return value

    def __str__(self) -> str:
        return self.to_short_string()

    def to_short_string(self) -> str:
        return f"{self.__name}, {self.__phone}"

    def __eq__(self, other: object) -> bool:
        """Поставщики равны при совпадении типа и идентификатора."""
        if type(self) is not type(other):
            return NotImplemented
        return self.__supplier_id == other.__supplier_id

    @property
    def supplier_id(self) -> int:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = SupplierShort.validate_name(value)

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        self.__phone = SupplierShort.validate_phone(value)


class Supplier(SupplierShort):
    def __init__(
        self,
        supplier_id: int,
        name: str,
        address: str,
        phone: str,
    ) -> None:
        address = Supplier.validate_address(address)
        super().__init__(supplier_id, name, phone)
        self.__address = address

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
    def validate_address(value: str) -> str:
        return SupplierShort._validate_text(value, "Адрес", 300)

    def __str__(self) -> str:
        return (
            f"Поставщик #{self.supplier_id}: {self.name}; "
            f"адрес: {self.__address}; телефон: {self.phone}"
        )

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str) -> None:
        self.__address = Supplier.validate_address(value)


if __name__ == "__main__":
    supplier = Supplier(1, "Автодеталь", "Москва", "+74951234567")
    same_supplier = Supplier.from_string("1;Автодеталь;Тула;+74871234567")
    other_supplier = Supplier.from_json(
        '{"supplier_id": 2, "name": "Автомир", "address": "Казань", "phone": "+78431234567"}'
    )
    short_supplier = SupplierShort.from_supplier(supplier)
    print("Полная версия:", supplier)
    print("Краткая версия:", supplier.to_short_string())
    print("Краткий объект:", short_supplier)
    print("Supplier наследует SupplierShort:", isinstance(supplier, SupplierShort))
    print("Одинаковый ID:", supplier == same_supplier)
    print("Разные ID:", supplier == other_supplier)
    print("Полный и краткий объекты равны:", supplier == short_supplier)
    supplier.name = "Новое название"
    print("Унаследованный сеттер:", supplier.name)
    print("Независимая краткая копия:", short_supplier)
    try:
        supplier.phone = "123"
    except ValueError as error:
        print("Ошибка:", error)
    print("Телефон остался прежним:", supplier.phone)
