#!/usr/bin/env python3
"""blueprint user"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Blueprint for all User
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
