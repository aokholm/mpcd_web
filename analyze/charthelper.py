# Chart helping functions 
import copy


def _chartDataJoinX(list_of_xcols):

    # join two first cols
    x = copy.deepcopy(list_of_xcols[0])
    x.extend(list_of_xcols[1])
    
    if (len(list_of_xcols) > 2): # if more than two cols
        new_list_of_xcols = [x] 
        new_list_of_xcols.extend(list_of_xcols[2:])
        return _chartDataJoinX(new_list_of_xcols)
    else:
        return x

# print ChartDataJoinX([x1, x2, x3])


def chartDataJoin(list_of_xcols, list_of_ycols):

    x_column = _chartDataJoinX(list_of_xcols)

    rows = sum ([len(list) for list in list_of_ycols])
    cols = len(list_of_ycols)

    y_joined = []

    current_col = 0
    current_row_in_col = 0

    for l in range(rows):
        print (current_col, current_row_in_col)

        if current_row_in_col == len(list_of_ycols[current_col]):
            current_col+=1
            current_row_in_col = 0

        row = []
        row.extend([x_column[l]])

        for col in range(cols):
            if col == current_col:
                row.extend([list_of_ycols[current_col][current_row_in_col]])
            else:
                row.extend([None])
        y_joined.append(row)
        current_row_in_col+=1

    return y_joined