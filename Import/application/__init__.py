"""
application package
"""

__version__ = '1.0'

from .salary import calculate_salary
from .db import get_employees

__all__ = ['calculate_salary', 'get_employees']

