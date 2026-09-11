class Supplier:
    def __init__(
        self,
        supplier_id: int,
        name: str,
        address: str,
        phone: str,
    ) -> None:
        self.__supplier_id = supplier_id
        self.__name = name
        self.__address = address
        self.__phone = phone

    @property
    def supplier_id(self) -> int:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str) -> None:
        self.__address = value

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        self.__phone = value
