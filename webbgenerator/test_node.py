from node import Node


def test_node_init():
    node = Node(1, 2, 3, 1, 1)
    assert node.xyz == [1, 2, 3]


def test_node_rotate():
    node = Node(1, 2, 3, 1, 1)
    node.rotate(60, 0)
    assert coords_within(node.xyz, [-1.23, 1.86, 3])
    node.rotate(220, 2)
    assert coords_within(node.xyz, [-1.23, 0.49, -3.49])
    node.rotate(820, 1)
    assert coords_within(node.xyz, [3.65, 0.49, -0.60])


def coords_within(coords1, coords2, delta=0.05):
    '''Checks if all ordered pairs of coordinates are within delta'''
    for c1, c2 in zip(coords1, coords2):
        if abs(c1 - c2) > delta:
            return False
    return True
