# S   -> NP VP
# VP  -> V NP | V NP PP
# PP  -> P NP
# V   -> END
# NP  -> END | Det N | Det N PP
# Det -> END
# N   -> END
# P   -> END

dev = False
test = ["Det", "N", "V", "Det", "N", "P", "Det", "N"]
tags = test

def cfg_check():
    global i
    i = 0
    print S()

def S():
    if dev: print "S"
    return ( NP(), VP() ) == ( True, True ) and i == len(tags)

def VP():
    if dev: print "VP"
    part = ( V(), NP() ) == ( True, True )
    # Even if V NP, may need to check V NP PP
    if i == len(tags):
        return part
    elif part:
        return PP() == True
    else:
        return False

def PP():
    if dev: print "PP"
    return ( P(), NP() ) == ( True, True )

def NP():
    if dev: print "NP"
    global i

    try:
        tags[i]
    except IndexError:
        return False

    if tags[i] == "NP":
        if dev: print "Found NP at pos", i
        i += 1
        return True
    else:
        # Overlooks the Det N PP rule as a possibility
        return ( Det(), N() ) == ( True, True )
        # part = ( Det(), N() ) == ( True, True )
        #
        # # Even if Det N, may need to check Det N PP
        # # TODO incomplete if statement. i could be in middle and this case still exists
        # if i == len(tags):
        #     return part
        # elif part:
        #     return PP() == True
        # else:
        #     return False

def V():
    if dev: print "V"
    global i

    try:
        tags[i]
    except IndexError:
        return False

    if tags[i] == "V":
        if dev: print "Found V at pos", i
        i += 1
        return True
    else:
        return False

def N():
    if dev: print "N"
    global i

    try:
        tags[i]
    except IndexError:
        return False

    if tags[i] == "N":
        if dev: print "Found N at pos", i
        i+=1
        return True
    else:
        return False

def P():
    if dev: print "P"
    global i

    try:
        tags[i]
    except IndexError:
        return False

    if tags[i] == "P":
        if dev: print "Found P at pos", i
        i+=1
        return True
    else:
        return False

def Det():
    if dev: print "Det"
    global i

    try:
        tags[i]
    except IndexError:
        return False

    if tags[i] == "Det":
        if dev: print "Found Det at pos", i
        i+=1
        return True
    else:
        return False


tags = test
cfg_check()
