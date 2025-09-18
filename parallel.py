import snappy
from util_PD import *
"""
sage: parallel(2, 1, snappy.Link("3_1"),0)
>> <Link: 1 comp; 25 cross>

sage: parallel(2, 1, snappy.Link("3_1"),0, do_simplify = True)
>> <Link: 1 comp; 22 cross>

sage: parallel(2, 4, snappy.Link("3_1"),0)
>> <Link: 2 comp; 28 cross>

sage: parallel(3, 1, snappy.Link("3_1"),0)
>> <Link: 1 comp; 56 cross>

sage: parallel(4, 1, snappy.Link("3_1"),0)
>> <Link: 1 comp; 99 cross>

sage: parallel(3,snappy.Link("3_1"),0).PD_code(True,1)
>> 'PD[X[60, 53, 61, 54], X[23, 52, 24, 53], X[98, 51, 99, 52], X[61, 16, 62, 17], X[24, 15, 25, 16], X[99, 14, 100, 15], X[62, 91, 63, 92], X[25, 90, 26, 91], X[100, 89, 101, 90], X[54, 47, 55, 48], X[17, 46, 18, 47], X[92, 45, 93, 46], X[55, 10, 56, 11], X[18, 9, 19, 10], X[93, 8, 94, 9], X[56, 85, 57, 86], X[19, 84, 20, 85], X[94, 83, 95, 84], X[48, 59, 49, 60], X[11, 58, 12, 59], X[86, 57, 87, 58], X[49, 22, 50, 23], X[12, 21, 13, 22], X[87, 20, 88, 21], X[50, 97, 51, 98], X[13, 96, 14, 97], X[88, 95, 89, 96], X[44, 82, 45, 81], X[7, 83, 8, 82], X[106, 66, 107, 65], X[31, 65, 32, 64], X[68, 64, 69, 63], X[105, 29, 106, 28], X[30, 28, 31, 27], X[67, 27, 68, 26], X[104, 104, 105, 103], X[29, 103, 30, 102], X[66, 102, 67, 101], X[112, 72, 1, 71], X[37, 71, 38, 70], X[74, 70, 75, 69], X[111, 35, 112, 34], X[36, 34, 37, 33], X[73, 33, 74, 32], X[110, 110, 111, 109], X[35, 109, 36, 108], X[72, 108, 73, 107], X[6, 78, 7, 77], X[43, 77, 44, 76], X[80, 76, 81, 75], X[5, 41, 6, 40], X[42, 40, 43, 39], X[79, 39, 80, 38], X[4, 4, 5, 3], X[41, 3, 42, 2], X[78, 2, 79, 1]]'


sage: parallel(2, 1, snappy.Link('3_1'),0).view()
>> # draws the parallel (2,1)-double of 0-framed 3_1 knot
"""

def multi_crossing(size):
    crossings = [[snappy.Crossing() for j in range(size)] for i in range(size)]

    for i in range(size):
        for j in range(size):
            if i != size - 1:
                crossings[i][j][2] = crossings[i+1][j][0]
            if j != size - 1:
                crossings[i][j][1] = crossings[i][j+1][3]
                
    return crossings

#return [preceding, successing]
def arc_multi_crossing(multi_cross, arc_index):
    size = len(multi_cross)

    if arc_index == 0:
        return [multi_cross[0][i][0] for i in range(size)]
    elif arc_index == 1:
        return [multi_cross[i][size - 1][1] for i in range(size)]
    elif arc_index == 2:
        return [multi_cross[size-1][size - 1 - i][2] for i in range(size)]
    elif arc_index == 3:
        return [multi_cross[size-1-i][0][3] for i in range(size)]
    
def connect_multi_crossings(multi_cross_1,arc_index_1,multi_cross_2,arc_index_2):
    size = len(multi_cross_1)

    if arc_index_1 == 0:
        for i in range(size):
            multi_cross_1[0][i][0] = arc_multi_crossing(multi_cross_2,arc_index_2)[size-1-i]
    if arc_index_1 == 1:
        for i in range(size):
            multi_cross_1[i][size - 1][1] = arc_multi_crossing(multi_cross_2,arc_index_2)[size-1-i]
    if arc_index_1 == 2:
        for i in range(size):
            multi_cross_1[size-1][size - 1 - i][2] = arc_multi_crossing(multi_cross_2,arc_index_2)[size-1-i]
    if arc_index_1 == 3:
        for i in range(size):
            multi_cross_1[size-1-i][0][3] = arc_multi_crossing(multi_cross_2,arc_index_2)[size-1-i]


# n can be negative to reverse the direction of twist
def parallel(m, n, knot,framing = 0,do_simplify = False):
    assert n != 0
    
    parallel_twist = [[snappy.Crossing() for i in range(m-1)] for j in range(abs(n))]

    # rows proceed from up to down
    if abs(n) > 1:
        for j in range(abs(n)-1):
            this_row = parallel_twist[j]
            next_row = parallel_twist[j+1]
            for i in range(m-2):
                this_row[i][1] = this_row[i+1][3]
                next_row[i][1] = next_row[i+1][3]
                # rows in the middle will be connected twice, but anyway

            for i in range(m-1):
                if i == m-2:
                    this_row[i][0] = next_row[i][1]
                else:
                    this_row[i][0] = next_row[i+1][2]
            
            this_row[0][3] = next_row[0][2]
    else:
        this_row = parallel_twist[0]
        for i in range(m-2):
            this_row[i][1] = this_row[i+1][3]
            
    knott = knot.copy()
    knott.simplify()
    wr = knott.writhe()

    longPD = reformulate_longPD(PD_to_LongPD(knott.PD_code()))
    multi_crossings = {}
    
    for crossing in longPD:
        multi_crossings.update({crossing:multi_crossing(m)})

    for arc in arcs(longPD):
        corre = corresponded_crossings(longPD,arc)
        if len(corre) == 2:
            indices = [corre[0].index(arc),corre[1].index(arc)]

            connect_multi_crossings(multi_crossings[corre[0]],indices[0],multi_crossings[corre[1]],indices[1])
            
        elif arc == 0:
            indices = [corre[0].index(arc)]

            for i in range(m-1):
                parallel_twist[0][i][2] = arc_multi_crossing(multi_crossings[corre[0]],indices[0])[i]

            parallel_twist[0][-1][1] = arc_multi_crossing(multi_crossings[corre[0]],indices[0])[-1]

        else:
            indices = [corre[0].index(arc)]
            if framing - wr == 0:
                framing_multis = []

                for i in range(m-1):
                    parallel_twist[-1][-1-i][0] = arc_multi_crossing(multi_crossings[corre[0]],indices[0])[i]

                parallel_twist[-1][0][3] = arc_multi_crossing(multi_crossings[corre[0]],indices[0])[-1]

            else:
                framing_multis = [multi_crossing(m) for i in range(abs(framing-wr))]

                connect_multi_crossings(framing_multis[0],1,multi_crossings[corre[0]],indices[0])

                for i in range(m-1):
                    parallel_twist[-1][-1-i][0] = arc_multi_crossing(framing_multis[-1],0)[i]

                parallel_twist[-1][0][3] = arc_multi_crossing(framing_multis[-1],0)[-1]

                for i in range(abs(framing-wr)):
                    connect_multi_crossings(framing_multis[i],2,framing_multis[i],3)

                    if i <abs(framing-wr)-1:
                        connect_multi_crossings(framing_multis[i+1],1,framing_multis[i],0)
                if framing-wr<0:
                    for multi in framing_multis:
                        for row in multi:
                            for cross in row:
                                cross.rotate(1)

    if n < 0:
        for row in parallel_twist:
            for cross in row:
                cross.rotate(1)

    crossings =[crossing for multi in list(multi_crossings.values()) for row in multi for crossing in row]+[crossing for row in parallel_twist for crossing in row]+[crossing for multi in framing_multis for row in multi for crossing in row]

    ans = snappy.Link(crossings)
    if do_simplify: ans.simplify()

    return ans
