from cube import Cube

def test_cube_init():
    cube = Cube()
    assert len(cube.c_layers) == 4
    assert len(cube.points) == 64
    assert len(cube.edges) == 48

    cube2 = Cube(num_sides=5)
    assert len(cube2.c_layers) == 5
    assert len(cube2.points) == 125
    assert len(cube2.edges) == 75

def test_cube_generate_basic():
    cube = Cube()

    expected_basic = '''for x=1 to 125:
    portb = %00000000
    portd = %00000000
    portc = %00010000
    pause 1

    portb = %00000000
    portd = %00000000
    portc = %00100000
    pause 1

    portb = %00000000
    portd = %00000000
    portc = %01000000
    pause 1

    portb = %00000000
    portd = %00000000
    portc = %10000000
    pause 1

    next x
'''
    assert expected_basic == cube.generate_basic(500)
    cube.points[0].switch()
    cube.points[10].switch()
    cube.points[-1].switch()

    expected_basic2 = '''for x=1 to 125:
    portb = %00000000
    portd = %00000001
    portc = %00010000
    pause 1

    portb = %00000000
    portd = %00000000
    portc = %00100000
    pause 1

    portb = %00000001
    portd = %00000000
    portc = %01000000
    pause 1

    portb = %10000000
    portd = %00000000
    portc = %10000000
    pause 1

    next x
'''
    assert expected_basic2 == cube.generate_basic(500)