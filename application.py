"""
RESTful API methods.
"""

from flask import Flask, request, make_response, jsonify
from data.cube import Cube, instantiate_from_raw_data
from persistence.cube import delete, delete_all, get, get_all, store, update

app = Flask(__name__)

# Status codes constants
_SUCCESS = 200
_BAD_REQUEST = 400
_NOT_FOUND = 404
_INTERNAL_SERVER_ERROR = 500


@app.route('/cubes', methods=['POST'])
def create_cube():
    """
    Creates a new cube of the dimension provided in the input.
    :return: JSON response with the id of the cube just created.
    """
    try:
        request_body = request.json  # Extract body.

        # Validate body structure.
        if 'dimension' not in request_body:
            return make_response(jsonify(message='Bad Request. "dimension" field not provided'), _BAD_REQUEST)

        # Persist cube.
        cube = Cube(dimension=request_body['dimension'])
        cube_id = store(cube)

        return make_response(jsonify(message='Cube created successfully', data=cube_id), _SUCCESS)
    except Exception as e:
        return make_response(jsonify(message='Internal Server Error. Details: %s' % e), _INTERNAL_SERVER_ERROR)


@app.route('/cubes/<cube_id>', methods=['PUT'])
def update_cube(cube_id):
    """
    Updates a particular element of a cube.
    :param cube_id: Identifier of the cube to be updated.
    :return: JSON with a message with the operation status.
    """
    try:
        request_body = request.json

        # Checks that the body is properly constructed.
        if set(request_body.keys()) != {'x', 'y', 'z', 'value'}:
            return make_response(jsonify(message='Bad Request. Check x, y, z, and value fields are present'), _BAD_REQUEST)

        raw_cube = get(cube_id)  # Get raw cube representation.
        cube = instantiate_from_raw_data(raw_cube)  # Create new object from raw data
        cube.update(request_body['x'], request_body['y'], request_body['z'], request_body['value'])  # Perform update.

        successfully_updated = update(cube_id, cube)

        if not successfully_updated:
            return make_response(jsonify(message='Could not update cube with id %s' % cube_id), _INTERNAL_SERVER_ERROR)

        return make_response(jsonify(message='Cube successfully updated.'), _SUCCESS)
    except Exception as e:
        return make_response(jsonify(message='Internal Server Error. Details: %s' % e), _INTERNAL_SERVER_ERROR)


@app.route('/cubes', methods=['GET'])
def list_cubes():
    """
    Retrieves all cubes stored.
    :return: List of cubes.
    """
    cubes = get_all()
    return make_response(jsonify(data=cubes, message='Cubes retrieved successfully.'), _SUCCESS)


@app.route('/cubes/<cube_id>', methods=['GET'])
def detail_cube(cube_id):
    """
    Gets the details of a cube. This is:
        - If not range query parameter is provided (x1, x2, y1, y2, z1 or z2) then just returns the raw cube.
        - If there's at least query parameter, then it performs a summation over the cube, using the params passed
        as input, and defaulting to 1 in the case of the lower limits, and to N in the case of the upper bounds (where N
        is the cube dimension).
    :param cube_id: Identifier of the cube to be retrieved.
    :return: JSON with the cube details.
    """
    try:
        # Extract query parameters
        query_params = request.args
        x1 = query_params.get('x1')
        x2 = query_params.get('x2')
        y1 = query_params.get('y1')
        y2 = query_params.get('y2')
        z1 = query_params.get('z1')
        z2 = query_params.get('z2')

        # Get cube
        raw_cube = get(cube_id)

        # If cube is None, then nothing was found.
        if not raw_cube:
            return make_response(jsonify(message='Not found cube with id %s' % cube_id), _NOT_FOUND)

        response = raw_cube

        # If there's at least one parameter, then we must query the cube before returning it
        if any([x1, x2, y1, y2, z1, z2]):
            cube = instantiate_from_raw_data(raw_cube)  # Create cube

            # Put initial and final range values in a list so we can add defaults more easily.
            from_ = [x1, y1, z1]
            to_ = [x2, y2, z2]

            # This loop adds defaults and cast to int already present values
            for i in range(3):  # It's a cube, so we're pretty sure there will always be three dimensions to check.
                if not from_[i]:
                    from_[i] = 1
                else:
                    from_[i] = int(from_[i])

                if not to_[i]:
                    to_[i] = cube.dimension
                else:
                    to_[i] = int(to_[i])

            # Unpack range values again into their respective variables.
            x1, y1, z1 = from_
            x2, y2, z2 = to_

            cube_summation = cube.query(x1, x2, y1, y2, z1, z2)

            # Complement the response with the parameters and summation result
            response['params'] = {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'z1': z1, 'z2': z2}
            response['result'] = cube_summation

        return make_response(jsonify(message='Cube retrieved successfully', data=response), _SUCCESS)
    except Exception as e:
        return make_response(jsonify(message='Internal Server Error. Details: %s' % e), _INTERNAL_SERVER_ERROR)


@app.route('/cubes', methods=['DELETE'])
def delete_all_cubes():
    """
    Deletes all cubes.
    :return: JSON with a message notifying the number of cubes removed.
    """
    elements_removed = delete_all()

    return make_response(jsonify(message='%d cubes were removed.' % elements_removed), _SUCCESS)


@app.route('/cubes/<cube_id>', methods=['DELETE'])
def delete_cube(cube_id):
    """
    Deletes a particular cube.
    :param cube_id: Identifier of the cube to be deleted.
    :return: JSON with message related to the operation status.
    """
    try:
        successfully_removed = delete(cube_id)

        if not successfully_removed:
            return make_response(jsonify(message='Could not remove cube with id %s' % cube_id),
                                 _INTERNAL_SERVER_ERROR)

        return make_response(jsonify(message='Cube successfully removed'), _SUCCESS)
    except Exception as e:
        return make_response(jsonify(message='Internal Server Error. Details %s' % e), _INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
    from config.config import server_conf

    # If you want to change these configurations, head to /config/server.json
    app.run(host=server_conf['host'], port=server_conf['port'])
