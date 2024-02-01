## By Emils Valdmanis 2024
## some additions by VS

def find_minimum_energy(grid):
  num_rows = len(grid)
  num_cols = len(grid[0])

  # Create a 2D array to store the minimum energy expenditure for each cell
  min_energy_dp = [[0] * num_cols for _ in range(num_rows)]

  # create 2D array to store move to get to each cell
  moves_dp = [[(None,None)] * num_cols for _ in range(num_rows)]

  # Initialize the first cell
  min_energy_dp[0][0] = grid[0][0]

  # initiatize first cell actually we do not need to do this because we already did it above
  moves_dp[0][0] = (None,None)

  # Calculate the energy expenditure when coming from the left for the first row
  for j in range(1, num_cols):
    min_energy_dp[0][j] = min_energy_dp[0][j - 1] + grid[0][j]
    # add move to moves_dp
    moves_dp[0][j] = (0,j-1) # we had to come from the left so we have no choice in moves

  # Calculate energy expenditure for each spot in the first column when coming from the top
  for i in range(1, num_rows):
    min_energy_dp[i][0] = min_energy_dp[i - 1][0] + grid[i][0]
    # add move to moves_dp
    moves_dp[i][0] = (i-1,0) # again we have no choice in moves we just have to have come from the upper neighbor

  # Calculate the best option for each location based on whether it's better to move from the left or the top
  for i in range(1, num_rows):
    for j in range(1, num_cols):
      min_energy_dp[i][j] = min(min_energy_dp[i - 1][j], min_energy_dp[i][j - 1]) + grid[i][j]
      # add move to moves_dp
      if min_energy_dp[i - 1][j] < min_energy_dp[i][j - 1]:
        moves_dp[i][j] = (i-1,j)
      else: # so if moves equal we will choose to come from the left
        moves_dp[i][j] = (i,j-1)

  # After calculating each value to be the minimum, the bottom right will have the sum of the best path, which is our answer
  
  # let's return the path as well
  path = []
  i = num_rows-1
  j = num_cols-1
  path.append((i,j))
  while i is not None or j is not None: # in this case it does not matter because only first square has None
    # TODO see what happens if we change from or to and
    i,j = moves_dp[i][j] # we utilize tuple unpacking to get the coordinates of the previous square
    path.append((i,j))
  path.reverse() # this is IN PLACE modifies the original list
  
  return min_energy_dp[num_rows - 1][num_cols - 1], path

grids = [
  [
    [2, 1],
    [3, 4]
  ],
  [
    [5, 2, 1],
    [8, 3, 4],
    [7, 6, 9]
  ],
  [
    [1, 1, 3],
    [4, 2, 1],
    [3, 1, 1]
  ],
  # 3x5 grid
  [
    [1, 2, 8, 4, 5],
    [2, 7, 4, 5, 1],
    [3, 4, 5, 2, 2]
  ],
  # lets do 4 x 6 grid
  [
    [100, 200, 999, 999, 999, 999],
    [100, 100, 999, 999, 999, 999],
    [999, 100, 100, 999, 999, 999],
    [999, 999, 100, 100, 100, 100]
  ],
]

for i, grid in enumerate(grids):
  result = find_minimum_energy(grid)
  print(f"Grid {i} - Minimum Energy Expenditure: {result}")
