# this is an implementation of Approximate Frequent Itemsets (AFI)

d = [[1,1,1,0],[1,1,0,0],[1,0,1,0],[0,1,1,0],[1,1,1,1],[0,0,0,1],[0,1,0,1],[1,0,0,0]]

def run():
    e_r = 1.0/3
    e_c = 1.0/3
    afi(d, e_r, e_c, .5)

import math

# takes a matrix D, row error ratio epsilon_r, column error ratio epsilon_c, and minimum support threshold minsup
def afi( D, epsilon_r, epsilon_c, minsup ):
    print "epsilon r", epsilon_r
    print "epsilon_c", epsilon_c
    print "minsup", minsup
    # holds the support set (list of row indices) for each itemset I
    T = {}
    # holds the set of itemsetS at EACH level k
    L = [[]]
    # the current level
    k = 0
    # generates the support set (list of row indices) for each item (column)
    n = len( D )
    for i in range( 0, len( D[ 0 ] ) ):
        #print "support for row", i
        # I needs to be frozen so it's immutable and can be used as a key in T
        itemset = frozenset([i])
        # each set at the first level holds a single item
        L[ k ].append( itemset )
        # we need to know each item's support
        T[ itemset ] = __gen_support( D, i )
        #print T[ itemset ]
    #print "L[ 0 ]"
    #print L[ k ]
    # the set of AFIs before filtering
    AFI_p = set()
    # until no more potential AFIs have been generated
    minsup_k = n*minsup
    while L[ k ]:
        print "previous minsup", minsup_k/n
        k += 1
        #print "level", k
        # generate the set of itemsets for level k
        itemsets_and_support = __generate_candidate_itemsets( L[ k-1 ], T, minsup_k )
        L.append( itemsets_and_support.keys() )
        #print "L[ k ]"
        #print L[ k ]
        # if another 0 is allowed in the itemset
        if math.floor( (k+1)*epsilon_r ) == math.floor( (k+2)*epsilon_r ):
            for itemset in L[ k ]:
                T[ itemset ] = __one_extension( itemsets_and_support[ itemset ] )
        # if another zero is not allowed in the itemset
        else:
            for itemset in L[ k ]:
                T[ itemset ] = __zero_extension( itemsets_and_support[ itemset ] )
        AFI_p = AFI_p.union( L[ k ] )
        # calculate this iteration's minsup
        minsup_k = n*max( minsup*(1-(((k+1)*epsilon_c)/(math.floor((k+1)*epsilon_r)+1))), 0 )
    print "AFI_p"
    print AFI_p
    #AFI = __filter( AFI_p, minsup, epsilon_c )
    #return AFI

# generates the support set (list of rows indices) for each singleton item (column)
def __gen_support( D, j ):
    rows = set()
    for i in range( len( D ) ):
        if D[ i ][ j ] == 1:
            rows.add( i )
    return rows

def __generate_candidate_itemsets( previous_L, T, minsup ):
    # which itemsets will actually contribute to the next itemset?
    contributors = []
    for itemset in previous_L:
        #print "checking"
        #print itemset
        if len( T[ itemset ] ) >= minsup:
            contributors.append( itemset )
    # make the new itemsets
    support = {}
    for i in range( 0, len( contributors )-1 ):
        for j in range( i+1, len( contributors ) ):
            #print "contributors"
            #print contributors[ i ]
            #print contributors[ j ]
            superset = contributors[ i ].union( contributors[ j ] )
            superset = frozenset( superset )
            #print "superset"
            #print superset
            if superset in support:
                support[ superset ].append( T[ contributors[ i ] ] )
                support[ superset ].append( T[ contributors[ j ] ] )
            else:
                support[ superset ] = [ T[ contributors[ i ] ], T[ contributors[ j ] ] ]
    return support

# generates a transaction set for the case where additional error will not be tolerated
def __one_extension( support ):
    # the transaction set of a (k+1) itemset I is the intersection of the transaction sets of its length k subsets
    print "one support"
    #print support
    t = support[ 0 ]
    for i in range( 1, len( support ) ):
        t = t.intersection( support[ i ] )
    return t

# generates a transaction set for the case where additional error will be tolerated
def __zero_extension( support ):
    # the transaction set of a (k+1) itemset I is the union of the transaction sets of its length k subsets
    print "zero extension"
    t = support[ 0 ]
    for i in range( 1, len( support ) ):
        t = t.union( support[ i ] )
    return t

def filter( AFI_p, minsup, epsilon_c ):
    AFI = ()
    return AFI
