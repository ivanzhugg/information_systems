import re


class Supplier:
    def __init__(
        self,
        supplier_id: int,
        name: str,
        address: str,
        phone: str,
    ) -> None:
        Supplier.validate_supplier_id(supplier_id)
        Supplier.validate_name(name)
        Supplier.validate_address(address)
        Supplier.validate_phone(phone)

        self.__supplier_id = supplier_id
        self.__name = name.strip()
        self.__address = address.strip()
        self.__phone = phone.strip()

    @staticmethod
    def validate_supplier_id(value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Идентификатор должен быть целым числом")
        if not 1 <= value <= 9223372036854775807:
            raise ValueError("Идентификатор должен быть от 1 до 9223372036854775807")

    @staticmethod
    def validate_name(value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Название должно быть строкой")
        if not value.strip():
            raise ValueError("Название не должно быть пустым")
        if len(value.strip()) > 200:
            raise ValueError("Название должно содержать не более 200 символов")

    @staticmethod
    def validate_address(value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Адрес должен быть строкой")
        if not value.strip():
            raise ValueError("Адрес не должен быть пустым")
        if len(value.strip()) > 300:
            raise ValueError("Адрес должен содержать не более 300 символов")

    @staticmethod
    def validate_phone(value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Телефон должен быть строкой")
        if re.fullmatch(r"\+?[0-9]{7,15}", value.strip()) is None:
            raise ValueError("Телефон должен содержать 7–15 цифр и необязательный + в начале")

    @property
    def supplier_id(self) -> int:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        Supplier.validate_name(value)
        self.__name = value.strip()

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str) -> None:
        Supplier.validate_address(value)
        self.__address = value.strip()

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        Supplier.validate_phone(value)
        self.__phone = value.strip()


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
