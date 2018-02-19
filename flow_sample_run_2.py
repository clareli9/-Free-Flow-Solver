from printf_colour import *
from flow_bridges_csp import *
from propagators import *
import ast, sys
import copy

from flow_bridges_csp import path_map
b0 = [[((0,0),(1,4)),((1,3),(2,0)),((2,1),(2,4)),((3,3),(4,0)),((3,4),(4,1))],5]

b1 = [[((0,1),(3, 0)),((0,4),(4, 0)),((1,4),(3, 3)),((2,2),(2,4))],5]

b2 = [[((0,1),(4,1)),((0,2),(0,4)),((1,1),(3,1)),((1,3),(3,4)),((1,4),(3,3))],5]

b3 = [[((0,0),(2,3)),((0,4),(2,2)),((1,2),(1,4)),((4,0),(2,4))],5]

b4 = [[((2,0),(3,2)),((1,1),(2,3)),((2,1),(4,4)),((3,0),(5,1)),((0,4),(5,2))],6]

b5 = [[((0,0),(4,1)),((3,1),(0,2)),((1,2),(4,2)),((3,3),(0,4)),((4,3),(1,4))],5]

b6 = [[((0,6),(3,0)),((1,6),(6,3)),((5,1),(5,4)),((2,6),(5,5)),((3,4),(5,3)),((6,4),(6,6))],7]

if __name__ == "__main__":

    for b in [b4]:
        print("Solving board:")
        board = []
        for ptp in b[0]:
            board.append([ptp[0], ptp[1]])
        print(create_string([board, b[1]]))

        print("=======================================================")
        print("Using model 2")

        #csp, var_array = flow_bridges_csp_model_2(b, [1,2])
        #csp, var_array = flow_bridges_csp_model_2(b, [0,4])
        csp, var_array = flow_bridges_csp_model_2(b, [0, 4])
        solver = BT(csp)
        solver.bt_search(prop_GAC)
        result = []

        for var in var_array:
            result.append(path_map[var.get_assigned_value()])

        print(create_string([result, 6]))

        #print(var_array)



    for b in []:
        print("Solving board:")
        board = []
        for ptp in b[0]:
            board.append([ptp[0],ptp[1]])
        print(create_string([board,b[1]]))

        print("=======================================================")
        print("Using model 1")
        '''
        csp, var_array = flow_bridges_csp_model_1(b)
        solver = BT(csp)
        #solver.trace_on()
        solver.bt_search(prop_BT)
        '''
        solved = True
        size = len(b[0])
        for i in range(size):
            grid = copy.deepcopy(b)
            print("Now its " + str(i))
            print(grid)
            csp, var_array = flow_bridges_csp_model_1(grid, i)
            solver = BT(csp)
            #solver.trace_on()
            solver.bt_search(prop_BT)
            #if var_array:
                #break
            for var in var_array:
                if var.get_assigned_value():
                    continue
                else:
                    solved = False

            if solved:
                break


        # print("Calling solver")
        '''call solver part'''
        #result = [[[(0,0),(0,1),(0,2),(0,3),(0,4),(1,4)],[(1,3),(1,2),(1,1),(1,0),(2,0)],[(2,1),(2,2),(2,3),(2,4)],[(3,0),(4,0),(3,1),(3,2),(3,3)],[(4,1),(4,2),(4,3),(4,4),(3,4)]],5]
        print("Solution")

        result = []

        '''
        for key, value in path_map.items():
            print(key)
            print(value)

        print("Now it is " + str(i))
        '''
        mirrior_grid = [[0 for row in range(b[1])] for col in range(b[1])]

        for var in var_array:
            result.append(path_map[var.get_assigned_value()])
            for row, col in path_map[var.get_assigned_value()]:
                mirrior_grid[int(row)][int(col)] = 3

        mirrior_grid[int(b[0][i][1][0])][int(b[0][i][1][1])] = 2


        #print(remained_path)
        remained_path = []
        if hasPath(mirrior_grid, remained_path, b[0][i][0][0],b[0][i][0][1]):
            result.append(remained_path)
        # Still need to append the remained path

        print(create_string([result,5]))

            
