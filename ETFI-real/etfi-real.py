# this is an implementation of Approximate Frequent Itemsets (AFI)

d = [[2.0, 2.1, 8.0, 2.0, 2.0],[2.1, 2.2, 2.2, 2.2, 2.2],[4.0, 4.0, 9.0, 4.0, 4.0],[6.5, 6.6, 6.5, 20.0, 6.5],[8.0, 20.0, 8.8, 8.0, 8.0],[9.0, 20.0, 9.1, 10.0, 9.1],[3.2, 3.0, 8.0, 20.0, 3.2],[2.0, 2.0, 2.0, 2.0, 2.0]]

def example():
    print "input"
    print "epsilon_r"
    e_r = 1.0/3
    print e_r
    print "epsilon_c"
    e_c = 1.0/3
    print e_c
    print "matrix D"
    print d
    rAFIs = etfi_real(d, e_r, e_c, .5)
    print "output"
    print "rAFIs"
    print rAFIs

import math

# takes a matrix D, row error ratio epsilon_r, column error ratio epsilon_c, and minimum support threshold minsup
def etfi_real( D, epsilon_r, epsilon_c, minsup ):
    # holds the support set (list of row indices) for each itemset I
    T = {}
    # holds the set of itemsetS at EACH level k
    L = [[]]
    # the current level
    k = 0
    # generates the support set (list of row indices) for each item (column)
    n = len( D )
    for i in range( 0, len( D[ 0 ] ) ):
        # I needs to be frozen so it's immutable and can be used as a key in T
        itemset = frozenset([i])
        # each set at the first level holds a single item
        L[ k ].append( itemset )
        # we need to know each item's support
        T[ itemset ] = __gen_support( D, i )
    # the set of AFIs before filtering
    AFI_p = []
    # until no more potential AFIs have been generated
    minsup_k = n*minsup
    while L[ k ]:
        k += 1
        # calculate this iteration's minsup
        minsup_k = n*max( minsup*(1-(((k+1)*epsilon_c)/(math.floor((k+1)*epsilon_r)+1))), 0 )
        # generate the set of itemsets for level k
        itemsets_and_subsets = __generate_candidate_itemsets( L[ k-1 ], T, minsup_k, D, epsilon_r, epsilon_c )
        print "pre extension"
        print itemsets_and_subsets
        # if another 0 is allowed in the itemset
        if math.floor( (k)*epsilon_r ) == math.floor( (k+1)*epsilon_r ):
           __one_extension( itemsets_and_subsets, T )
        # if another zero is not allowed in the itemset
        else:
            __zero_extension( itemsets_and_subsets, T, D, epsilon_r )
        # the remaining itemsets are AFIs
        L.append( itemsets_and_subsets.keys() )
        # add the itemsets to the global list of AFIs and remove their subsets
        for itemset in itemsets_and_subsets.keys():
            for subset in itemsets_and_subsets[ itemset ]:
                if subset in AFI_p:
                    AFI_p.remove( subset )
            AFI_p.append( itemset )
    #AFI = __filter( AFI_p, minsup, epsilon_c, T, n )
    AFI = AFI_p
    return AFI

# generates the support set (list of rows indices) for each singleton item (column)
def __gen_support( D, j ):
    rows = set()
    for i in range( len( D ) ):
        if D[ i ][ j ] == 1:
            rows.add( i )
    return rows

# generates all possible length k+1 itemsets given a set of length k itemsets, and then prunes them
def __generate_candidate_itemsets( previous_L, T, minsup_k, D, epsilon_r, epsilon_c ):
    n = len( D )
    # find all possible size k+1 itemsets
    itemsets_and_subsets = {}
    for i in range( 0, len( previous_L )-1 ):
        for j in range( i+1, len( previous_L ) ):
            itemset = previous_L[ i ].union( previous_L[ j ] )
            itemset = frozenset( itemset )
            if len( itemset ) == len( previous_L[ i ] )+1:
                if itemset in itemsets_and_subsets:
                    itemsets_and_subsets[ itemset ].add( previous_L[ i ] )
                    itemsets_and_subsets[ itemset ].add( previous_L[ j ] )
                else:
                    itemsets_and_subsets[ itemset ] = set([ previous_L[ i ], previous_L[ j ] ])
    print "generated"
    print itemsets_and_subsets
    # generate all possible size k subsets for each itemset and see if any of them don't support the itemset
    for itemset in itemsets_and_subsets.keys():
        subsets = __generate_subsets( set(), list( itemset ), len( itemset )-1 )
        difference = itemsets_and_subsets[ itemset ].symmetric_difference( subsets )
        # if a non-AFI was found to be a subset, then the symmetric difference will not be empty
        if difference:
            print "eliminating for lack of support"
            del itemsets_and_subsets[ itemset ]
            break
        # prune itemsets that are not within the row error threshold
        subset_transactions = [ T[ s ] for s in itemsets_and_subsets[ itemset ] ]
        support = subset_transactions[ 0 ]
        for i in range( 1, len( subset_transactions ) ):
            support.update( subset_transactions[ i ] )
        if len( support ) < n*minsup_k:
            print "eliminating for not meeting minsup"
            print itemset
            del itemsets_and_subsets[ itemset ]
            break
        for t in support:
            non_error = 0
            for i in itemset:
                if D[ t ][ i ] == 1:
                    non_error += 1
            if non_error < (1-epsilon_r)*len( itemset ):
                print "eliminating for row error"
                print itemset
                del itemsets_and_subsets[ itemset ]
                break
        if itemset not in itemsets_and_subsets:
            continue
        # prune itemsets that are not within the column error threshold
        for i in itemset:
            non_error = 0
            for t in support:
                if D[ t ][ i ] == 1:
                    non_error += 1
            if non_error < (1-epsilon_c)*minsup_k*n:
                print "eliminating for column error"
                print itemset
                del itemsets_and_subsets[ itemset ]
                break
    # the remaining itemsets are the candidates
    return itemsets_and_subsets

# a helper function that generates all possible length k subsets of a given length k+1 set
def __generate_subsets( previous, itemset, k ):
    subsets = set()
    if len( previous ) < k:
        for i in range( len( itemset ) ):
            current = set( previous )
            current.add( itemset[ i ] )
            subsets = subsets.union( __generate_subsets( current, itemset[ i+1: ], k ) )
    else:
        subsets.add( frozenset( previous ) )
    return subsets


# generates a transaction set for the case where additional error will not be tolerated
def __one_extension( itemsets_and_subsets, T ):
    for itemset in itemsets_and_subsets.keys():
        # make a list of the supporting transactions
        transactions = [ T[ s ] for s in itemsets_and_subsets[ itemset ] ]
        # the transaction set of a (k+1) itemset I is the intersection of the transaction sets of its length k subsets
        t = set(transactions[ 0 ])
        for i in range( 1, len( transactions ) ):
            t.intersection_update( transactions[ i ] )
        T[ itemset ] = t

# generates a transaction set for the case where additional error will be tolerated
def __zero_extension( itemsets_and_subsets, T, D, epsilon_r ):
    m = len( D[ 0 ] )
    # the transaction set of a (k+1) itemset I is the rows in the database that have <= epsilon_r error in their support for I
    for itemset in itemsets_and_subsets.keys():
        # make a list of the supporting transactions
        t = set()
        for i in range( len( D ) ):
            num_support = 0
            for j in itemset:
                if D[ i ][ j ] == 1:
                    num_support += 1
            if num_support/m > epsilon_r:
                t.add( i )
        T[ itemset ] = t

def __filter( AFI_p, minsup, epsilon_c, T, n ):
    item_support = math.ceil( n*minsup*(1.0-epsilon_c) )
    AFI = []
    for itemset in AFI_p:
        if len( T[ itemset ] ) >= minsup*n:
            is_AFI = True
            for item in itemset:
                support = T[ frozenset([ item ]) ].intersection( T[ itemset ] )
                is_AFI = len( support ) > item_support
                if not is_AFI:
                    break
            if is_AFI:
                AFI.append( itemset )
    return AFI
