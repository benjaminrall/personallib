import math
import random

# Linear interpolation for two values
def lerp(a, b, w):
    return b + w * (a - b)

def sigmoid(x):
    return 1 / (1 + (math.e ** (-x)))

# Python Matrix object
# Stores matrices as 2D lists and has static methods to use on matrices
# Dependencies : None
class Matrix:
    def __init__(self, r, c):
        self.matrix = []            # Matrix stored as a 2D list
        self.columns = []           # A list of the columns in the matrix
        for i in range(r):          # Default matrix setup
            row = []
            for j in range(c):
                row.append(random.randint(-10, 10))
            self.matrix.append(row)
        self.dimensions = (r, c)    # Stores matrix dimensions to check validity of operations
        self.calculate_columns()    # Finds columns in matrix

    # Sets a specified index i row to be equal to parameter row v
    def set_row(self, i, v):
        if len(v) != self.dimensions[1]:
            print("Invalid row size")
            return
        self.matrix[i] = v
        self.calculate_columns()

    # Sets a specified index i column to be equal to parameter column v
    def set_column(self, i, v):
        if len(v) != self.dimensions[0]:
            print("Invalid column size")
            return
        for r in range(len(self.matrix)):
            self.matrix[r][i] = v[r]
        self.calculate_columns()

    # Finds columns in matrix
    def calculate_columns(self):
        self.columns = [ n for n in zip(*self.matrix)]

    # Returns matrix in string form to be nicely displayed or stored
    def display(self):
        total = ""
        rowLength = 0
        for row in self.matrix:
            r = "\n|"
            for item in row:
                r += str(item) + " "
            total +=  r[0:-1] + "|"
            rowLength = max(rowLength, len(r[0:-1]))
        caps = ""
        for i in range(rowLength):
            caps += "_"
        total = caps + total + "\n" + caps
        return total
    
    # Static method to add two matrices together
    @staticmethod
    def add(m1, m2):
        if m1.dimensions != m2.dimensions:
            print("Invalid matrix dimensions")
            return m1
        result = Matrix(m1.dimensions[0], m2.dimensions[1])
        for i in range(m1.dimensions[0]):
            row = m1.matrix[i]
            for j, item in enumerate(m2.matrix[i]):
                row[j] += item
            result.set_row(i, row)
        return result

    # Static method to multiply two matrices together
    @staticmethod 
    def multiply(m1, m2):
        if m1.dimensions[1] != m2.dimensions[0]:
            print("Invalid matrix dimensions")
            return m1
        result = Matrix(m1.dimensions[0], m2.dimensions[1])
        for row in range(m1.dimensions[0]):
            newRow = []
            for col in range(m2.dimensions[1]):
                newRow.append(sum([ i[0] * i[1] for i in zip(m1.matrix[row], m2.columns[col]) ]))
            result.set_row(row, newRow)
        return result

    # Returns the determinant of a given matrix
    @staticmethod
    def determinant(m):
        if(len(m) == 2):
            value = m[0][0] * m[1][1] - m[1][0] * m[0][1]
            return value
        sum = 0
        for col in range(len(m)):
            sign = (-1) ** (col)
            d = Matrix.determinant(Matrix.get_cofactor(m, 0, col))
            sum += (sign * m[0][col] * d)
        return sum

    # Gets a sub-matrix to use for determinant calculation
    @staticmethod
    def get_cofactor(m, i, j):
        return [row[: j] + row[j+1:] for row in (m[: i] + m[i+1:])]

# Python Vector2 object
# Stores 2D vectors as a tuple and has static methods to use with vectors
# Dependencies : math
class Vector2:
    def __init__(self, x, y):
        self.x = x                          # The x component of the vector
        self.y = y                          # The y component of the vecor
        self.vector = (x, y)                # The vector as a tuple
        self.magnitude =  math.hypot(x, y)  # The magnitude of the vector

    # Adds 2 vectors together and returns as a vector
    @staticmethod
    def add(v1, v2):
        return Vector2(v1.x + v2.x, v1.y + v2.y)

    # Subtracts one vector from another and returns as a vector
    @staticmethod
    def subtract(v1, v2):
        return Vector2(v1.x - v2.x, v1.y - v2.y)

    # Finds the dot product of two vectors
    @staticmethod
    def dot(v1, v2):
        return sum([i[0] * i[1] for i in zip(v1.vector, v2.vector)])

    # Returns the unit vector of the given vector
    @staticmethod
    def unit(v):
        return Vector2(v.x / v.magnitude, v.y / v.magnitude)