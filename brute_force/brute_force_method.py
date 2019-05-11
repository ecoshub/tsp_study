import itertools
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


def minumum_permutation_calculation(points, distance_matrix):
    # creating and trying all posible permutations for finding shortest route.
    len_points = len(points)
    # creating a list of index.
    index = [each for each in range(len_points)]
    # generating permutation.
    permutations = itertools.permutations(index, len_points)
    # first (n-1)! permutations is circular permutations.
    # there is repetitive circular permutations in first (n-1)! permutations.
    # but they are inseparable because of the structure of itertool.permutation.
    number_of_permutation = int(math.factorial(len_points - 1))
    current_sum = 0
    minimum_distance = float('inf')
    minimum_permutation = []
    # iteration of all possible circular permutation.
    for _ in range(number_of_permutation):
        current_permutation = next(permutations)
        for i in range(len_points):
            # if "i" is equal to last index, last move has to be between first and last points.
            if i == len_points - 1:
                current_distance = distance_matrix[current_permutation[i]][current_permutation[0]]
            # if "i" is not equal to last index, the move has to be between first and next point.
            else:
                current_distance = distance_matrix[current_permutation[i]][current_permutation[i + 1]]
            # summing up all moves for total route distance.
            current_sum += current_distance
        # total distance comparison for finding shortest route.
        if current_sum < minimum_distance:
            minimum_distance = current_sum
            minimum_permutation = current_permutation
        current_sum = 0
    return minimum_distance, minimum_permutation


def draw_minimum_distance(points, space_size, minimum_distance, minimum_permutation):
    # drawing plot for visualising points and route.
    len_points = len(points)
    # setting plotting environment.
    sns.set(style='darkgrid')
    plt.xlim(-1, space_size + 1)
    plt.ylim(-1, space_size + 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('minimum distance: {}'.format(minimum_distance))
    for i in range(len_points - 1):
        # plotting point.
        plt.plot(points[i][0], points[i][1], 'go')
        # drawing line between points.
        if i == len_points - 1:
            # connetting first point to last.
            last_to_first_x = [points[minimum_permutation[i]][0], points[minimum_permutation[0]][0]]
            last_to_first_y = [points[minimum_permutation[i]][1], points[minimum_permutation[0]][1]]
            plt.plot(last_to_first_x, last_to_first_y)
            plt.text(points[minimum_permutation[i]][0], points[minimum_permutation[i]][1], minimum_permutation[i])
        else:
            # connetting point with next point.
            last_to_first_x = [points[minimum_permutation[i]][0], points[minimum_permutation[i + 1]][0]]
            last_to_first_y = [points[minimum_permutation[i]][1], points[minimum_permutation[i + 1]][1]]
            plt.plot(last_to_first_x, last_to_first_y)
            plt.text(points[minimum_permutation[i]][0], points[minimum_permutation[i]][1], minimum_permutation[i])
    plt.show()


def brute_force_method(num_point, space_size, seed, plot=False):
    # master function for this method.
    # creating points.
    points = create_points(num_point, space_size, seed)
    # creating distance matrix.
    distance_matrix = create_distance_matrix(points)
    # finding shortest route and total distance of this route.
    minimum_distance, minimum_permutation = minumum_permutation_calculation(points, distance_matrix)
    if plot:
        # plotting points and shortest route.
        draw_minimum_distance(points, space_size, minimum_distance, minimum_permutation)
    return minimum_distance


# EXAMPLE USAGE
# number_of_points = 10
# space_size = 100
# seed = 1

# brute_force_method(number_of_points, space_size, seed, True)
