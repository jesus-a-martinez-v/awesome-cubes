from persistence.cube import *
from data.cube import Cube
from nose.tools import *


def teardown_func():
    delete_all()


@with_setup(teardown=teardown_func)
def test_store_cube():
    # Insert cube and get its id.
    cube = Cube(dimension=10)
    cube_id = store(cube)

    # Cube must be present.
    assert cube_id is not None, "cube_id is None"

    # Get all cubes. At this point, there should be only one: The one we just inserted.
    cubes = get_all()

    eq_(len(cubes), 1)
    raw_cube = cubes[0]

    # Check that the data is the same.
    eq_(raw_cube['dimension'], cube.dimension)
    eq_(raw_cube['_id'], cube_id)


@with_setup(teardown=teardown_func)
def test_list_cubes():
    # Insert a bunch of cubes.
    for i in range(10):
        cube = Cube(dimension=i + 1)
        store(cube)

    # Given we inserted 10 elements, then our query must throw us 10 elements back.
    cubes = get_all()
    eq_(len(cubes), 10)


@with_setup(teardown=teardown_func)
def test_get_single_cube():
    # Insert a cube.
    cube = Cube(dimension=10)
    cube_id = store(cube)

    # Retrieve it back.
    assert cube_id is not None, "cube_id is None"
    raw_cube = get(cube_id)
    assert raw_cube is not None, "Cube wasn't retrieved"
    eq_(raw_cube['_id'], cube_id)


@with_setup(teardown=teardown_func)
def test_update_cube():
    # Insert a new cube.
    cube = Cube(dimension=10)
    cube_id = store(cube)

    # At this point, its inner representation is empty ({})
    raw_cube = get(cube_id)
    eq_({}, raw_cube['cube'])

    # Put a 42 at (1,2,3)
    cube.update(1, 2, 3, 42)
    updated = update(cube_id, cube)

    # There must be a 42 at (1,2,3)
    eq_(updated, True)
    raw_cube = get(cube_id)
    eq_(42, raw_cube['cube']['1']['2']['3'])


@with_setup(teardown=teardown_func)
def test_delete_cube():
    # Insert a cube.
    cube = Cube(dimension=10)
    cube_id = store(cube)

    # Now delete it.
    removed = delete(cube_id)

    # There shouldn't exist anymore.
    eq_(removed, True)
    raw_cube = get(cube_id)
    eq_(None, raw_cube)


def test_delete_all_cubes():
    # Insert a bunch of cubes.
    for i in range(10):
        cube = Cube(dimension=i + 1)
        store(cube)

    # Now delete them all. Exactly 10 cubes have been removed.
    cubes_deleted = delete_all()
    eq_(cubes_deleted, 10)

    # Now our collection is empty.
    cubes = get_all()
    eq_(len(cubes), 0)







