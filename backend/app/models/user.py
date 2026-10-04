"""
Backward-compatible exports for the user model.

The actual User model is defined in domain.py.
This file exists so older imports do not break.
"""

from app.models.domain import User, UserRole

__all__ = ["User", "UserRole"]