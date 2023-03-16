# Personal Lib History

## 1.0
#
First defined version. Includes `canvas`, `camera` and `maths` libraries.

`maths.py`:
- `lerp(float, float, float) -> float` - Calculates linear interpolation between two values.
- `sigmoid(float) -> float` - Applies the sigmoid function to a value.
- `Matrix` - A class representing a 2D matrix
    - `__init__(int, int)` - Initialises a matrix with a given number of rows and columns
    - `set_row(int, list[float])`: Sets a specified row index to be equal to a given list
    - `set_column(int, list[float])`: Sets a specified column index to be equal to a given list
    - `calculate_columns()`: Calculates the matrix's columns and stores as a separate array
    - `display() -> str`: Returns the matrix in a neat string form to be displayed
    - `add(Matrix, Matrix) -> Matrix`: Returns the sum of two matrices
    - `multiply(Matrix, Matrix) -> Matrix`: Returns the product of two matrices
    - `determinant(Matrix) -> float`: Returns the determinant of a matrix
    - `get_cofactor(Matrix, int, int) -> Matrix`: Gets the cofactor of a specified element
- `Vector2` - A class representing a column vector with 2 elements
    - `__init__(float, float)`: Constructs the vector with the given 2 elements
    - `add(Vector2, Vector2) -> Vector2`: Returns the sum of two vectors
    - `subtract(Vector2, Vector2) -> Vector2`: Returns one vector subtracted from another
    - `dot(Vector2, Vector2) -> float`: Returns the dot product of two vectors
    - `unit(Vector2) -> Vector2`: Returns a vector with the same direction as a given vector but a magnitude of 1


`camera.py`:
- `Camera` - A 2D camera controller for pygame
    - `__init__(Surface, float, float, float)`: Constructs a camera for a given surface at a specified x and y position with a given zoom.
    - `draw_rect(Rect, Colour)`: Draws a rectangle to the camera
    - `get_screen_rect(Rect) -> Rect`: Converts a rect in world coordinates to screen coordinates
    - `draw_circle(Coordinate, float)`: Draws a circle to the camera
    - `get_screen_circle(Coordinate, float) -> Coordinate, float`: Converts a circle in world coordinates to screen coordinates
    - `draw_line(Coordinate, Coordinate, Colour, int)`: Draws a line between two points to the camera
    - `draw_polygon(list[Coordinate], Colour)`: Draws a polygon to the camera
    - `get_screen_coord(Coordinate) -> Coordinate`: Converts a world coordinate to a screen coordinate
    - `get_world_coord(Coordinate) -> Coordinate`: Converts a screen coordinate to a world coordinate
    - `blit(Surface, Coordinate, [Rect])`: Draws one surface onto another, with an optional specific area to draw
    - `zoom_out(float, [float])`: Zooms the camera out by a certain amount, with a given limit
    - `zoom_in(float, [float])`: Zooms the camera in by a certain amount, with a given limit
    - `zoom_out_step([float])`: Zooms the camera out by one step, with a given limit
    - `zoom_in_step([float])`: Zooms the camera in by one step, with a given limit
    - `pan(Coordinate)`: Pans the camera by a given coordinate
    - `follow(Coordinate, [Coordinate, bool])`: Moves the camera towards a given point with an optional offset and smoothing
    - `set_bounds([Coordinate, Coordinate, list[bool, bool, bool, bool]])`: Sets boundaries for the camera's position, allowing boundary on only some sides to be specified
    - `enforce_bounds()`: Enforces the set boundaries for the camera's position

`canvas.py`: A collection of UI objects that can be drawn to the screen with the Camera object