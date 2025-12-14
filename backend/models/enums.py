import enum

# Enums
class ContentStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ActiveStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class WoundCategory(str, enum.Enum):
    diabetic_ulcer = "diabetic_ulcer"
    pressure_ulcer = "pressure_ulcer"
    vascular_ulcer = "vascular_ulcer"
    surgery = "surgery"
    burns = "burns"
    general = "general"

class UserRole(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
