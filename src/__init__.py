"""
GhostVision Source Package
Contains modules for gesture recognition, human segmentation, and visual effects.
"""

# Expose core classes and functions for cleaner imports in main.py
from .gesture_recognition import GestureTracker
from .segmentation import HumanSegmenter
from .visual_effects import apply_invisibility

__version__ = "1.0.0"
__author__ = "GhostVision Developer"
