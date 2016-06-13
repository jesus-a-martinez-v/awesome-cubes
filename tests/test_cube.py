import os
from data.cube import Cube


def test_cube():
    """
    Tests the update and query behaviors of the cube.
    """
    parent_dir = os.path.dirname(os.path.abspath(__file__))

    # Names of the files used to perform the test
    input_filename = "%s/test_cube_input" % parent_dir
    output_filename = "%s/test_cube_output" % parent_dir
    expected_output_filename = "%s/test_cube_expected_output" % parent_dir

    out = open(output_filename, "w")
    with open(input_filename, "r") as in_data:
        TESTS = None
        cube_dimension = None
        remaining_tests = None
        cube = None
        output_lines = []
        for line in in_data:
            if not TESTS:
                TESTS = int(line)
                continue

            if not cube_dimension or not remaining_tests:
                cube_dimension, remaining_tests = line.split(" ")
                cube_dimension = int(cube_dimension)
                remaining_tests = int(remaining_tests)

                cube = Cube(dimension=cube_dimension)
                continue

            if remaining_tests > 0:
                remaining_tests -= 1
                input = line.split(" ")

                if input[0] == "UPDATE":
                    x = int(input[1])
                    y = int(input[2])
                    z = int(input[3])
                    value = int(input[4])
                    cube.update(x, y, z, value)
                else:
                    x1 = int(input[1])
                    y1 = int(input[2])
                    z1 = int(input[3])
                    x2 = int(input[4])
                    y2 = int(input[5])
                    z2 = int(input[6])
                    output_lines.append("%d" % cube.query(x1, x2, y1, y2, z1, z2))

        out.write("\n".join(output_lines))
    out.flush()
    out.close()

    assert os.path.getsize(expected_output_filename) == os.path.getsize(output_filename), "File sizes don't match"

    out = open(output_filename, "r")
    expected_out = open(expected_output_filename, "r")
    assert expected_out.read() == out.read(), "Output doesn't match"

    # Flush and close.
    expected_out.flush()
    expected_out.close()

