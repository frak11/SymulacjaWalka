import random

def generuj_mape(grid_size, spawn_rate):

    grid = [["X" for _ in range(grid_size)] for _ in range(grid_size)]
    for i in range(grid_size):
        for j in range(grid_size):
            chance = random.random()
            if chance < 0.045 * spawn_rate:
                grid[i][j] = "D"
            elif chance < 0.07 * spawn_rate:
                grid[i][j] = "K"
            elif chance < 0.085 * spawn_rate:
                grid[i][j] = "Z"
            elif chance < 0.1 * spawn_rate:
                grid[i][j] = "J"
    return grid
