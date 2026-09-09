import enum


class Perfil(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"