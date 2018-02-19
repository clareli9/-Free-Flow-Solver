def check_completed(grid, point_pair_list):
    # Set the initial points (start and end)
    init_point_list = []
    for source, dest in point_pair_list:
        init_point_list.append(source)
        init_point_list.append(dest)
    print(init_point_list)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (row, col) in init_point_list:
                if not check_completed_helper1(grid, row, col):
                    return False
            else:
                if not check_completed_helper2(grid, row, col):
                    return False

    return True

def check_completed_helper1(grid, x, y):
    check = 0
    if x >= 1 and grid[x][y] == grid[x-1][y]:
        print("hehe1 " + str(grid[x][y]))
        check = check + 1
    if x <= len(grid)-2 and grid[x][y] == grid[x+1][y]:
        print("hehe2 " + str(grid[x][y]))
        check = check + 1
    if y >= 1 and grid[x][y] == grid[x][y-1]:
        print("hehe3 " + str(grid[x][y]))
        check = check + 1
    if y <= len(grid[0])-2 and grid[x][y] == grid[x][y+1]:
        print("hehe4 " + str(grid[x][y]))
        check = check + 1
    print("method1: " +str(x) + str(y) + " " +str(check))
    return (check == 1)

def check_completed_helper2(grid,x,y):
    check = 0
    if x >= 1 and grid[x][y] == grid[x - 1][y]:
        print("haha1 " + str(grid[x][y]))
        check = check + 1
    if x <= len(grid) - 2 and grid[x][y] == grid[x + 1][y]:
        print("haha2 " + str(grid[x][y]))
        check = check + 1
    if y >= 1 and grid[x][y] == grid[x][y - 1]:
        print("haha3 " + str(grid[x][y]))
        check = check + 1
    if y <= len(grid[0]) - 2 and grid[x][y] == grid[x][y + 1]:
        print("haha4 " + str(grid[x][y]))
        check = check + 1
    print("method2: "+ str(x) + str(y) + " " + str(check))
    return (check >= 2)


if __name__ == "__main__":
    grid = [[0,1,1,2,2],
            [0,1,3,2,4],
            [0,1,3,2,4],
            [0,1,3,2,4],
            [0,0,3,4,4]]
    point_pair_list = [((0,0),(4,1)),((3,1),(0,2)),((1,2),(4,2)),((3,3),(0,4)),((4,3),(1,4))]
    print(check_completed(grid, point_pair_list))
