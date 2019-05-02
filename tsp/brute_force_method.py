import itertools
import math
import matplotlib.pyplot as plt
import seaborn as sns
import random


# creating random points
def create_points(number_of_points, space_size, seed):
    # using random seed for generating same random set for debug or work on it.
    random.seed(seed)
    # using universal set as space_size and getting random samples from it.
    x_es = random.sample(range(space_size), number_of_points)
    y_s = random.sample(range(space_size), number_of_points)
    # merging x set and y set
    points = list(zip(x_es, y_s))
    return points



''' calculating a matrix that holds all the distance informations point to point.
so do not repeat it self to mesure same distance over and over again.'''
def create_distance_matrix(points):
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

# trying all posible permutations.


def minumum_permutation_calculation(points, distance_matrix):
    len_points = len(points)
    index = [each for each in range(len_points)]
    permutations = itertools.permutations(index, len_points)
    number_of_permutation = int(math.factorial(len_points - 1))
    current_sum = 0
    minimum_distance = float('inf')
    minimum_permutation = []
    for _ in range(number_of_permutation):
        current_permutation = next(permutations)
        current_permutation = list(current_permutation)
        current_permutation.append(current_permutation[0])
        for i in range(len_points):
            if i == len_points - 1:
                current_distance = distance_matrix[current_permutation[i]][current_permutation[0]]
            else:
                current_distance = distance_matrix[current_permutation[i]][current_permutation[i + 1]]
            current_sum += current_distance
        if current_sum < minimum_distance:
            minimum_distance = current_sum
            minimum_permutation = current_permutation
        current_sum = 0
    return minimum_distance, minimum_permutation


def draw_minimum_distance(points, space_size, minimum_distance, minimum_permutation):
    len_per = len(minimum_permutation)
    sns.set(style='darkgrid')
    plt.xlim(-1, space_size + 1)
    plt.ylim(-1, space_size + 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('minimum distance: {}'.format(minimum_distance))
    for i in range(len_per - 1):
        plt.plot(points[i][0], points[i][1], 'go')
        if i == len_per - 1:
            plt.plot([points[minimum_permutation[i]][0], points[minimum_permutation[0]][0]], [points[minimum_permutation[i]][1], points[minimum_permutation[0]][1]])
            plt.text(points[minimum_permutation[i]][0], points[minimum_permutation[i]][1], minimum_permutation[i])
        else:
            plt.plot([points[minimum_permutation[i]][0], points[minimum_permutation[i + 1]][0]], [points[minimum_permutation[i]][1], points[minimum_permutation[i + 1]][1]])
            plt.text(points[minimum_permutation[i]][0], points[minimum_permutation[i]][1], minimum_permutation[i])
    plt.show()


def brute_force_method(num_point, space_size, seed, plot=False):
    points = create_points(num_point, space_size, seed)
    distance_matrix = create_distance_matrix(points)
    minimum_distance, minimum_permutation = minumum_permutation_calculation(points, distance_matrix)
    if plot:
        draw_minimum_distance(points, space_size, minimum_distance, minimum_permutation)
    return minimum_distance


number_of_points = 10
space_size = 100
seed = 1

brute_force_method(number_of_points, space_size, seed, True)
