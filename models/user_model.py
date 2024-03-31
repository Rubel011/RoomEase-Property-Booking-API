from mongoengine import Document, StringField, ValidationError


class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    username = StringField(required=True)
    ROLES = ("user", "admin", "super_admin")
    role = StringField(default="user", choices=ROLES)

    def clean(self):
        # Validate role field
        if self.role not in self.ROLES:
            raise ValidationError(
                f"Invalid role '{self.role}'. Allowed roles are: {', '.join(self.ROLES)}")
