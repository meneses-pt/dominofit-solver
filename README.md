# DominoFit Solver

This is a Python project named "DominoFit Solver". The project is currently at version 0.1.0.

## Description

The DominoFit Solver is a Python application designed to solve specific problems related to the game of Dominoes. More details about the functionality and usage of the application will be provided as the project progresses.

## Installation

This project uses Poetry for dependency management. To install the project and its dependencies, you need to have Poetry installed. If you don't have it, you can install it by following the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

Once you have Poetry installed, you can install the project by running:

```bash
poetry install
```

This will install all the project dependencies as specified in the `pyproject.toml` file.

## Usage

After installing the project, you can run it using the following command:

```bash
poetry run python main.py
```

Replace `main.py` with the name of the script you want to run.

## Build Executable

```bash
pyinstaller --add-data 'images:images' --onefile -n dominofit-solver source/main.py
```

## Code Style

This project uses Black for code formatting, Ruff for linting, and Mypy for type checking. You can run these tools using the provided `_stylescript.sh` script. Make sure to replace the `MY_CONDA_BIN_PREFIX` variable in the script with the path to your virtual environment.

## Contributing

Contributions are welcome. Please make sure to update tests as appropriate and adhere to the code style guidelines.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

For any inquiries, you can reach out to the author at andre@meneses.pt.