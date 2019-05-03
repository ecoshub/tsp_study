import math
import matplotlib.pyplot as plt
import seaborn as sns
import random


def create_points(number_of_points, space_size, seed):
    # creating random points.

    # generating same random set for debug or work on it.
    random.seed(seed)
    # using space_size as universal set and getting random samples from it.
    x_coordinates = random.sample(range(space_size), number_of_points)
    y_coordinates = random.sample(range(space_size), number_of_points)
    # merging x coordinates y coordinates.
    points = list(zip(x_coordinates, y_coordinates))
    return points


def create_distance_matrix(points):
    # creating a matrix that holds all the distance informations.
    # calculating relative distance of all points with other points
    # so do not calculate same distance over and over again.
    # for example: distance between points[i] and points[j] is distance[i][j]

    # size of points set.
    len_points = len(points)
    # creating a null matrix.
    distances = [[0 for _ in range(len_points)] for _ in range(len_points)]
    for i in range(len_points):
        for j in range(len_points):
            # calculating distance between points
            distance = math.sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)
            distances[i][j] = distance
    return distances


def distance_calculation(first_point, second_point):
    # calculating Euclidean distance.
    delta_x = first_point[0] - second_point[0]
    delta_y = first_point[1] - second_point[1]
    euclidean = math.sqrt(delta_x ** 2 + delta_y ** 2)
    return euclidean


def find_corner_points_index(points):
    # for adding index value to points list making a new points list.
    sorted_array = []
    len_points = len(points)
    for i in range(len_points):
        # [x coordinate, y coordinate, index]
        sorted_array.append([points[i][0], points[i][1], i])
    # sort by x cordinate value
    sorted_array = sorted(sorted_array, key=lambda x: x[0])
    # sort by y cordinate value
    sorted_array = sorted(sorted_array, key=lambda x: x[1])
    # those sortes gave us left bottom corner point.
    index = sorted_array[0][2]
    return index


def find_center(points):
    sum_x_coordinate = 0
    sum_y_coordinate = 0
    for i, j in points:
        sum_x_coordinate += i
        sum_y_coordinate += j
    len_points = len(points)
    center_x = sum_x_coordinate / len_points
    center_y = sum_y_coordinate / len_points
    return center_x, center_y


def calculate_angle(main_point, other_point):
    # hard coding of special slopes
    if main_point[0] == other_point[0]:
        if main_point[1] > other_point[1]:
            angle = 270
            return angle
        elif main_point[1] < other_point[1]:
            angle = 90
            return angle
    if main_point[1] == other_point[1]:
        if main_point[0] > other_point[0]:
            angle = 180
            return angle
        elif main_point[0] < other_point[0]:
            angle = 0
            return angle
    # quadrant constants adding.
    if other_point[0] > main_point[0] and other_point[1] > main_point[1]:
        constant = 0
    elif other_point[0] < main_point[0] and other_point[1] > main_point[1]:
        constant = 180
    elif other_point[0] < main_point[0] and other_point[1] < main_point[1]:
        constant = 180
    elif other_point[0] > main_point[0] and other_point[1] < main_point[1]:
        constant = 360
    delta_x = main_point[0] - other_point[0]
    delta_y = main_point[1] - other_point[1]
    angle = math.atan(delta_y / delta_x)
    # radians to degrees
    angle = angle / 2 / math.pi * 360
    angle += constant
    return angle


def deviation_amount(first_point, second_point, other):
    # distance without deviation.
    base_distance = distance_calculation(first_point, second_point)
    # first deviations cost.
    first_deviation = distance_calculation(first_point, other)
    # second deviations cost.
    second_deviation = distance_calculation(second_point, other)
    # cost of deviation to other point.
    delta = first_deviation + second_deviation - base_distance
    return delta


def minimum_deviations(exterior_polygon, points, distance_matrix):
    len_wrap = len(exterior_polygon)
    len_points = len(points)
    all_deviations = []
    for i in range(len_points):
        min_delt = float('inf')
        main_mem = []
        for j in range(len_wrap):
            # looping sequential exterior polygon points.
            # calculating all deviation amounts of points except exterior polygons points.
            if j == len_wrap - 1:
                temp_delt = deviation_amount(exterior_polygon[j], exterior_polygon[0], points[i])
                temp_mem = [temp_delt, j, 0, i]
            else:
                temp_delt = deviation_amount(exterior_polygon[j], exterior_polygon[j + 1], points[i])
                temp_mem = [temp_delt, j, j + 1, i]
            # finding point that has minimum deviation amount.
            if temp_delt < min_delt:
                min_delt = temp_delt
                main_mem = temp_mem
        # appending minimum deviation point.
        all_deviations.append(main_mem)
    return all_deviations


def wrap_points(points):
    # wraping points, finding most exterior points.
    # starting with left bottom point.
    starting_index = find_corner_points_index(points)
    selected_index = starting_index
    selected = points[selected_index]
    # finding center point.
    center_x, center_y = find_center(points)
    center = [center_x, center_y]
    exterior_polygon = []
    # stop condition.
    stop = True
    while(stop):
        min_angle = float('inf')
        index = 0
        first_lines_angle = calculate_angle(selected, center) + 180
        for i in range(len(points)):
            # calculating all angle between index point and other points.
            if i != selected_index:
                second_lines_angle = calculate_angle(selected, points[i])
                delta_angle = (second_lines_angle - first_lines_angle) % 360
                # finding point that has minimum angle with index point.
                if delta_angle < min_angle:
                    min_angle = delta_angle
                    index = i
        # the found point storing as start point.
        selected_index = index
        selected = points[selected_index]
        # the found point appending as an exterior point.
        exterior_polygon.append(selected)
        # cyle ends when loop hits the start point again.
        if selected_index == starting_index:
            stop = False
    return exterior_polygon


def length_of_route(points):
    length = 0
    len_points = len(points)
    for i in range(len_points):
        if i == len(points) - 1:
            length += distance_calculation(points[i], points[0])
        else:
            length += distance_calculation(points[i], points[i + 1])
    return length


def draw_minimum_distance(points, space_size, minimum_distance, polygon):
    # drawing plot for visualising points and route.

    len_points = len(points)
    # setting plotting environment.
    sns.set(style='darkgrid')
    plt.xlim(-1, space_size + 1)
    plt.ylim(-1, space_size + 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('minimum distance: {}'.format(minimum_distance))
    for i in range(len_points):
        # plotting point.
        plt.plot(points[i][0], points[i][1], 'go')
        # drawing line between points.
        if i == len_points - 1:
            # connetting first point to last.
            last_to_first_x = polygon[i][0], polygon[0][0]
            last_to_first_y = polygon[i][1], polygon[0][1]
            plt.plot(last_to_first_x, last_to_first_y)
            plt.text(polygon[i][0], polygon[i][1], i)
        else:
            # connetting point with next point.
            last_to_first_x = polygon[i][0], polygon[i + 1][0]
            last_to_first_y = polygon[i][1], polygon[i + 1][1]
            plt.plot(last_to_first_x, last_to_first_y)
            plt.text(polygon[i][0], polygon[i][1], i)
    plt.show()


def wrap_method(num_point, space_size, seed, plot=False):
    # master function for this method.

    # creating points.
    points = create_points(num_point, space_size, seed)
    # creating distance matrix.
    distance_matrix = create_distance_matrix(points)
    # creating exterior polygon.
    exterior_polygon = wrap_points(points)
    new_points = []
    # eliminating exterior polygons points.
    for i in range(len(points)):
        if points[i] not in exterior_polygon:
            new_points.append(points[i])

    for _ in range(len(new_points)):
        # calculating minumum deviation list.
        min_dev = minimum_deviations(exterior_polygon, new_points, distance_matrix)
        # sorting minimum deviations biggest to smallest. for starting biggest deviation first.
        # also starting with minimum deviations lists minimum value is another method.
        # reverse = False , gaves another sub minimum solition.
        min_dev = sorted(min_dev, key=lambda x: x[0], reverse=True)
        max_dev = min_dev[0]
        # inserting new point to middle of two exterior points.
        exterior_polygon.insert(max_dev[2], new_points[max_dev[3]])
        new_points.pop(max_dev[3])
    # route total length.
    length = length_of_route(exterior_polygon)
    if plot:
        draw_minimum_distance(points, space_size, length, exterior_polygon)
    return length


# EXAMPLE USAGE
# num_point = 10
# space_size = 100
# seed = 1

# wrap_method(num_point, space_size, seed, True)
