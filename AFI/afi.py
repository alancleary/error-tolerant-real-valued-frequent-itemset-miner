# this is an implementation of Approximate Frequent Itemsets (AFI)

import math

# takes a matrix D, row error ratio epsilon_r, column error ratio epsilon_c, and minimum support threshold minsup
def approximate_frequent_itemsets( D, epsilon_r, epsilon_c, minsup ):
    # will hold the support set for each I
    T = []
    # holds the set of itemsets at each level k
    L = [[]]
    # the current level
    k = 0
    # generate each item's initially support
    for i in range( 0, len( D[ 0 ] ) ):
        T[ i ] = __gen_support( D, i )
        # each set at the first level holds a single item
        L[ k ].append( ( i ) )
    # the pre-processed AFIs
    AFI_p = ()
    while # L_k is not empty:
        k++
        previous_minsup_k = math.max( minsup*(1-(((k)*epsilon_c)/(math.floor((k)*epsilon_r)+1))), 0 )
        L[ k ] = __generate_candidate_itemset( L[ k-1 ], previous_minsup )
        if math.floor( k*epsilon_r ) == math.floor( (k+1)*epsilon_r ):
            # how do we generate I?
            T[ L[ k ] ] = __one_extension( I, L[ k-1 ] )
        else:
            # ditto?
            T[ L[ k ] ] = __zero_extension( I, L[ k-1 ] )
        AFI_p = AFI_p.union( L[ k ] )
    AFI = __filter( AFI_p, minsup, epsilon_c )
    return AFI

# generates the support for each singleton item
def __gen_support( D, i ):
    pass

def __generate_candidate_itemset( previous_L, previous_minsup ):
    L = []
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
