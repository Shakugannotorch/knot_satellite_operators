import snappy
from util_PD import *

"""
sage: len(whitehead_double(snappy.Link('3_1'),0, do_simplify = False).PD_code())
>> 26
sage: len(whitehead_double(snappy.Link('3_1'),0, do_simplify = True).PD_code())
>> 23 

sage: whitehead_double(snappy.Link('3_1'),0).PD_code(True)
'PD[X[18, 23, 19, 24], X[41, 25, 42, 24], X[42, 35, 43, 36], X[17, 37, 18, 36], X[22, 27, 23, 28], X[37, 29, 38, 28], X[38, 31, 39, 32], X[21, 33, 22, 32], X[26, 19, 27, 20], X[33, 21, 34, 20], X[34, 39, 35, 40], X[25, 41, 26, 40], X[3, 31, 4, 30], X[29, 5, 30, 4], X[46, 15, 47, 16], X[13, 17, 14, 16], X[14, 43, 15, 44], X[45, 45, 46, 44], X[50, 11, 51, 12], X[9, 13, 10, 12], X[10, 47, 11, 48], X[49, 49, 50, 48], X[2, 7, 3, 8], X[5, 9, 6, 8], X[6, 51, 7, 0], X[1, 1, 2, 0]]'

sage: whitehead_double(snappy.Link('3_1'),0,False).view()
>>> # draws the whitehead double of 0-framed 3_1 knot
""" 
        
def double_crossing():
    crossings = [snappy.Crossing() for i in range(4)]
    crossings[0][1] = crossings[1][3]
    crossings[1][2] = crossings[2][0]
    crossings[2][3] = crossings[3][1]
    crossings[3][0] = crossings[0][2]

    return crossings

#return [preceding, successing]
def arc_double_crossing(double_cross, arc_index):
    return [double_cross[arc_index][arc_index],double_cross[proceed_and_mod_4(arc_index)][arc_index]]

"""
The variable framing controls the frame on the knot diagram to be doubled, in the way that 
it adds Reidemester I moves so that the writhe of the original diagram is equal to the value of framing. 
"""
def whitehead_double(knot,framing = 0,do_simplify = False):
    up = snappy.Crossing()
    down = snappy.Crossing()
    up[0],up[1] = down[1], down[0]

    knott = knot.copy()
    knott.simplify()
    wr = knott.writhe()

    longPD = reformulate_longPD(PD_to_LongPD(knott.PD_code()))
    double_crossings = {}
    
    for crossing in longPD:
        double_crossings.update({crossing:double_crossing()})

    for arc in arcs(longPD):
        corre = corresponded_crossings(longPD,arc)
        if len(corre) == 2:
            indices = [corre[0].index(arc),corre[1].index(arc)]

            [double_crossings[corre[1]][proceed_and_mod_4(indices[1])][indices[1]],double_crossings[corre[1]][indices[1]][indices[1]]]= arc_double_crossing(double_crossings[corre[0]],indices[0])
        elif arc == 0:
            indices = [corre[0].index(arc)]
            [down[2],up[3]] = arc_double_crossing(double_crossings[corre[0]],indices[0])
        else:
            indices = [corre[0].index(arc)]
            if framing - wr == 0:
                framing_doubles = []
                [up[2],down[3]] = arc_double_crossing(double_crossings[corre[0]],indices[0])
            else:
                framing_doubles = [double_crossing() for i in range(abs(framing-wr))]

                [framing_doubles[0][proceed_and_mod_4(1)][1],framing_doubles[0][1][1]] = arc_double_crossing(double_crossings[corre[0]],indices[0])

                [up[2],down[3]] = arc_double_crossing(framing_doubles[-1],0)

                for i in range(abs(framing-wr)):
                    [framing_doubles[i][proceed_and_mod_4(2)][2],framing_doubles[i][2][2]] = arc_double_crossing(framing_doubles[i],3)
                    if i <abs(framing-wr)-1:
                        [framing_doubles[i+1][proceed_and_mod_4(1)][1],framing_doubles[i+1][1][1]] = arc_double_crossing(framing_doubles[i],0)
                if framing-wr<0:
                    for double in framing_doubles:
                        for crossing in double:
                            crossing.rotate(1)
    crossings =[crossing for double in list(double_crossings.values()) for crossing in double]+[up,down]+[crossing for double in framing_doubles for crossing in double]
    whitehead = snappy.Link(crossings)
    if do_simplify: whitehead.simplify()

    return whitehead
