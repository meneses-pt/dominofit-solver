from enum import Enum


class PiecePart(Enum):
    VerticalTop = ("../images/vt.png", 1)
    VerticalBottom = ("../images/vb.png", 0)
    HorizontalLeft = ("../images/hl.png", 0)
    HorizontalRight = ("../images/hr.png", 2)

    @property
    def image_path(self) -> str:
        return self.value[0]

    @property
    def cell_value(self) -> int:
        return self.value[1]


MatrixRow = list[int | PiecePart]
Matrix = list[MatrixRow]
