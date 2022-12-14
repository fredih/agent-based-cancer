import numpy as np
import matplotlib.pyplot as plt
#import random

# Returns an array with 1 in the region that contains the N centre-most grid points and 0 on the others
def find_quasi_circle(N, grid_width, grid_height):
    '''
    Returns the coordinate of the centre-most points and also an
    array with 1 in that region and 0 on the rest
    '''

    current_grid = np.zeros((grid_height, grid_width))
    less_than_ideal_radius = np.sqrt(N/np.pi) / 1.2   
    n_cells_current = 0

    # Center of the grid in 0 based indexing
    a = grid_width/2 - 0.5
    b = grid_height/2 - 0.5

    # Increases the radius of the circle until if finds the correct size
    for radius in np.arange(less_than_ideal_radius, (min(grid_width, grid_height)/2), 0.1):
        last_grid = current_grid.copy()
        n_cells_last = n_cells_current

        # fill the circle
        for x in range(grid_width):
            for y in range(grid_height):
                if (x-a)**2 + (y-b)**2 < radius**2:
                    current_grid[x,y] = 1

        n_cells_current = np.count_nonzero(current_grid == 1)

        if n_cells_current >= N:

            if n_cells_current == N:
                last_grid = current_grid

            if n_cells_current > N:
                n_cells_to_add = N - n_cells_last
                circle_border = np.ma.masked_where(last_grid == 1, current_grid)

                # Fill the outer cells in a diametrically opposit counter-clocksise way
                outer_p = np.where(circle_border == 1)
                coords_outer_p = list(zip(outer_p[0], outer_p[1]))
                sign = 1
                for i in range(n_cells_to_add):
                    coord_to_add = coords_outer_p[i*sign]
                    last_grid[coord_to_add] = 1
                    sign *= -1

            # Create a list with possible places
            possible_places = np.where(last_grid == 1)
            coords = [list(tup) for tup in zip(possible_places[0], possible_places[1], (0 for i in possible_places[0]))]
            return last_grid, coords
        
        

# A test to see a 2D colormap of a given number of cells in the 201x201 grid
# width = 201
# height = 201
# resulting_quasi_circle = find_quasi_circle(97, width, height)[0]
# plt.imshow(resulting_quasi_circle, interpolation='none')
# plt.show()



# width = 10
# height = 10
# num_agents = 6
# array = find_quasi_circle(num_agents, width, height)[0]
# pos_coords = find_quasi_circle(num_agents, width, height)[1]
# print(array)
# print(pos_coords)




'''
To see how the vessel creatin is working

not_possible_places = pos_coords


not_possible_grid = array
# remove 2 cell border of the grid
not_possible_grid[:2,:] = 1
not_possible_grid[-2:,:] = 1
not_possible_grid[:,:2] = 1
not_possible_grid[:,-2:] = 1
possible_places = np.where(not_possible_grid == 0)
pos_coords = [list(tup) for tup in zip(possible_places[0], possible_places[1])]

print("possible coords: \n", pos_coords)

print(not_possible_grid)

numCellsToPlace = 7
numIter = 0
temp = numCellsToPlace
while temp > 0:
    numIter += 1
    cell_to_place = [random.randrange(width), random.randrange(height)]
    
    if cell_to_place in pos_coords:
        not_possible_grid[cell_to_place[0], cell_to_place[1]] = 1
        pos_coords.remove(cell_to_place)
        temp -= 1
print(f'temp: {temp} e numCellsToPlace: {numCellsToPlace}')


print("possible coords: \n", pos_coords)
print('numIter', numIter)
print(not_possible_grid)
'''