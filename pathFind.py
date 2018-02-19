def search(grid, x, y, path):
	if grid[x][y] == 2:
		# Already found the goal
		path.append((x,y))
		return True
	elif grid[x][y] == 1:
		# This is the wall
		return False
	elif grid[x][y] == 3:
		return False

    # Mark as visited
	grid[x][y] = 3

	# Explore the neighbours
	if (x < len(grid)-1 and search(grid, x+1, y, path)) or (y > 0 and search(grid,x, y-1, path)) or (x > 0 and search(grid,x-1, y, path)) or (y < len(grid)-1 and search(grid,x, y+1, path)):
		path.append((x,y))
		return True

	return False



if __name__ == "__main__":
	'''
	path = []
	grid = [[1,1,1,1,1],
	        [1,1,1,1,1],
	        [1,1,0,0,0],
	        [1,1,1,0,0],
	        [1,1,2,0,0]]
	print('Has path? :' + str(search(grid, 2,2,path)))
	#print(grid[:])
	print(path)
	'''
	indices = 0,2 
	a = [5,6,7,8]
	a = [i for j, i in enumerate(a) if j not in indices]
	print(a)
	print(type(indices))