import logging
import re
from collections import deque
from sympy import sympify, Number, NumberSymbol
from sympy.core.numbers import Float

class Spreadsheet:
    class Cell:
        def __init__(self, id, value):
            self.id = id
            self.value = value

    def __init__(self):
        self.cells = {}
        self.formulas = {}
        self.history = deque()
        self.future = deque()
        self.dependencies = {}
        self.logger = logging.getLogger(__name__)

    def set_cell_value(self, cell_id, value):
        self.validate_cell_id(cell_id)
        if self.is_formula(value):
            self.update_dependencies(cell_id, value)
            self.formulas[cell_id] = value
        elif cell_id in self.formulas:
            del self.formulas[cell_id]
            del self.dependencies[cell_id]
        self.future.clear()
        self.history.append(self.Cell(cell_id, self.cells.get(cell_id, None)))
        self.cells[cell_id] = value

    def get_cell_value(self, cell_id):
        if cell_id not in self.cells:
            self.logger.error("Cell {} does not exist".format(cell_id))
            raise ValueError("Cell does not exist")
        value = self.cells[cell_id]
        if self.is_formula(value):
            if cell_id not in self.formulas:
                self.logger.error(
                    "Formula does not exist for cell {}".format(cell_id))
                raise ValueError("Formula does not exist")
            try:
                return self.evaluate_expression(self.formulas[cell_id][1:], cell_id)
            except ValueError as e:
                self.logger.error(
                    "Invalid formula in cell {}: {}".format(cell_id, str(e)))
                raise ValueError(
                    "Invalid formula in cell {}: {}".format(cell_id, str(e)))
        return value

    def undo(self):
        if not self.history:
            return
        previous_cell = self.history.pop()
        self.future.append(
            self.Cell(previous_cell.id, self.cells.get(previous_cell.id)))
        del self.cells[previous_cell.id]
        if previous_cell.id in self.formulas:
            del self.formulas[previous_cell.id]
            del self.dependencies[previous_cell.id]
        if previous_cell.value is not None:
            self.cells[previous_cell.id] = previous_cell.value
            if self.is_formula(previous_cell.value):
                self.update_dependencies(previous_cell.id, previous_cell.value)
                self.formulas[previous_cell.id] = previous_cell.value

    def redo(self):
        if not self.future:
            return
        cell = self.future.pop()
        self.history.append(cell)
        self.cells[cell.id] = cell.value
        if self.is_formula(cell.value):
            self.formulas[cell.id] = cell.value

    def validate_cell_id(self, cell_id):
        if cell_id is None or cell_id == '':
            self.logger.error("Invalid cellId")
            raise ValueError("Invalid cellId")
        if not re.match("[A-Z]+[1-9][0-9]*", cell_id):
            self.logger.error("Invalid cellId format")
            raise ValueError("Invalid cellId format")

    def update_dependencies(self, cell_id, formula):
        new_dependencies = self.extract_dependencies_from_formula(formula)
        self.dependencies[cell_id] = new_dependencies
        if self.detect_circular_dependency(cell_id):
            self.logger.error(
                "Circular reference detected in cell {}".format(cell_id))
            raise ValueError("Circular reference detected")

    def extract_dependencies_from_formula(self, formula):
        dependencies = set()
        parts = re.split("(?<=[+\\-*/])|(?=[+\\-*/])", formula[1:])
        for part in parts:
            part = part.strip()
            if not self.is_numeric(part):
                dependencies.add(part)
        return dependencies

    def detect_circular_dependency(self, cell_id):
        visited = set()
        stack = [cell_id]  # Use a stack instead of a queue for depth-first search
        while stack:
            current_cell = stack.pop()
            visited.add(current_cell)
            dependents = self.dependencies.get(current_cell, set())
            for dependent in dependents:
                if dependent == cell_id:
                    self.logger.warning(
                        "Circular dependency detected for cellId: {}".format(cell_id))
                    return True
                if dependent not in visited:
                    stack.append(dependent)
        return False

    def is_numeric(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_formula(self, value):
        return isinstance(value, str) and value[0] == '='

    def evaluate_expression(self, expression, current_cell_id):
        try:
            result = self.prepare_expression(expression, current_cell_id)
            self.logger.debug(
                "Result of the expression {}: {}".format(expression, result))
            return result
        except ValueError as e:
            self.logger.error("Invalid expression: " + str(e))
            raise ValueError("Invalid expression: " + str(e))

    def prepare_expression(self, expression, current_cell_id):
        processed_expression = self.preprocess_expression(
            expression, current_cell_id)
        self.validate_expression_syntax(processed_expression)
        return self.calculate_expression(processed_expression)

    def calculate_expression(self, expression):
        try:
            expr = sympify(expression)
            if isinstance(expr, NumberSymbol):
                return float(expr)
            elif isinstance(expr, Number) and expr.is_real:
                return float(expr)
            else:
                return 'NaN'
        except ZeroDivisionError:
            self.logger.error(
                "Error in calculations. Division by zero: {}".format(expression))
            return 'NaN'
        except Exception:
            self.logger.error(
                "Error in calculations. Expression: {}".format(expression))
            raise ValueError("Error in calculations")

    def preprocess_expression(self, expression, current_cell_id):
        for cell_id in self.cells.keys():
            if cell_id in expression:
                if current_cell_id in self.dependencies.get(cell_id, set()):
                    self.logger.error(
                        "Circular reference detected in expression: {}".format(expression))
                    raise ValueError("Circular reference detected")
                value = self.get_cell_value(cell_id)
                expression = re.sub("\\b" + cell_id + "\\b",
                                    str(value), expression)
        return expression

    def validate_expression_syntax(self, expression):
        try:
            sympify(expression)
        except Exception:
            self.logger.error(
                "Invalid syntax in formula: {}".format(expression))
            raise ValueError("Invalid syntax in formula")
