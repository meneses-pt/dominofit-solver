import os
import sys
from enum import Enum


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath("../")

    return os.path.join(base_path, relative_path)


class PiecePart(Enum):
    VerticalTop = (resource_path("images/vt.png"), 1)
    VerticalBottom = (resource_path("images/vb.png"), 0)
    HorizontalLeft = (resource_path("images/hl.png"), 0)
    HorizontalRight = (resource_path("images/hr.png"), 2)

    @property
    def image_path(self) -> str:
        return self.value[0]

    @property
    def cell_value(self) -> int:
        return self.value[1]


MatrixRow = list[int | PiecePart]
Matrix = list[MatrixRow]
