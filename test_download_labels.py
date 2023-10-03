from download_labels import add_extra_point, remove_excess_points


def test_add_extra_point():
    triangle_polygon = [{"x": 0, "y":0}, {"x": 5, "y": 4}, {"x": 5, "y":0}, {"x": 0, "y":0}]
    expected_rect_polygon = [{"x": 0, "y":0}, {"x": 0, "y":4}, {"x": 5, "y": 4}, {"x": 5, "y":0}, {"x": 0, "y":0}]

    assert add_extra_point(triangle_polygon) == expected_rect_polygon

def test_add_extra_point_at_origin():
    triangle_polygon = [ {"x": 0, "y":4}, {"x": 5, "y": 4}, {"x": 5, "y":0},  {"x": 0, "y":4}]
    expected_rect_polygon = [ {"x": 0, "y":4}, {"x": 5, "y": 4}, {"x": 5, "y":0},{"x": 0, "y":0},  {"x": 0, "y":4}] #[{"x": 0, "y":0}, {"x": 0, "y":4}, {"x": 5, "y": 4}, {"x": 5, "y":0}, {"x": 0, "y":0}]

    assert add_extra_point(triangle_polygon) == expected_rect_polygon

def test_add_extra_point_tilted():
    triangle_polygon = [ {"x": 1, "y":0}, {"x": 5, "y": 1}, {"x": 4, "y":5}, {"x": 1, "y":0}] 
    expected_rect_polygon = [ {"x": 1, "y":0}, {"x": 5, "y": 1}, {"x": 4, "y":5},{"x": 0, "y":4},  {"x": 1, "y":0}] 

    assert add_extra_point(triangle_polygon) == expected_rect_polygon

def test_remove_excess_points():
    extra_point_polygon = [ {"x": 1, "y":0}, {"x": 5, "y": 1}, {"x": 4, "y":5}, {"x": 2, "y":5}, {"x": 0, "y":4},  {"x": 1, "y":0}] 
    expected_rect_polygon = [ {"x": 1, "y":0}, {"x": 5, "y": 1}, {"x": 4, "y":5},{"x": 0, "y":4}] 
    assert remove_excess_points(extra_point_polygon) == expected_rect_polygon

test_add_extra_point()