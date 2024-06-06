import logging
from typing import override

from PyQt6.QtCore import QRegularExpression, QSize, Qt
from PyQt6.QtGui import QIcon, QRegularExpressionValidator
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from source.models import MatrixRow, PiecePart, resource_path
from source.solver import solve_from_matrix

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def button_clicked(msg: str) -> None:
    logger.info(msg)


class SquareButton(QPushButton):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.state = 0
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(50, 50)  # Set a fixed size for the buttons
        self.clicked.connect(lambda: self.button_clicked())

    @override
    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        dimension = max(size.width(), size.height())
        return QSize(dimension, dimension)

    def button_clicked(self) -> None:
        new_color = "grey" if self.state == 0 else "white"
        self.setStyleSheet(f"background-color: {new_color};")
        self.state = 1 if self.state == 0 else 0


class MainWindow(QWidget):
    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__()
        self.stacked_widget = stacked_widget
        self.grid_layout = QGridLayout()
        layout = QVBoxLayout()

        label = QLabel("Please choose the grid size")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        button1 = QPushButton("6x6")
        button1.clicked.connect(lambda: self.start_grid(6))
        layout.addWidget(button1)

        button2 = QPushButton("7x7")
        button2.clicked.connect(lambda: self.start_grid(7))
        layout.addWidget(button2)

        button3 = QPushButton("8x8")
        button3.clicked.connect(lambda: self.start_grid(8))
        layout.addWidget(button3)

        self.setLayout(layout)

        self.row_inputs: list[QLineEdit] = []
        self.column_inputs: list[QLineEdit] = []

    def start_grid(self, grid_size: int) -> None:
        grid_window = QWidget()
        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(11)

        # Create a validator that accepts only non-negative integers
        validator = QRegularExpressionValidator(QRegularExpression("^[0-9]*$"))

        # Add QLineEdit widgets at the top of each column
        for j in range(grid_size):
            input_field = QLineEdit()
            self.column_inputs.append(input_field)
            h_layout = self.create_input_widget(input_field, validator)
            self.grid_layout.addLayout(h_layout, 0, j + 1)  # Add 1 to j to leave space for row input fields

        # Add QLineEdit widgets at the start of each row
        for i in range(grid_size):
            input_field = QLineEdit()
            self.row_inputs.append(input_field)
            h_layout = self.create_input_widget(input_field, validator)
            self.grid_layout.addLayout(h_layout, i + 1, 0)  # Add 1 to i to leave space for column input fields

        for i in range(grid_size):
            for j in range(grid_size):
                button = SquareButton("")
                button.clicked.connect(lambda _, _i=i, _j=j: button_clicked(f"Button {_i},{_j}"))
                self.grid_layout.addWidget(button, i + 1, j + 1)

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)
        calculate_layout = QHBoxLayout()
        calculate_layout.addWidget(calculate_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid_layout)
        main_layout.addLayout(calculate_layout)

        grid_window.setLayout(main_layout)
        self.stacked_widget.addWidget(grid_window)
        self.stacked_widget.setCurrentWidget(grid_window)

    def create_input_widget(self, input_field: QLineEdit, validator: QRegularExpressionValidator) -> QHBoxLayout:
        input_field.setFixedWidth(20)
        input_field.setValidator(validator)
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(input_field)
        h_layout.addStretch(1)
        return h_layout

    def calculate(self) -> None:
        matrix = self.get_matrix()
        try:
            row_inputs: list[int] = [int(input_field.text()) for input_field in self.row_inputs]
            column_inputs: list[int] = [int(input_field.text()) for input_field in self.column_inputs]
        except ValueError:
            show_error_message("Make sure your inputs are correct!")
            return

        try:
            matrix = solve_from_matrix(matrix, row_inputs, column_inputs)
        except IndexError:
            show_error_message("No solution was found")
            return

        self.update_grid(matrix, len(matrix))

    def get_matrix(self) -> list[list[int | PiecePart]]:
        matrix = []
        for i in range(1, self.grid_layout.rowCount()):
            row: MatrixRow = []
            for j in range(1, self.grid_layout.columnCount()):
                item = self.grid_layout.itemAtPosition(i, j)
                if item:
                    button = item.widget()
                    if type(button) is SquareButton:
                        row.append(button.state)
            matrix.append(row)
        logger.info(matrix)  # Print the matrix for debugging purposes
        return matrix

    def update_grid(self, matrix: list[list[int | PiecePart]], grid_size: int) -> None:
        for i in range(1, grid_size + 1):
            for j in range(1, grid_size + 1):
                item = self.grid_layout.itemAtPosition(i, j)
                if item:
                    button = item.widget()
                    if isinstance(button, SquareButton) and isinstance(matrix[i - 1][j - 1], PiecePart):
                        button.setIcon(QIcon(PiecePart(matrix[i - 1][j - 1]).image_path))
                        button.setIconSize(button.size())


def show_error_message(message: str) -> None:
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setWindowTitle("Error")
    error_dialog.setText(message)
    error_dialog.exec()


def main() -> None:
    app = QApplication([])

    app.setWindowIcon(QIcon(resource_path("images/faviconV2.png")))

    stacked_widget = QStackedWidget()
    stacked_widget.setWindowTitle("Domino Fit Solver")

    main_window = MainWindow(stacked_widget)

    stacked_widget.addWidget(main_window)
    stacked_widget.show()

    app.exec()


if __name__ == "__main__":
    main()
