"""
__init__.py - models package
"""

from .trainer import train
from .predictor import LotLPredictor

__all__ = ["train", "LotLPredictor"]

