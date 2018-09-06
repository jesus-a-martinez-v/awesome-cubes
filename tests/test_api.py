from nose.tools import *
import json
from tests import test_app
from persistence.cube import *


# ===================
# Auxiliary functions
# ===================
def teardown_func():
    """
    Flushes database
    """
    delete_all()


def _check_status_code(response, status_code=200):
    """
    Checks that a given response has a specific status code.
    """
    eq_(response.status_code, status_code)


def _check_content_type(response, content_type='application/json'):
    """
    Checks that a given response has a specific content type
    """
    eq_(response.headers['Content-Type'], content_type)


def _decode_response(response):
    """
    Takes a response object and returns its payload JSON representation
    """
    return json.loads(response.data.decode('utf8'))


@with_setup(teardown=teardown_func)
def test_create_cube():
    """
    Tests cube creation through API
    """
    request_body = {'dimension': 10}
    response = test_app.post('/cubes', data=json.dumps(request_body), content_type='application/json')

    # Check status code and content type
    _check_content_type(response)
    _check_status_code(response)

    # Check returned id
    payload = _decode_response(response)
    data = payload['data']
    assert '_id' in data and data['_id']

    # Check object was actually created
    cube = get(data['_id'])
    assert cube is not None


@with_setup(teardown=teardown_func())
def test_update_cube():
    """
    Tests cube update through API
    """
    # Create cube directly

    cube_id = store(Cube(dimension=4))

    cube = get(cube_id)
    assert cube
    eq_(cube['cube'], {})

    request_body = {'x': 1, 'y': 2, 'z': 3, 'value': 42}
    # Update cube
    response = test_app.put('/cubes/%s' % cube_id, data=json.dumps(request_body), content_type='application/json')

    # Check status code and content type
    _check_content_type(response)
    _check_status_code(response)

    # Check if was actually updated
    cube = get(cube_id)
    eq_(cube['cube']['1']['2']['3'], 42)


@with_setup(teardown=teardown_func)
def test_list_all_cubes():
    """
    Tests cube indexing through API
    """
    # Insert a bunch of cubes

    cubes_ids = set()
    for i in range(10):
        cubes_ids.add(store(Cube(dimension=i + 1)))

    # Now list all cubes
    response = test_app.get('/cubes')

    # Check content type and status code.
    _check_content_type(response)
    _check_status_code(response)

    # Extract list of cubes.
    data = _decode_response(response)['data']
    eq_(len(data), 10)  # We inserted 10. We expect 10.
    eq_(cubes_ids, set([c['_id'] for c in data]))  # Ids must match.


@with_setup(teardown=teardown_func)
def test_get_cube():
    """
    Tests cube retrieval through API
    """
    # Store cube
    cube_id = store(Cube(4))

    # Get it back
    response = test_app.get('/cubes/%s' % cube_id)
    _check_status_code(response)
    _check_content_type(response)

    data = _decode_response(response)['data']

    # Must be expected cube
    eq_(data['_id'], cube_id)
    assert 'params' not in data and 'result' not in data


@with_setup(teardown=teardown_func)
def test_query_cube():
    """
    Tests cube querying through API
    """
    # Create cube
    cube = Cube(4)
    cube.update(2, 2, 2, 4)
    cube_id = store(cube)

    response = test_app.get('/cubes/%s?x1=1&y1=1&x2=3&y2=3' % cube_id)

    _check_status_code(response)
    _check_content_type(response)

    data = _decode_response(response)['data']

    # Cube retrieved is the one we asked for
    eq_(data['_id'], cube_id)
    parameters = data['params']

    # Check parameters used to perform the summations match params passed as input and defaults
    eq_(parameters['x1'], 1)
    eq_(parameters['y1'], 1)
    eq_(parameters['z1'], 1)
    eq_(parameters['x2'], 3)
    eq_(parameters['y2'], 3)
    eq_(parameters['z2'], 4)
    eq_(data['result'], 4)


def test_delete_one():
    """
    Tests cube deletion through API
    """
    # Insert cube
    cube_id = store(Cube(5))

    # Must get cube back
    cube = get(cube_id)
    assert cube

    # Now delete cube
    response = test_app.delete('/cubes/%s' % cube_id)
    _check_status_code(response)
    _check_content_type(response)

    # null result because cube doesn't exist anymore.
    cube = get(cube_id)
    eq_(cube, None)


def test_delete_all():
    """
    Tests cube deletion through API
    """
    # Insert some cubes
    for i in range(10):
        store(Cube(dimension=i + 1))

    # Inserted ten, so must retrieve 10
    cubes = get_all()
    eq_(len(cubes), 10)

    # Delete them all
    response = test_app.delete('/cubes')
    _check_content_type(response)
    _check_status_code(response)

    # Collection must be empty
    cubes = get_all()
    eq_(len(cubes), 0)

    
