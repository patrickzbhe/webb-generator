from app import App
from app import DEFAULT_FRAME_TIME
from app import distance

def test_distance():
    assert distance([1,2,3], [3,2,1]) == 2
    assert abs(distance([1,-5,3], [-300,2,12]) - 301.0813) < 0.005

def test_app_frames():
    app = App()
    app.new_frame()
    app.new_frame()
    app.new_frame()
    assert len(app.cubes) == 4
    assert app.cube_pointer == 3
    app.prev_frame()
    assert app.cube_pointer == 2
    app.next_frame()
    assert app.cube_pointer == 3
    app.next_frame()
    assert app.cube_pointer == 3
    app.delete_frame()
    app.delete_frame()
    app.delete_frame()
    app.delete_frame()
    assert app.cube_pointer == 0
    assert len(app.cubes) == 1


