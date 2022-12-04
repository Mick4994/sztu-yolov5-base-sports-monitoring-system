

NOSE, R_HAND, L_HAND = 0, 9, 10

X,Y = 0, 1

HARD, EASY = 5, 2

def Counter(count, y_list, is_count, hang_line, difficulty):
    y_list = [-i for i in y_list]
    if len(y_list) >= 15:
        if y_list[-15] > -hang_line and is_count == True:
            for s in range(3):
                if y_list[-15 + s] <= -hang_line:
                    break
                if s == 2:
                    is_count = False
                    if max(y_list[-15:-1]) > -hang_line + difficulty:
                        count += 1
        if is_count == False:
            for s in range(3):
                if y_list[-15 + s] >= -hang_line:
                    break
                if s == 2:
                    is_count = True
    return count,is_count

def ReturnCount(count, y_list, is_count, hang_line):
    y_list = [-i for i in y_list]
    if len(y_list) >= 15:
        if y_list[-15] > -hang_line and is_count == True:
            for s in range(3):
                if y_list[-15 + s] <= -hang_line:
                    break
                if s == 2:
                    is_count = False
                    if max(y_list[-15:-1]) > -hang_line - 3:
                        count += 1
        if is_count == False:
            for s in range(3):
                if y_list[-15 + s] >= -hang_line:
                    break
                if s == 2:
                    is_count = True
    return count,is_count

def NewCounter(count, y, is_count, up_bound, down_bound):
    if count == 0:
        if y > up_bound and y > down_bound:
            is_count = True
    if is_count:
        if y < up_bound and y < down_bound:
            count += 1
            is_count = False
    if y > up_bound and y > down_bound:
        is_count = True
    return count, is_count
    
