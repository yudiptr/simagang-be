from enum import Enum

class InternRegistrationStatus(str, Enum):
    ACCEPTED = "Diterima"
    ON_PROCESS = "Diproses"
    REJECTED = "Ditolak"
    DELETED = "Dihapus"