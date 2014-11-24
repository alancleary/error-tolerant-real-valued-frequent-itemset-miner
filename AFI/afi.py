# this is an implementation of Approximate Frequent Itemsets (AFI)

import math

# takes a matrix D, row error ratio epsilon_r, column error ratio epsilon_c, and minimum support threshold minsup
def approximate_frequent_itemsets( D, epsilon_r, epsilon_c, minsup ):
    # holds the support set (list of row indices) for each itemset I
    T = {}
    # holds the set of itemsetS at EACH level k
    L = [[[]]]
    # the current level
    k = 0
    # generates the support set (list of row indices) for each item (column)
    for i in range( 0, len( D[ 0 ] ) ):
        # I needs to be frozen so it's immutable and can be used as a key in T
        T[ frozenset( [ i ] ) ] = __gen_support( D, i )
        # each set at the first level holds a single item
        L[ k ].append( [ i ] )
    # the set of AFIs before filtering
    AFI_p = ()
    # until no more potential AFIs have been generated
    while not L[ k ]:
        k++
        # calculate the next (previous) minsup
        previous_minsup_k = math.max( minsup*(1-(((k)*epsilon_c)/(math.floor((k)*epsilon_r)+1))), 0 )
        # generate the set of itemsets for level k
        L[ k ] = __generate_candidate_itemsets( L[ k-1 ], T, previous_minsup )
        # if another 0 is allowed in the itemset
        if math.floor( k*epsilon_r ) == math.floor( (k+1)*epsilon_r ):
            # I is an itemset. how do we generate it?
            #T[ L[ k ] ] = __one_extension( I, L[ k-1 ] )
            T[ frozenset( I ) ] = __one_extension( I, L[ k-1 ] )
        # if another zero is not allowed in the itemset
        else:
            # ditto?
            #T[ L[ k ] ] = __zero_extension( I, L[ k-1 ] )
            T[ frozenset( I ) ] = __zero_extension( I, L[ k-1 ] )
        AFI_p = AFI_p.union( L[ k ] )
    AFI = __filter( AFI_p, minsup, epsilon_c )
    return AFI

# generates the support set (list of rows indices) for each singleton item (column)
def __gen_support( D, i ):
    rows = []
    for r in D:
        if r[ i ] == 1:
            rows.append( r )
    return rows

def __generate_candidate_itemsets( previous_L, T, previous_minsup ):
    # the new set of itemsets
    L = []
    # generate all possible combinations
    return L

# generates a transaction set for the case where additional error will not be tolerated
def __one_extension( I, previous_L ):
    # the transaction set of a (k+1) itemset I is the intersection of the transaction sets of its length k subsets
    T = ()
    return T

# generates a transaction set for the case where additional error will be tolerated
def __zero_extension( I, previous_L ):
    # the transaction set of a (k+1) itemset I is the union of the transaction sets of its length k subsets
    T = ()
    return T

def filter( AFI_p, minsup, epsilon_c ):
    AFI = ()
    return AFI
