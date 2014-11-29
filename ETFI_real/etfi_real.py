# this is an implementation of Approximate Frequent Itemsets (ETFI)

#d = [[2.0, 2.1, 8.0, 2.0, 2.0],[2.1, 2.2, 2.2, 2.2, 2.2],[4.0, 4.0, 9.0, 4.0, 4.0],[6.5, 6.6, 6.5, 20.0, 6.5],[8.0, 20.0, 8.8, 8.0, 8.0],[9.0, 20.0, 9.1, 10.0, 9.1],[3.2, 3.0, 8.0, 20.0, 3.2],[2.0, 2.0, 2.0, 2.0, 2.0]]
d = [[0,0,0,0,0,0,0,0,0,0],
    [0,5.1,5.2,5.2,2.0,0,0,0,0,0],
    [0,2.2,2.2,2.1,2.0,0,0,0,0,0],
    [0,2.0,5.0,2.2,2.0,0,0,0,0,0],
    [0,0,0,0,0,10.5,10.6, 0,0,0],
    [0,0,0,0,0,0,0,0.1,0.1,0.2],
    [0,0,0,0,0,0,0,0.05,0.06,0.05],
    [0,0,0,0,0,0,0,0.13,0.12,0.11],
    [0,0,0,0,0,0,0,0.11,0.11,0.12]]

def example():
    ETFIs = etfi_real(d, 0.25, 0.25, 2, 0.1, 0.1)
    print "ETFIs"
    print ETFIs

import math

# takes a matrix D, row error ratio epsilon_r, column error ratio epsilon_c, and minimum support threshold minsup
def etfi_real( D, epsilon_r, epsilon_c, range_support, alpha, minsup ):
    T = {} # holds the support set (list of row indices) for each itemset I
    L = [[]] # holds the set of itemsetS at EACH level k
    E = [] # for each transaction, tells us whether positive or negative values are errors with respect to each itemset
    k = 0 # the current level
    n = len( D )
    m = len( D[ 0 ] )
    # all transactions meet the minsup criteria for each singleton
    for i in range( n ):
        E.append( {frozenset([ i ]): 0 for i in range( m )} )
        for j in range( m ):
            E[ i ][ frozenset([ j ]) ] = (1 if D[ i ][ j ] >= 0 else -1)

    all_transactions = set([ i for i in range( n ) ])
    for i in range( 0, m ):
        itemset = frozenset([i]) # I needs to be frozen so it's immutable and can be used as a key in T
        rs = __range_support( itemset, all_transactions, D, E )
        # check that the itemset meets the rangesupport measure
        if rs >= range_support:
            L[ k ].append( itemset )
            T[ itemset ] = all_transactions
    ETFI = [] # the set of ETFIs before filtering
    # until no more potential ETFIs have been generated
    while L[ k ]:
        k += 1
        # calculate this iteration's minsup
        minsup_k = max( minsup*(1-((k*epsilon_c)/(math.floor(k*epsilon_r)+1))), 0 )
        # generate the set of itemsets for level k
        itemsets_and_subsets = __generate_candidate_itemsets( L[ k-1 ] )
        # if another 0 is allowed in the itemset
        if math.floor( (k)*epsilon_r ) == math.floor( (k+1)*epsilon_r ):
            __one_extension( itemsets_and_subsets, T )
            __generate_support( itemsets_and_subsets.keys(), T, D, E, epsilon_r, alpha )
        # if another zero is not allowed in the itemset
        else:
            __zero_extension( itemsets_and_subsets, T, all_transactions )
            __generate_support( itemsets_and_subsets.keys(), T, D, E, epsilon_r, alpha )
        # filter the itemsets using the range_support criteria
        for itemset in itemsets_and_subsets.keys():
            rs = __range_support( itemset, T[ itemset ], D, E )
            if rs < range_support or len( T[ itemset ] ) < n*minsup_k:
                del T[ itemset ]
                del itemsets_and_subsets[ itemset ]
        # the remaining itemsets are ETFIs
        L.append( itemsets_and_subsets.keys() )
        # add the itemsets to the global list of ETFIs and remove their subsets
        for itemset in itemsets_and_subsets.keys():
            for subset in itemsets_and_subsets[ itemset ]:
                if subset in ETFI:
                    ETFI.remove( subset )
            ETFI.append( itemset )
    return ETFI

# a function that finds the range_support for a given itemset in a given set of transactions
def __range_support( itemset, transactions, D, E ):
    rs = 0
    for t in transactions:
        positive = set()
        negative = set()
        for i in itemset:
            if D[ t ][ i ] > 0:
                positive.add( i )
            elif D[ t ][ i ] < 0:
                negative.add( i )
        # we're assuming the transactions already meet the range criteria
        # is positive or negative considered the error?
        if E[ t ][ itemset ] > 0: # negative is the error
            if len( positive ) > 0:
                rs += min([ D[ t ][ i ] for i in positive ])
        elif E[ t ][ itemset ] < 0: # positive is the error
            rs += min([ abs( D[ t ][ i ] ) for i in negative ])
        else: # neither is the error
            rs += max( min([ D[ t ][ i ] for i in positive ]), min([ abs( D[ t ][ i ] ) for i in negative ]) )
    return rs

# generates all possible length k+1 itemsets given a set of length k itemsets, and then prunes them
def __generate_candidate_itemsets( previous_L ):
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
    # generate all possible size k subsets for each itemset and see if any of them don't support the itemset
    for itemset in itemsets_and_subsets.keys():
        subsets = __generate_subsets( set(), list( itemset ), len( itemset )-1 )
        difference = itemsets_and_subsets[ itemset ].symmetric_difference( subsets )
        # if a non-ETFI was found to be a subset, then the symmetric difference will not be empty
        if difference:
            del itemsets_and_subsets[ itemset ]
            continue
        # remove itemsets that don't meet the minsup criteria?????

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

# a function that determines if the given transaction and itemset meet the range criteria for alpha
def __range( transaction, itemset, alpha ):
    top = max([ abs( transaction[ i ] ) for i in itemset ])
    bottom = min([ abs( transaction[ i ] ) for i in itemset ])
    return top-bottom <= alpha*bottom

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
def __zero_extension( itemsets_and_subsets, T, all_transactions ):
    for itemset in itemsets_and_subsets.keys():
        # each itemset is set to all transactions so __generate_support scans the entire database
        T[ itemset ] = all_transactions

# given a set of itemsets and their transactions, this function prunes the transactions that don't meet the range criteria for each itemset
def __generate_support( itemsets, T, D, E, epsilon_r, alpha ):
    for itemset in itemsets:
        max_error = epsilon_r*len( itemset )
        remove = []
        for t in T[ itemset ]:
            positive = set()
            negative = set()
            zero = 0
            for i in itemset:
                if D[ t ][ i ] > 0:
                    positive.add( i )
                elif D[ t ][ i ] < 0:
                    negative.add( i )
                else:
                    zero += 1
            if zero+len( positive ) <= max_error and zero+len( negative ) <= max_error:
                positive_max = max( D[ t ][ i ] for i in positive )
                positive_min = min( D[ t ][ i ] for i in positive )
                positive_range = ((positive_max-positive_min)*1.0)/positive_min
                negative_max = max( abs( D[ t ][ i ] ) for i in positive )
                negative_min = min( abs( D[ t ][ i ] ) for i in positive )
                negative_range = ((negative_max-negative_min)*1.0)/negative_min
                if positive_range <= alpha*positive_min and negative_range <= alpha*negative_min:
                    E[ t ][ itemset ] = 0
                elif positive_range <= alpha*positive_min:
                    E[ t ][ itemset ] = 1
                elif negative_range <= alpha*negative_min:
                    E[ t ][ itemset ] = -1
                else:
                    remove.append( t )
            elif zero+len( negative ) <= max_error:
                positive_max = max( D[ t ][ i ] for i in positive )
                positive_min = min( D[ t ][ i ] for i in positive )
                positive_range = ((positive_max-positive_min)*1.0)/positive_min
                if positive_range <= alpha*positive_min:
                    E[ t ][ itemset ] = 1
                else:
                    remove.append( t )
            elif zero+len( positive ) <= max_error:
                negative_max = max( abs( D[ t ][ i ] ) for i in positive )
                negative_min = min( abs( D[ t ][ i ] ) for i in positive )
                negative_range = ((negative_max-negative_min)*1.0)/negative_min
                if negative_range <= alpha*negative_min:
                    E[ t ][ itemset ] = -1
                else:
                    remove.append( t )
            else:
                remove.append( t )
        for t in remove:
            T[ itemset ].remove( t )

