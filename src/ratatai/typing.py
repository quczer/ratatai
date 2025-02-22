"""Define type aliases and type hints for Ratatai."""

from pathlib import Path
from typing import NewType

Speech = NewType("Speech", Path)
