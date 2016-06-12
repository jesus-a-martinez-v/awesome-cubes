"""
Defines the Cube class used to
process the incoming requests at runtime.
"""


def instantiate_from_raw_data(dictionary):
    """
    Factory method that creates a new cube from raw data from database.
    :param dictionary: dict instance.
    :return: new Cube filled with the data received in the input.
    """
    return Cube(dictionary['dimension'], dictionary['cube'])


class Cube:
    """
    Provides an abstraction of a Cube of integers.
    """

    # NOTE ABOUT INNER REPRESENTATION:
    # ------------------------------------
    # A cube is represented as a dictionary (a.k.a. hash table) for accessibility speed and ease. At first, a cube has
    # all its elements set to 0. Given that we only query the cube by summing the elements within a given range and
    # provided that 0 is the neutral element of the sum, there's no use in storing it. Hence, only the positions with a
    # non-zero value has a (key, value) pair in the dictionary. Example:
    # * 100-dimensional matrix with 5 at position (1, 56, 9):
    #       {'1': {'56': {'9': 5}}}
    # Here's how dimensions are represented:
    #   row: dict; key: int (z-coordinate); value: int (actual element).
    #   matrix: dict; key: int (y-coordinate); value: row.
    #   cube: dict; key: int (x-coordinate); value: matrix.

    def __init__(self, dimension, cube=None):
        """
        Creates a new Cube instance of the specified dimension.
        :param dimension: integer between 1 and 100, inclusive.
        :return: New Cube instance.
        """
        assert isinstance(dimension, int), 'dimension must be of type int.'
        assert 1 <= dimension <= 100, 'dimension must fall in the range [0, 100]'

        self.dimension = dimension

        if cube:
            assert isinstance(cube, dict), 'cube must be of type dict'
            self.cube = cube
        else:
            self.cube = {}  # This represents a cube with all its elements equal to 0.

    def __str__(self):
        """
        :return: human readable representation of a Cube.
        """
        return 'Cube(dimension=%d,cube=%s)' % (self.dimension, self.cube)

    def update(self, x, y, z, value):
        """
        Replaces the element at point (x,y,z) with the input value.
        :param x: X coordinate. Must be between 1 and N, where N is the dimension of the cube.
        :param y: Y coordinate. Must be between 1 and N, where N is the dimension of the cube.
        :param z: Z coordinate. Must be between 1 and N, where N is the dimension of the cube.
        :param value: Value to be set at the (X,Y,Z) point.
        """
        self._validate_integers([x, y, z, value], ['X', 'Y', 'Z', 'value'])
        self._elements_in_range([x, y, z], ['X', 'Y', 'Z'])

        x, y, z = str(x), str(y), str(z)  # Stringify coordinates.
        matrix = self.cube.get(x, {})  # Extract the matrix if it exists, or create a new one.
        row = matrix.get(y, {})  # Extract a row if it exists, or create a new one.

        # Update the row, matrix and cube.
        row[z] = value
        matrix[y] = row
        self.cube[x] = matrix

    def query(self, x_init, x_end, y_init, y_end, z_init, z_end):
        """
        Sums all elements that fall inside the space described by the input parameters.
        :param x_init: Initial X coordinate.
        :param x_end: Final X coordinate.
        :param y_init: Initial Y coordinate.
        :param y_end: Final Y coordinate.
        :param z_init: Initial Z coordinate.
        :param z_end: Final Z coordinate.
        :return: Sum of elements that fall inside the range.
        """
        # Lists used for validation.
        from_ = [x_init, y_init, z_init]
        from_names = ['x_init', 'y_init', 'z_init']
        to_ = [x_end, y_end, z_end]
        to_names = ['x_end', 'y_end', 'z_end']

        # Validate input.
        self._validate_integers(from_ + to_, from_names + to_names)
        self._elements_in_range(from_ + to_, from_names + to_names)
        self._validate_range(from_, to_, from_names, to_names)

        return self._sum_cube(x_init, x_end, y_init, y_end, z_init, z_end)

    # ========================
    # Private helper functions
    # ========================
    def _sum_cube(self, x_init, x_end, y_init, y_end, z_init, z_end):
        """
         Sums elements that complies with the specified range.
        """

        # =============================================================================================
        # Inner helper functions. Defined here because their only purpose is to do their parent's work.
        # =============================================================================================

        def sum_matrix(matrix):
            """
            Sums all matrix's elements.
            """
            matrix_total = 0
            y = y_init

            while y <= y_end:
                y_key = str(y)
                if y_key in matrix:
                    matrix_total += sum_row(matrix[y_key])
                y += 1
            return matrix_total

        def sum_row(row):
            """
            Sums all row's elements.
            """
            row_total = 0
            z = z_init

            while z <= z_end:
                z_key = str(z)
                row_total += row.get(z_key, 0)
                z += 1

            return row_total

        cube_total = 0
        x = x_init  # Iterator var

        while x <= x_end:
            x_key = str(x)
            if x_key in self.cube:
                cube_total += sum_matrix(self.cube[x_key])
            x += 1

        return cube_total

    def _elements_in_range(self, elements, elements_names):
        """
         Validates elements are within the cube's limits.
        """
        error_message = '%s out of range. Must be between 1 and %d'
        for var_name, var_value in zip(elements_names, elements):
            assert 1 <= var_value <= self.dimension, error_message % (var_name, self.dimension)

    def _validate_range(self, from_elems, to_elems, from_elems_names, to_elems_names):
        """
         Validates that input ranges are correct (from <= to)
        """
        error_message = 'Invalid range: %s <= %s not satisfied'

        for from_, to_, from_name, to_name in zip(from_elems, to_elems, from_elems_names, to_elems_names):
            assert from_ <= to_, error_message % (from_name, to_name)

    def _validate_integers(self, elements, elements_names):
        """
        Validates that a series of elements are integers.
        """
        error_message = '%s must be instance of int'

        for var_name, var_value in zip(elements_names, elements):
            assert isinstance(var_value, int), error_message % var_name
