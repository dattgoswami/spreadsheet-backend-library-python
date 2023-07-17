# Spreadsheet Backend Library

This is a Python library which simulates a basic spreadsheet program. This program allows the users to create cells in a spreadsheet, assign values to these cells, and perform calculations using formulas. The library also supports undo and redo operations.

## Overview

In the Spreadsheet.py, the basic unit of a spreadsheet is a `Cell` which has an `id` and `value`. The Spreadsheet itself is made up of `Cell` objects and maintains a history and future (used for undo and redo operations), dependencies between cells, and formulas for cells.

Cells can be assigned a numerical value or a formula. Formulas start with an `=` sign and support basic arithmetic operations like addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`).

Dependencies between cells are tracked to handle formulas that reference other cells. When a cell's value changes, any cell that depends on it will be updated as well.

Here is an example of how cells are related with dependencies. Suppose we have three cells: `A1`, `A2`, `A3`. `A1` has a value of `10`, `A2` has a value of `20` and `A3` has a formula `=A1+A2`. In this case, `A3` is dependent on `A1` and `A2`.

Error handling is also taken into account, especially for circular references in the formulas and invalid formulas.

## Stack

1. **Python:** The entire library is written in Python, utilizing its extensive standard library.
2. **Sympy:** A Python library for symbolic mathematics, used to parse and calculate the results of the formulas.
3. **Logging:** Python's built-in logging framework is used to log any errors or exceptions.
4. **Unittest:** Python's built-in unittest module is used for testing.

## Quickstart

You can start using the library by creating an instance of the `Spreadsheet` class and using its methods to manipulate the cells.

```python
from spreadsheet import Spreadsheet

# Create a spreadsheet
ss = Spreadsheet()

# Add cell value
ss.set_cell_value("A1", 10)

# Get cell value
print(ss.get_cell_value("A1"))  # Outputs: 10

# Add a formula to cell
ss.set_cell_value("A2", "=A1*2")

# Get the result of the formula
print(ss.get_cell_value("A2"))  # Outputs: 20

# Undo the last operation
ss.undo()

# Redo the last undone operation
ss.redo()
```

## Running Tests

The unit tests can be run using Python's built-in unittest module. From the terminal, navigate to the folder containing `test_spreadsheet.py` and run the following command:

```bash
python3 -m unittest test_spreadsheet.py
```

The tests will automatically run and provide a report detailing any failed or successful tests.

---

Note: This library only supports basic operations and does not handle advanced features such as cell formatting, date/time operations, and non-arithmetic functions.

# Running Main.py

To run the main script `main.py`, follow the instructions below.

Ensure that Python is installed on your system. This project uses Python 3 and may not work correctly with Python 2. You can check your Python version by opening a terminal and running the following command:

```bash
python --version
```

If Python 3 is not installed, refer to the Python [official site](https://www.python.org/downloads/) for installation instructions.

Once Python 3 is installed, navigate to the project directory and run `main.py` using the following command:

```bash
python3 main.py
```

The `main.py` script is the primary entry point to the Spreadsheet program. Running it will start the application, where you can interactively create and manipulate cells in your spreadsheet using the methods provided by the `Spreadsheet` class.

Remember to use the valid cell ID format (e.g., "A1", "B2", etc.) when interacting with the spreadsheet.

Enjoy exploring the functionality of your simple, yet powerful, Spreadsheet application!
