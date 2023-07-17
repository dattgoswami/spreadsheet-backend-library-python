from spreadsheet import Spreadsheet

spreadsheet = Spreadsheet()
spreadsheet.set_cell_value("A1", 13)
spreadsheet.set_cell_value("A2", 14)
spreadsheet.set_cell_value("A3", "=A1+A2")
spreadsheet.set_cell_value("A4", "=A1+A2+A3")
print("A1:", spreadsheet.get_cell_value("A1"))
print("A2:", spreadsheet.get_cell_value("A2"))
print("A3:", spreadsheet.get_cell_value("A3"))
print("A4:", spreadsheet.get_cell_value("A4"))
spreadsheet.set_cell_value("B1", "Hello")
spreadsheet.set_cell_value("C1", "=A1 + 10")
print("B1:", spreadsheet.get_cell_value("B1"))
print("C1:", spreadsheet.get_cell_value("C1"))
spreadsheet.undo()
try:
    print("C1 after undo:", spreadsheet.get_cell_value("C1"))
except ValueError as e:
    print(e)
spreadsheet.redo()
print("C1 after redo:", spreadsheet.get_cell_value("C1"))
spreadsheet.set_cell_value("C2", 1.5)
print("C2:", spreadsheet.get_cell_value("C2"))
spreadsheet.set_cell_value("A7", "=A4-A1")
spreadsheet.set_cell_value("A8", "=A1*A2")
spreadsheet.set_cell_value("A9", "=A4/A3")
print("A7:", spreadsheet.get_cell_value("A7"))
print("A8:", spreadsheet.get_cell_value("A8"))
print("A9:", spreadsheet.get_cell_value("A9"))
spreadsheet.set_cell_value("A12", "=A2+A1")
spreadsheet.set_cell_value("A12", "=A2-A1")
spreadsheet.undo()
print("A12:", spreadsheet.get_cell_value("A12"))
spreadsheet.redo()
print("A12:", spreadsheet.get_cell_value("A12"))
spreadsheet.set_cell_value("A1", 10)
spreadsheet.set_cell_value("A2", "=A1")
spreadsheet.set_cell_value("A1", 20)
print("A2:", spreadsheet.get_cell_value("A2"))
try:
    spreadsheet.set_cell_value("121", "10")
except ValueError as e:
    print(e)
