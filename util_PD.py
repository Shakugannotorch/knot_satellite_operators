def entrance_arcs(crossing_PD):
    ordered_arcs = list(crossing_PD)
    ordered_arcs.sort()

    if 0 in ordered_arcs and 1 not in ordered_arcs:
        return (ordered_arcs[1], ordered_arcs[-1])
    else: 
        return (ordered_arcs[0],ordered_arcs[2])

def is_positive_crossing(crossing_PD):
    return crossing_PD[1] not in entrance_arcs(crossing_PD)

def PD_to_LongPD(PD):
    LongPD = []

    for crossing in PD:
        if is_positive_crossing(crossing):
            LongPD += [(1, crossing[-1],crossing[0],0)]
        else:
            LongPD += [(-1, crossing[0], crossing[1],0)]

    return LongPD

def reformulate_longPD(longPD):
    reform = []

    for crossing in longPD:
        if crossing[0] == 1:
            reform += [(crossing[2],crossing[1]+1,crossing[2]+1,crossing[1])]
        else:
            reform += [(crossing[1],crossing[2],crossing[1]+1,crossing[2]+1)]

    return reform

def arcs(PD):
    return [arc for crossing in PD for arc in crossing]

def corresponded_crossings(PD, arc):
    return [crossing for crossing in PD if arc in crossing]

def proceed_and_mod_4(i):
    return (i+1)%4