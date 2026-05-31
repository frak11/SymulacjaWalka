import random

def generuj_mape(gridSize, spawnRate, seed):
    random.seed(seed)

    grid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]
    for i in range(gridSize):
        for j in range(gridSize):
            chance = random.random()
            if chance <= 0.05 * spawnRate:
                 grid[i][j] = "D"
            if chance > 0.05 * spawnRate and chance <= 0.08 * spawnRate:
                grid[i][j] = "K"
            if chance > 0.08 * spawnRate and chance <= 0.1 * spawnRate:
                grid[i][j] = "Z"

    for i in range(gridSize):
        for j in range(gridSize):
            print(grid[i][j], end=" ")
        print()
    return grid
