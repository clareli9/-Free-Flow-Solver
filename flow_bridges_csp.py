from cspbase import *
import itertools
import numpy as np

SOURCE = 1
DEST = 2
OBSTACLE = 3
VISITED = 4

global path_map
path_map = dict()


remained_path = list()

def flow_bridges_csp_model_1(initial_flow_board, poped):
    flow_csp = CSP('flow bridge CSP for model1')
    point_pair_list = initial_flow_board[0]
    grid_size = initial_flow_board[1]
    remained_point_pair = initial_flow_board[0][poped]
    # Remove the ignored one
    point_pair_list.pop(poped)
    #point_pair_list.pop(3)
    num_vars = len(point_pair_list)
    num = 0

    grid = [[0 for row in range(grid_size)] for col in range(grid_size)]
    # Fill the point pairs into the grid
    for source, dest in point_pair_list:
        grid[source[0]][source[1]] = SOURCE
        grid[dest[0]][dest[1]] = DEST

    # Encapsulate the path into Variable
    vars = [None for x in range(num_vars)]

    for i in range(len(vars)):
        paths = get_path_dom(point_pair_list[i])
        path_num = []
        for j in range(len(paths)):
            path_map[num] = paths[j]
            path_num.append(num)
            num = num + 1

        vars[i] = Variable('Pair ' + str(i), path_num)
        flow_csp.add_var(vars[i])

    # Set the constraints
    # No-collison constraint
    '''
    for i in range(len(vars)-1):
        for j in range(i+1, len(vars)):
            flow_csp.add_constraint(no_collision_constraint(vars[i], vars[j]))
    '''
    #for var in vars:
    for (var1, var2) in itertools.combinations(vars, 2):
        flow_csp.add_constraint(no_collision_constraint(path_map, var1, var2))

    # Remained path constraint
    flow_csp.add_constraint(remain_path_constraint(vars, remained_point_pair, grid_size, path_map))
    
    return flow_csp, vars


# A new model dealing with the 2 (or more )remained pairs

def flow_bridges_csp_model_2(initial_flow_board, popeds):
    flow_csp = CSP('flow bridge CSP for model2')
    point_pair_list = initial_flow_board[0]
    grid_size = initial_flow_board[1]
    original_num_vars = len(point_pair_list)
    remained_point_pair_list = []
    for poped in popeds:
        remained_point_pair_list.append(initial_flow_board[0][poped])

    # Pop out all points
    point_pair_list = [i for j, i in enumerate(point_pair_list) if j not in popeds]
    num_vars = len(point_pair_list)
    num = 0

    grid = [[0 for row in range(grid_size)] for col in range(grid_size)]
    # Fill the point pairs into the grid
    for source, dest in point_pair_list:
        grid[source[0]][source[1]] = SOURCE
        grid[dest[0]][dest[1]] = DEST

    # Encapsulate the Manhattan path into Variable
    vars = [None for x in range(original_num_vars)]
    all_domain = []
    for i in range(num_vars):
        paths = get_path_dom(point_pair_list[i])
        path_num = []
        for j in range(len(paths)):
            path_map[num] = paths[j]
            path_num.append(num)
            num = num + 1

        vars[i] = Variable('Pair ' + str(i), path_num)
        flow_csp.add_var(vars[i])
        all_domain.append(vars[i].cur_domain())

    # Then, encapsulate the remained paths into Variable

    for i in range(num_vars, original_num_vars):
        path_num = []
        for dom in itertools.product(*all_domain):
            obstacles = []
            for obs in dom:
                obstacles.append(path_map[obs])
            paths = get_path_dom_2(remained_point_pair_list[i-num_vars], obstacles, grid_size)
            for j in range(len(paths)):
                path_map[num] = paths[j]
                path_num.append(num)
                num = num + 1

        vars[i] = Variable('Pair ' + str(i), path_num)
        flow_csp.add_var(vars[i])

    # Set the no collision constraint
    for (var1, var2) in itertools.combinations(vars, 2):
        flow_csp.add_constraint(no_collision_constraint(path_map, var1, var2))

    return flow_csp, vars


def flow_bridges_csp_model_3(initial_flow_board):
    flow_csp = CSP('flow bridge csp for model3')
    point_pair_list = initial_flow_board[0]
    grid_size = initial_flow_board[1]
    grid_with_color = [[-1 for row in range(grid_size)] for col in range(grid_size)]
    vars = [[None for row in range(grid_size)] for col in range(grid_size)]

    # Fill the color into grid
    color = 0
    for source, dest in point_pair_list:
        grid_with_color[source[0]][source[1]] = color
        grid_with_color[dest[0]][dest[1]] = color
        color = color + 1

    print(grid_with_color)
    # Then, encapsulate all cells in grid into variables
    for row in range(grid_size):
        for col in range(grid_size):
            if grid_with_color[row][col] == -1:
                vars[row][col] = Variable('Cell' + str(row+1) + ',' + str(col+1), list(range(0, len(point_pair_list))))
            else:
                vars[row][col] = Variable('Cell' + str(row+1) + ',' + str(col+1), [grid_with_color[row][col]])
            flow_csp.add_var(vars[row][col])

    # Set the constraints (from the view of the whole)
    flow_csp.add_constraint(Board_constraint(vars, point_pair_list))
    return flow_csp, vars


def Board_constraint(vars, point_pair_list):
    const = Constraint('Board', vars)
    sat_turples = []
    all_domain = []
    for row in range(len(vars)):
        for col in range(len(vars[0])):
            all_domain.append(vars[row][col].cur_domain())


    for dom in itertools.product(*all_domain):
        idx = 0
        help_grid = [[-1 for row in range(len(vars))] for col in range(len(vars))]
        #print("aaaaaaaaa")
        for cell_color in dom:
            help_grid[int(int(idx)/int(len(vars)))][idx%(len(vars))] = cell_color
            idx =idx + 1
        print(help_grid)
        if check_completed(help_grid, point_pair_list):
            sat_turples.append(dom)

    const.add_satisfying_tuples(sat_turples)
    return const

def check_completed(grid, point_pair_list):
    # Set the initial points (start and end)
    init_point_list = []
    for source, dest in point_pair_list:
        init_point_list.append(source)
        init_point_list.append(dest)

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
        check = check + 1
    if x <= len(grid)-2 and grid[x][y] == grid[x+1][y]:
        check = check + 1
    if y >= 1 and grid[x][y] == grid[x][y-1]:
        check = check + 1
    if y <= len(grid[0])-2 and grid[x][y] == grid[x][y+1]:
        check = check + 1

    return (check == 1)

def check_completed_helper2(grid,x,y):
    check = 0
    if x >= 1 and grid[x][y] == grid[x - 1][y]:
        check = check + 1
    if x <= len(grid) - 2 and grid[x][y] == grid[x + 1][y]:
        check = check + 1
    if y >= 1 and grid[x][y] == grid[x][y - 1]:
        check = check + 1
    if y <= len(grid[0]) - 2 and grid[x][y] == grid[x][y + 1]:
        check = check + 1

    return (check >= 2)

# The constraints relevant to this csp

def no_collision_constraint(path_map, var1, var2):
    # var1, var2 here is two paths
    const = Constraint('No collision', (var1, var2))
    sat_turples = []
    for (val1, val2) in itertools.product(var1.cur_domain(), var2.cur_domain()):
        if not check_collision(path_map[val1], path_map[val2]):
            sat_turples.append((val1, val2))

    #print(sat_turples)
    const.add_satisfying_tuples(sat_turples)
    return const

# Helper functions
def check_collision(path1, path2):
    for point in path1:
        if point in path2:
            return True
    return False

# This constraint only works for one remained point pair
def remain_path_constraint(vars, remained_point_pair, grid_size, path_map):
    # remained_point_pair is like ((source_x, source_y), (dest_x, dest_y))
    const = Constraint("Remained path", vars)
    sat_turples = []
    all_domain = []
    # Create a mirrior board

    for var in vars:
        all_domain.append(var.cur_domain())
        # for row,col in var:
            # mirrior_grid[row][col] = 1

    for dom in itertools.product(*all_domain):
        global remained_path
        #remained_path = []
        mirrior_grid = [[0 for row in range(grid_size)] for col in range(grid_size)]
        # Fill the mirror board with already known obstacles
        for path in dom:
            for row,col in path_map[path]:
                mirrior_grid[int(row)][int(col)] = OBSTACLE

        # If source or dest already occupied by obstables, indeedly false
        if mirrior_grid[remained_point_pair[1][0]][remained_point_pair[1][1]] == OBSTACLE or mirrior_grid[remained_point_pair[0][0]][remained_point_pair[0][1]] == OBSTACLE:
            continue

        # Set the destination
        mirrior_grid[remained_point_pair[1][0]][remained_point_pair[1][1]] = DEST

        if hasPath(mirrior_grid, remained_path, remained_point_pair[0][0], remained_point_pair[0][1]):
            #print('We found remained path!!!!, the path is : ')
            #for path in dom:
                #print(path)
            sat_turples.append(dom)
        #else:
            #print('Did not find!!')

    const.add_satisfying_tuples(sat_turples)
    return const

def hasPath(grid, path, x, y):
    if grid[x][y] == DEST:
        # Find the goal!
        path.append((x,y))
        return True
    elif grid[x][y] == OBSTACLE:
        # Obstacles!
        return False
    elif grid[x][y] == VISITED:
        return False

    # Mark as visited
    grid[x][y] = VISITED
    # Explore the neighbours
    if (x < len(grid)-1 and hasPath(grid, path, x+1, y)) or (y > 0 and hasPath(grid,path,x, y-1)) or (x > 0 and hasPath(grid,path,x-1, y)) or (y < len(grid)-1 and hasPath(grid,path,x, y+1)):
        path.append((x, y))
        return True

    return False




# -------------- Get the path in model 1 --------------------

def get_path_dom(point_pair):
    dir_tp = (point_pair[1][0]-point_pair[0][0],point_pair[1][1]-point_pair[0][1])
    unit_dir_tp = [0,0]
    
    if dir_tp[0] == 0:
       unit_dir_tp[0] = 0
    else:
       unit_dir_tp[0] = dir_tp[0]/abs(dir_tp[0])
    if dir_tp[1] == 0:
       unit_dir_tp[1] = 0
    else:
       unit_dir_tp[1] = dir_tp[1]/abs(dir_tp[1])
    
    all_path = []
    path = []
    getpath(path,all_path,point_pair[0],point_pair[1],unit_dir_tp)
    '''
    for path_n in all_path:
        print("****************************A new path******************************")
        for pt in path_n:
            print(pt[0],pt[1])
    '''
    return all_path

def getpath(path,all_path,cur,goal, udir_tp):
    if (goal[0]-cur[0])*udir_tp[0]<0 or (goal[1]-cur[1])*udir_tp[1]<0:
       return
    path.append(cur)
    if cur[0] == goal[0] and cur[1] == goal[1]:
       all_path.append(path)
       return
    if udir_tp[0] != 0:
       new_path_1 = list(path)
       getpath(new_path_1,all_path,(cur[0]+udir_tp[0],cur[1]),goal,udir_tp)
    if udir_tp[1] != 0:
       new_path_2 = list(path)
       getpath(new_path_2,all_path,(cur[0],cur[1]+udir_tp[1]),goal,udir_tp)


# -------------- Get the path in model 2 --------------------
def get_path_dom_2(point_pair, path_tuple, n):
    obstacle_list = []
    for path in path_tuple:
        obstacle_list += path
    #print(obstacle_list)
    all_path = []
    path = []
    getpath_2(path,all_path,point_pair[0],point_pair[1],obstacle_list, n)
    '''
    for path_n in all_path:
        print("****************************A new path******************************")
        for pt in path_n:
            print(pt[0],pt[1])
    '''
    return all_path

def getpath_2(path,all_path,cur,goal, obstacle, n):
    if cur[0]<0 or cur[0]>n-1 or cur[1]<0 or cur[1]>n-1:
       return
    path.append(cur)
    if cur[0] == goal[0] and cur[1] == goal[1]:
       all_path.append(path)
       return
    if (not (cur[0]+1,cur[1]) in obstacle) and (not (cur[0]+1,cur[1]) in path):
       new_path_1 = list(path)
       getpath_2(new_path_1,all_path,(cur[0]+1,cur[1]),goal,obstacle, n)
    if (not (cur[0],cur[1]+1) in obstacle) and (not (cur[0],cur[1]+1) in path):
       new_path_2 = list(path)
       getpath_2(new_path_2,all_path,(cur[0],cur[1]+1),goal,obstacle,n)
    if (not (cur[0]-1,cur[1]) in obstacle) and (not (cur[0]-1,cur[1]) in path):
       new_path_3 = list(path)
       getpath_2(new_path_3,all_path,(cur[0]-1,cur[1]),goal,obstacle,n)
    if (not (cur[0],cur[1]-1) in obstacle) and (not (cur[0],cur[1]-1) in path):
       new_path_4 = list(path)
       getpath_2(new_path_4,all_path,(cur[0],cur[1]-1),goal,obstacle,n)
 








