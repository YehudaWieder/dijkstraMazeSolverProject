from colorsys import rgb_to_hls

import cv2
import heapq


def block_img(point_1, point_2):
    cv2.line(img_maze, point_1, point_2, (0, 0, 0), thickness=2)


def get_neighbors(img_maze, current):
    width, height, _ = img_maze.shape
    x, y = current
    neighbors = []
    neighbors_index = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    for i, j in neighbors_index:
        n_x, n_y = x + i, y + j
        if 0 <= n_x < width and 0 <= n_y < height and all(img_maze[n_x][n_y] > 200):
            neighbors.append((n_x, n_y))
    return neighbors


def get_distance(current, neighbor):
    x_1, y_1 = current
    x_2, y_2 = neighbor
    return ((x_1 - x_2) ** 2) + ((y_1 - y_2) ** 2) ** 0.5


def get_path(end_pixel, parents):
    path = []
    current = end_pixel
    while current:
        path.append(current)
        current = parents[current]
    return path[::-1]


def dijkstra(img_maze, start_pixel, end_pixel):
    visited = set()
    distance = {start_pixel: 0}
    parent = {start_pixel: None}
    priority_q = [(0, start_pixel)]
    current = start_pixel

    while current != end_pixel:
        visited.add(current)
        neighbors = get_neighbors(img_maze, current)
        for neighbor in neighbors:
            neighbor_distance = get_distance(current, neighbor)
            new_neighbor_distance = distance[current] + neighbor_distance
            if neighbor not in distance or distance[neighbor] > new_neighbor_distance:
                distance[neighbor] = new_neighbor_distance
                heapq.heappush(priority_q, (distance[neighbor], neighbor))
                parent[neighbor] = current
        while current in visited:
            _, current = heapq.heappop(priority_q)
    return get_path(end_pixel, parent), visited


def draw_path(img_maze, path):
    y_1, x_1 = path[0]
    for y_2, x_2 in path[1:]:
        cv2.line(img_maze, (x_1, y_1), (x_2, y_2), (0, 0, 255), 3)
        x_1, y_1 = x_2, y_2


def draw_visited(img_maze, visited):
    for x, y in visited:
        img_maze[x][y] = 0, 255, 255


maze_1 = "maze_1.jpg"
maze_2 = "maze_2.jpg"

is_maze_1 = True
if is_maze_1:
    img_maze = cv2.imread(maze_1)
    start_pixel = 785, 557
    end_pixel = 1295, 656
else:
    img_maze = cv2.imread(maze_2)
    start_pixel = 282, 329
    end_pixel = 1277, 785
    point_1 = 340, 275
    point_2 = 322, 284
    block_img(point_1, point_2)

path, visited = dijkstra(img_maze, start_pixel, end_pixel)
print("maze solved. saving...")

draw_visited(img_maze, visited)
draw_path(img_maze, path)

if is_maze_1:
    cv2.imwrite("solve_maze_1.jpg", img_maze)
else:
    cv2.imwrite("solve_maze_2.jpg", img_maze)
