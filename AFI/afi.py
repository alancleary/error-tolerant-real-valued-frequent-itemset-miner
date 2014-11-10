# this is an implementation of Approximate Frequent Itemsets (AFI)

import math

# takes a matrix D, row error ration epsilon_r, column error threshold epsilon_c, and and minimum support threshold minsup
def approximate_frequent_itemsets( D, epsilon_r, epsilon_c, minsup ):
    T = []
    for i in range( 0, len( D[ 0 ] ) ):
        T[ i ] = __gen_support( D, i )
    k = 1
    # L_1 = union for i > 0 through m of {i}
    while # L_k is not empty:
        k++
        # L_k = __generate_candidate_itemset( L_(k-1), minsup^(k-1) )
        if math.floor( k*epsilon_r ) == math.floor( (k+1)*epsilon_r ):
            # T( L_k ) = __one_extension( I, L_(k-1) )
        else:
            # T( L_k ) = __zero_extension( I, L_(k-1) )
        # AFI_p = AFI_p union L_k
    # AFI = __filter( AFI_p, minsup, epsilon_c )
    return AFI

def __gen_support( D, i ):
    pass

def __generate_candidate_itemset( L, minsup ):
    pass

def __one_extension( I, L ):
    pass

def __zero_extension( I, L ):
    pass
