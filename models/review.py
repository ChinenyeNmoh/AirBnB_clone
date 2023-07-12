#!/usr/bin/env python3
"""blueprint Review"""

from models.base_model import BaseModel


class Review(BaseModel):
    """creating instances"""
    place_id = ""
    user_id = ""
    text = ""
