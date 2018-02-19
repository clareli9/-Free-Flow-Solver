def create_string(result):
    n = result[1]
    result_path = result[0]

    fg_colours = {
        'red': '\033[31m',
        'cyan': '\033[36m',
        'blue': '\033[34m',
        'green': '\033[32m',
        'magenta': '\033[35m',
        'yellow': '\033[33m',
        'normal': '\033[0m'
    }
    bg_colours = {
        0: '\033[41m',
        1: '\033[47m',
        2: '\033[44m',
        3: '\033[42m',
        4: '\033[45m',
        5: '\033[43m',
        6: '\033[0m'
    }    

    map = []
    for y in range(0, n):
        row = []
        for x in range(0, n):
            row += ['__']
        map += [row]
        
    i = 0
    for path in result_path:
        for pt in path:
            map[int(pt[1])][int(pt[0])] = bg_colours[i] +'__'+ bg_colours[6]
        i += 1
    s = '  '
    for i in range(0,n):
        s += ' '
        s += str(i)

    s += '\n'
    j = 0
    for row in map:
        s += ' '
        s += str(j)
        for char in row:
            s += char
        s += '\n'
        j += 1

    return s     

if __name__ == "__main__":
    result = [[[(0,0),(0,1),(0,2),(0,3),(0,4),(1,4)],[(1,3),(1,2),(1,1),(1,0),(2,0)],[(2,1),(2,2),(2,3),(2,4)],[(3,0),(4,0),(3,1),(3,2),(3,3)],[(4,1),(4,2),(4,3),(4,4),(3,4)]],5]
    print(create_string(result))
