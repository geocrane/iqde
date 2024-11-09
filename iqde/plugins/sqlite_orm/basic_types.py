class BaseType:
    field_type: str

    def __init__(
        self,
        primary_key: bool = False,
        autoincrement: bool = False,
        unique: bool = False,
        null: bool = True,
        default: int = None,
    ):
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.unique = unique
        self.null = null
        self.default = default


class IntegerField(BaseType):
    field_type = "INTEGER"


class TextField(BaseType):
    field_type = "TEXT"


class RealField(BaseType):
    field_type = "REAL"


class ForeignKey(BaseType):
    field_type = "FOREIGN_KEY"

    def __init__(
        self,
        object_class: type,
        foreign_field: str,
        unique: bool = False,
        null: bool = True,
        default=None,
        primary_key: bool = False,
        autoincrement: bool = False,
    ):
        self.object_class = (object_class,)
        self.foreign_field = (foreign_field,)
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.unique = unique
        self.null = null
        self.default = default
