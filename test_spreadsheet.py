import unittest
from spreadsheet import Spreadsheet
from decimal import Decimal

class SpreadsheetTest(unittest.TestCase):
    def setUp(self):
        self.spreadsheet = Spreadsheet()

    def test_cell_value_set_and_get(self):
        self.spreadsheet.set_cell_value("A1", 13)
        self.assertEqual(13, self.spreadsheet.get_cell_value("A1"))

    def test_cell_addition(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 20)
        self.spreadsheet.set_cell_value("A3", "=A1+A2")
        self.assertEqual(30.0, self.spreadsheet.get_cell_value("A3"))

    def test_cell_addition_multiple(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 20)
        self.spreadsheet.set_cell_value("A3", "=A1+A2")
        self.spreadsheet.set_cell_value("A4", "=A1+A2+A3")
        self.assertEqual(60.0, self.spreadsheet.get_cell_value("A4"))

    def test_circular_dependency(self):
        self.spreadsheet.set_cell_value("A1", "=A2")
        with self.assertRaises(ValueError) as context:
            self.spreadsheet.set_cell_value("A2", "=A1")
        self.assertEqual("Circular reference detected", str(context.exception))

    def test_non_existent_cell(self):
        with self.assertRaises(ValueError) as context:
            self.spreadsheet.get_cell_value("B1")
        self.assertEqual("Cell does not exist", str(context.exception))

    def test_invalid_cell_id(self):
        with self.assertRaises(ValueError):
            self.spreadsheet.set_cell_value(None, 10)
        with self.assertRaises(ValueError):
            self.spreadsheet.set_cell_value("", 10)

    def test_undo(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 20)
        self.spreadsheet.set_cell_value("A3", "=A1+A2")
        self.spreadsheet.undo()
        with self.assertRaises(ValueError) as context:
            self.spreadsheet.get_cell_value("A3")
        self.assertEqual("Cell does not exist", str(context.exception))

    def test_redo(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 20)
        self.spreadsheet.set_cell_value("A3", "=A1+A2")
        self.spreadsheet.undo()
        self.spreadsheet.redo()
        self.assertEqual(30.0, self.spreadsheet.get_cell_value("A3"))

    def test_non_integer_values(self):
        self.spreadsheet.set_cell_value("A1", 10.5)
        self.spreadsheet.set_cell_value("A2", 20.5)
        self.spreadsheet.set_cell_value("A3", "=A1+A2")
        self.assertEqual(31.0, self.spreadsheet.get_cell_value("A3"))

    def test_formula_preservation(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 20)
        self.spreadsheet.set_cell_value("A3", "=A1+A2")
        self.spreadsheet.undo()
        self.spreadsheet.redo()
        self.spreadsheet.set_cell_value("A1", 5)
        self.assertEqual(25.0, self.spreadsheet.get_cell_value("A3"))

    def test_empty_cell_id(self):
        with self.assertRaises(ValueError):
            self.spreadsheet.set_cell_value("", 1)

    def test_number_cell_id(self):
        with self.assertRaises(ValueError):
            self.spreadsheet.set_cell_value("123", 1)

    def test_null_cell_id(self):
        with self.assertRaises(ValueError):
            self.spreadsheet.set_cell_value(None, 1)

    def test_invalid_expression(self):
        self.spreadsheet.set_cell_value("A1", "=B1 + ")
        with self.assertRaises(ValueError) as context:
            self.spreadsheet.get_cell_value("A1")
        error_message = str(context.exception)
        expected_message = "Invalid formula in cell A1: Invalid expression: Invalid syntax in formula"
        self.assertEqual(expected_message, error_message)

    def test_formula_calculation(self):
        self.spreadsheet.set_cell_value("B1", 2)
        self.spreadsheet.set_cell_value("A1", "=B1 + 2")
        self.assertEqual(4.0, self.spreadsheet.get_cell_value("A1"))

    def test_multiplication(self):
        self.spreadsheet.set_cell_value("A1", 3)
        self.spreadsheet.set_cell_value("A2", 4)
        self.spreadsheet.set_cell_value("B1", "=A1 * A2")
        self.assertEqual(12.0, self.spreadsheet.get_cell_value("B1"))

    def test_subtraction(self):
        self.spreadsheet.set_cell_value("A1", 5)
        self.spreadsheet.set_cell_value("A2", 2)
        self.spreadsheet.set_cell_value("B1", "=A1 - A2")
        self.assertEqual(3.0, self.spreadsheet.get_cell_value("B1"))

    def test_string_cell_value(self):
        self.spreadsheet.set_cell_value("A1", "Hello World")
        self.assertEqual("Hello World", self.spreadsheet.get_cell_value("A1"))

    def test_undo_with_no_history(self):
        try:
            self.spreadsheet.undo()
        except Exception:
            self.fail("Exception was not expected")

    def test_redo_with_no_future(self):
        try:
            self.spreadsheet.redo()
        except Exception:
            self.fail("Exception was not expected")

    def test_formula_with_multiple_spaces(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 20)
        self.spreadsheet.set_cell_value("A3", "= A1  +   A2")
        self.assertEqual(30.0, self.spreadsheet.get_cell_value("A3"))

    def test_cell_reference_update(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", "=A1")
        self.spreadsheet.set_cell_value("A1", 20)
        self.assertEqual(20.0, self.spreadsheet.get_cell_value("A2"))

    def test_complex_formulas(self):
        self.spreadsheet.set_cell_value("A1", 5)
        self.spreadsheet.set_cell_value("A2", 3)
        self.spreadsheet.set_cell_value("A3", "=A1 + (A2 * 2)")
        self.assertEqual(11.0, self.spreadsheet.get_cell_value("A3"))

    def test_error_handling(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 0)
        self.spreadsheet.set_cell_value("A3", "=A1 / A2")
        with self.assertRaises(ValueError):
            self.spreadsheet.get_cell_value("B1")

    def test_division(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 2)
        self.spreadsheet.set_cell_value("B1", "=A1 / A2")
        result = self.spreadsheet.get_cell_value("B1")
        self.assertEqual(5, result)

    def test_multiple_operations(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 2)
        self.spreadsheet.set_cell_value("A3", 3)
        self.spreadsheet.set_cell_value("B1", "=A1 * A2 / A3")
        result = self.spreadsheet.get_cell_value("B1")
        self.assertAlmostEqual(6.666666666666667, result)

    def test_cell_history(self):
        self.spreadsheet.set_cell_value("A1", 1)
        self.spreadsheet.set_cell_value("A1", 2)
        self.spreadsheet.undo()
        self.assertEqual(1, self.spreadsheet.get_cell_value("A1"))

    def test_division_by_zero(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", 0)
        self.spreadsheet.set_cell_value("B1", "=A1 / A2")
        result = self.spreadsheet.get_cell_value("B1")
        self.assertEqual("NaN", result)

    def test_multiple_undo_redo(self):
        self.spreadsheet.set_cell_value("A1", 1)
        self.spreadsheet.set_cell_value("A1", 2)
        self.spreadsheet.set_cell_value("A1", 3)
        self.spreadsheet.undo()
        self.spreadsheet.undo()
        self.assertEqual(1, self.spreadsheet.get_cell_value("A1"))
        self.spreadsheet.redo()
        self.assertEqual(2, self.spreadsheet.get_cell_value("A1"))

    def test_undo_redo_with_formula(self):
        self.spreadsheet.set_cell_value("A1", 10)
        self.spreadsheet.set_cell_value("A2", "=A1*2")
        self.spreadsheet.set_cell_value("A1", 20)
        self.spreadsheet.undo()
        self.assertEqual(20.0, self.spreadsheet.get_cell_value("A2"))
        self.spreadsheet.redo()
        self.assertEqual(40.0, self.spreadsheet.get_cell_value("A2"))

    def test_circular_dependency(self):
        self.spreadsheet.set_cell_value("A1", "=B1")
        self.spreadsheet.set_cell_value("B1", "=C1")
        with self.assertRaises(ValueError):
            self.spreadsheet.set_cell_value("C1", "=A1")

    def test_no_circular_dependency(self):
        self.spreadsheet.set_cell_value("A1", "=B1")
        self.spreadsheet.set_cell_value("B1", "=C1")
        self.spreadsheet.set_cell_value("C1", 42)
        try:
            self.spreadsheet.get_cell_value("A1")
            self.spreadsheet.get_cell_value("B1")
            self.spreadsheet.get_cell_value("C1")
        except ValueError:
            self.fail("Circular reference detected incorrectly")

if __name__ == '__main__':
    unittest.main()
