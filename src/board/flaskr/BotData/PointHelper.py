def add_points(point_a: [int, int], point_b: [int, int]) -> [int, int]:
    return [point_a[0] + point_b[0], point_a[1] + point_b[1]]


def sub_points(point_a: [int, int], point_b: [int, int]) -> [int, int]:
    return add_points(point_a, [point_b[0] * -1, point_b[1] * -1])


def mult_point(point_a: [int, int], factor) -> [int, int]:
    return [point_a[0] * factor, point_a[1] * factor]


def point_in_area(point: [int, int], area: [[int, int], [int, int]]) -> bool:
    return area[0][0] < point[0] < area[1][0] and area[0][1] < point[1] < area[1][1]
