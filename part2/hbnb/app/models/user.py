from __future__ import annotations

import re
from typing import Any
from flask_bcrypt import Bcrypt
from hbnb.app.models.base_model import BaseModel

bcrypt = Bcrypt()
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    """
    User entity
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str = None,
        is_admin: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.password = None
        if password:
            self.password = bcrypt.generate_password_hash(password).decode("utf-8")

        self.validate()

    def hash_password(self, password):    #take a plaintext password, hash it using bcrypt
    """Hashes the password before storing it."""
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):   #compare a plaintext password with the hashed password
    """Verifies if the provided password matches the hashed password."""
    if not self.password:
            return False
    return bcrypt.check_password_hash(self.password, password)

    def validate(self) -> None:
        if not isinstance(self.first_name, str) or not self.first_name.strip():
            raise ValueError("first_name is required")
        if len(self.first_name) > 50:
            raise ValueError("first_name must be at most 50 characters")

        if not isinstance(self.last_name, str) or not self.last_name.strip():
            raise ValueError("last_name is required")
        if len(self.last_name) > 50:
            raise ValueError("last_name must be at most 50 characters")

        if not isinstance(self.email, str) or not self.email.strip():
            raise ValueError("email is required")
        if not _EMAIL_RE.match(self.email.strip()):
            raise ValueError("email must be a valid email address")

        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean")
