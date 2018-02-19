import numpy as np

def hasPathHelper(m, v, i, j):
	if i < 0 or j < 0 or j >= len(m) or i >= len(m) or v[i][j] >= 0:
		return False
    # Mark as visited
    # 0 means bad path
    # 1 means good path
	v[i][j] = 0
	if m[i][j] == 0:
		return False
	new_v_1 = list(v)
	new_v_2 = list(v)
	new_v_3 = list(v)
	new_v_4 = list(v)
	if j == len(m)-1 or hasPathHelper(m, new_v_1, i+1, j) or hasPathHelper(m, new_v_2, i-1, j) or hasPathHelper(m, new_v_3, i, j+1) or hasPathHelper(m, new_v_4, i, j-1):
		v[i][j] = 1

	return v[i][j] == 1

def hasPath(m, v):
	for i in range(len(m)): 
		if hasPathHelper(m,v,i,0):
			return True

	return False

if __name__ == "__main__":
	m = np.array([[1,0,0,0],[1,1,0,0],[1,1,1,0],[0,1,1,1]])
	v = np.full((4,4), -1)
	print("Has path?: " + str(hasPath(m, v)))
	#print(str(v)[1:-1])
	print(list(v)[:])


