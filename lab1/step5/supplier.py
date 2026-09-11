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
    supplier = Supplier(1, "Автодеталь", "Москва", "+74951234567")
    print("Создан:", supplier.supplier_id, supplier.name, supplier.address, supplier.phone)
    supplier.name = "Автоснаб"
    print("Новое название:", supplier.name)
    try:
        supplier.phone = "123"
    except ValueError as error:
        print("Ошибка:", error)
    print("Телефон остался прежним:", supplier.phone)
