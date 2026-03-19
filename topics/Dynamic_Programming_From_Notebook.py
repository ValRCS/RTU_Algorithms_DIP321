# %% [markdown]
# # Dynamic Programming
# 
# Today we **Solve once, reuse forever.**
# 
# ## What is Dynamic Programming?
# 
# ### Less strict definition
# 
# Dynamic programming solves complex problems by breaking them into smaller pieces, solving each piece once, and reusing those results instead of repeating work.
# 
# ### Academically sounder definition
# 
# Dynamic programming is a method for solving problems by decomposing them into overlapping subproblems, solving each subproblem once, and systematically storing and reusing their results to construct an optimal global solution.
# 
# ## Why should you care?
# 
# Besides being more practical (read applicable more often), Dynamic Programming problems are favorite of various job interviews. It is almost guaranteed that you would encounter a Dynamic Programming problem when interviewing at the larger companies.
# 

# %% [markdown]
# ![Bellman](https://upload.wikimedia.org/wikipedia/en/7/7a/Richard_Ernest_Bellman.jpg)
# 
# https://en.wikipedia.org/wiki/Richard_E._Bellman

# %% [markdown]
# ## Dynamic Programming - not the programming in computer terms!
# The term dynamic programming (or simply DP) can be a bit confusing to newcomers. Both of the words are
# used in a different way than most might expect. Programming here refers to making a set of choices (as in “linear
# programming”) and thus has more in common with the way the term is used in, say, television, than in writing
# computer programs. Dynamic simply means that things change over time—in this case, that each choice depends
# on the previous one. In other words, this “dynamicism” has little to do with the program you’ll write and is just a
# description of the problem class. In Bellman’s own words, “I thought dynamic programming was a good name. It was
# something not even a Congressman could object to. So I used it as an umbrella for my activities

# %% [markdown]
# * The core technique of DP -> caching
# * Decompose your problem recursively/inductively (usual)
# * allow overlap between the subproblems.
# * Plain recursive solution xponential number of times -> caching trims away waste
# * result is usually both an impressively efficient algorithm and a greater insight into the problem.
# 
# 
# Commonly, DP algorithms turn the recursive formulation upside down, making it iterative and filling out some
# data structure (such as a multidimensional array) step by step.
# 
# * Another option well suited to high-level languages such as Python—is to implement the recursive formulation directly but to cache the return
# values.
# * If a call is made more than once with the same arguments, the result is simply returned directly from the
# cache. This is known as **memoization**

# %% [markdown]
# ## Little puzzle: Longest Increasing Subsequence
# 
# Say you have a sequence of numbers, and you want to find its
# longest increasing (or, rather nondecreasing) subsequence—or one of them, if there are more. A subsequence consists
# of a subset of the elements in their original order. So, for example, in the sequence [3, 1, 0, 2, 4], one solution
# would be [1, 2, 4].

# %% [markdown]
# ## Brute force - when in doubt use brute force

# %%
from itertools import combinations # from standard library

# %%
my_list = [3, 1, 0, 2, 4]
my_list

# %%
list(combinations(my_list, 4))

# %%
list(combinations(my_list, 3)) # 5 choose 3 - formula is n! / (k! * (n - k)!)
# n is the number of items in the list - 5
# k is the number of items in each combination - 3
# so here we have 5! / (3! * (5 - 3)!) = 5! / (3! * 2!) = 120 / (6 * 2) = 120 / 12 = 10

# %%
list(combinations(my_list, 2))

# %%
list(combinations(my_list, 1))
# gives us a list of single item tuples

# %%

def naive_list(seq):
    for length in range(len(seq), 0, -1): # n, n-1, ... , 1 # worse case for decreasing range would be 1 item as a solution
        for sub in combinations(seq, length): # Subsequences of given length
            # TODO find a faster way to check if the subsequence is sorted
            if list(sub) == sorted(sub): # An increasing subsequence? sorted one would be same with the original one
                # possible we could cache the sorted version of the subsequence
                return sub # Return it!

# %%
naive_list([3,1,0,2,4])

# %%
# i started with 5 then 4 then checked 3 number combination
list(combinations(my_list, 3))

# %%
naive_list([5,0,2,1,6,3,7,4,6])

# %%
# This works (on smaller sequences at least)



# %%
import random
random.seed(2024) # Set the seed so we all get the same pseudo-"random" results
r10 = [random.randint(1,100) for _ in range(10)]
r20 = [random.randint(1,100) for _ in range(20)]
r25 = [random.randint(1,100) for _ in range(25)]
r100 = [random.randint(1,1000) for _ in range(100)]
r1k = [random.randint(1,10_000) for _ in range(1000)]
r10

# %%
naive_list(r10)

# %%
%%timeit
naive_list(r10)

# %%
naive_list(r20)

# %%
%%timeit
naive_list(r20)

# %%
naive_list(r25)

# %%
# how about complexity?
# Two nested loops -> n^2 ?
# Hint combinations is not O(1).... so it is at least O(n^2) but more likely O(n^3) or worse

# TODO find exact complexity of this naive_list
# HINT anything involving factorials, is going to be candidate for factorial complexity

# %% [markdown]
# ## Fibonacci numbers

# %%
## Fibonacci
def fib(i): # finding i-th member in our Fibonacci chain 1,1,2,3,5,8,13,21,34,55,89
    if i < 2: # base case - first two numbers are 1
        return 1
    else:
        return fib(i-1) + fib(i-2) # we have two recursive calls, but our problem space is not going down by half

# %%
fib(0),fib(1),fib(2),fib(3),fib(4),fib(5)

# %%
# sidenote: Fibonaccy ratios approach golden mean
for n in range(1,20):
    print(fib(n), fib(n-1), round(fib(n)/fib(n-1),8))

# %% [markdown]
# ![Fib Spiral](https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Fibonacci_spiral_34.svg/500px-Fibonacci_spiral_34.svg.png)

# %% [markdown]
# https://en.wikipedia.org/wiki/Golden_ratio

# %%
# so far so good?
fib(30)

# %%
fib(35)

# %%
fib(36)

# %% [markdown]
# ## Fibonacci Recursion
# 
# https://stackoverflow.com/questions/35959100/explanation-on-fibonacci-recursion
# ![FibTree](https://i.stack.imgur.com/QVSdv.png)

# %%
from functools import wraps
# memo is a function that takes a function as argument and returns a wrapped version of this function with caching
def memo(func):
    cache = {} # Stored subproblem solutions, this dictionary - Hashmap type - so O(1) lookup
    @wraps(func) # Make wrap look like func
    def wrap(*args): # The memoized wrapper
        if args not in cache: # Not already computed? O(1) lookup
            cache[args] = func(*args) # Compute & cache the solution O(1) to store - of func itself will have some cost
        return cache[args] # Return the cached solution - return again is O(1)
    return wrap # Return the wrapper
# PS Python actually has memoization library as well - we are learning here

# %%
fib_memo = memo(fib) #functions are first class citizens in Python


# %%
fib_memo(30)

# %%
fib_memo(34)

# %%
fib_memo(35)

# %%
%%timeit
fib(35)

# %%
@memo # this is a decorator - meaning we wrap our fib_m function in memo function
def fib_m(i):
    if i < 2:
        return 1
    else:
        return fib_m(i-1) + fib_m(i-2)

# %%
%%timeit
fib_m(35)

# %%
%%timeit
fib_m(38)

# %%
%%timeit
fib_m(45)

# %%


# %%
fib_m(36) # well the book implemention does not quite work, it is not caching properly

# %%
fib_m(40)

# %%
fib_m(60)

# %%
fib_m(200)

# %%
import sys
sys.getrecursionlimit()

# %%
fib_m(600) # on Google Colab stack size is limited to 1k by defaulb

# %%
import sys
sys.setrecursionlimit(100_000)

# %%
# check recursion limit
sys.getrecursionlimit()

# %%
fib_m(2000)
# sadly memoization will not solved stack overflow problem

# %%
fib_m(5000)
# sadly memoization will not help us with stack overflow , a good way to force kernel restart :)

# %%
import functools
# https://stackoverflow.com/questions/1988804/what-is-memoization-and-how-can-i-use-it-in-python
@functools.lru_cache(maxsize=None) #by default only 128 latest so by setting it to None I cache everything - this is a decorator
def fib(num):
    if num < 2:
        return num
    else:
        return fib(num-1) + fib(num-2)
# in 3.9 Python there is a newer @functools.cache - similar idea

# %%
fib(35)

# %%
%%timeit
fib(35)

# %%
%%timeit
fib(45)

# %%
%%timeit
fib(100)

# %%
fib(900)

# %%
fib(1_000)

# %%
%%timeit
fib(1_000)

# %%
%%timeit
fib_m(100)  # so my memoization solution is about 2.5x slower than library solution but both are extremely fast

# %%
# so official caching version is 3 times faster than our self-made version, factor of 3 is not a dealbreak but nice to know

# %%
fib(40)

# %%
fib(100)

# %%
fib(200)

# %%
fib(1200)

# %%
fib(3000)

# %%
# let's limit cache to only say 50 values
# https://stackoverflow.com/questions/1988804/what-is-memoization-and-how-can-i-use-it-in-python
@functools.lru_cache(maxsize=50) #by default only 128 latest so by setting it to None I cache everything - this is a decorator
def fib_lim50(num):
    if num < 2:
        return num
    else:
        return fib(num-1) + fib(num-2)
# in 3.9 Python there is a newer @functools.cache - similar idea

# %%
fib_lim50(40)

# %%
%%timeit
fib_lim50(50)

# %%
fib_lim50(70)

# %%
%%timeit
fib_lim50(70)

# %%
%%timeit
fib_lim50(80)

# %%
## TODO investigate on how cache is cleared on cache_lru

# %% [markdown]
# ## Exercises on Memoization
# 
# ### Stair Climbing (Counting Problem)
# 
# **Core idea:**
# Count the number of distinct ways to reach step `n` using a fixed set of allowed step sizes (typically `{1, 2}` or `{1, 2, 3}`).
# 
# #### Problem formulation
# 
# * Input: integer `n` (target step)
# * Allowed moves: e.g., `{1, 2}`
# * Output: number of distinct sequences of moves reaching exactly `n`
# 
# #### Recursive structure
# 
# * Let `f(n)` be the number of ways to reach step `n`
# * Recurrence:
# 
#   * `f(n) = f(n-1) + f(n-2)` (for steps `{1,2}`)
# * Base cases:
# 
#   * `f(0) = 1` (one way: do nothing)
#   * `f(n < 0) = 0`
# 
# #### Memoization insight
# 
# * The same subproblems (`f(n-1)`, `f(n-2)`, etc.) are recomputed many times
# * Cache results for each `n` to reduce exponential recursion to linear time
# 
# #### Extensions (for exploration)
# 
# * Allow `{1, 2, 3}` steps → `f(n) = f(n-1) + f(n-2) + f(n-3)`
# * Introduce forbidden steps (e.g., broken stairs)
# * Return one valid path instead of just the count
# 
# ---
# 
# ### Rod Cutting (Optimization Problem)
# 
# **Core idea:**
# Maximize profit by cutting a rod into pieces, given a price table for each possible length.
# 
# #### Problem formulation
# 
# * Input:
# 
#   * Array `price[i]` = value of rod of length `i`
#   * Integer `n` = total rod length
# * Output: maximum obtainable value
# 
# #### Recursive structure
# 
# * Let `r(n)` be the maximum revenue for length `n`
# * Recurrence:
# 
#   * `r(n) = max(price[i] + r(n - i))` for all `1 ≤ i ≤ n`
# * Base case:
# 
#   * `r(0) = 0`
# 
# #### Memoization insight
# 
# * Many recursive calls recompute `r(k)` for the same `k`
# * Cache computed values of `r(k)` to avoid redundant work
# * Reduces exponential recursion to quadratic time
# 
# #### Extensions (for exploration)
# 
# * Reconstruct actual cuts (not just value)
# * Add cost per cut (penalize excessive splitting)
# * Compare with greedy strategies and show failure cases
# 
# ---
# 
# ### Edit Distance (String Transformation)
# 
# **Core idea:**
# Compute the minimum number of operations required to transform one string into another.
# 
# #### Problem formulation
# 
# * Input: two strings `A` and `B`
# * Allowed operations:
# 
#   * Insert
#   * Delete
#   * Substitute
# * Output: minimum number of operations
# 
# #### Recursive structure
# 
# * Let `d(i, j)` be the edit distance between:
# 
#   * first `i` characters of `A`
#   * first `j` characters of `B`
# * Recurrence:
# 
#   * If characters match:
#     `d(i, j) = d(i-1, j-1)`
#   * Otherwise:
#     `d(i, j) = 1 + min(`
# 
#     * `d(i-1, j)`   (delete)
#     * `d(i, j-1)`   (insert)
#     * `d(i-1, j-1)` (substitute)
#       `)`
# * Base cases:
# 
#   * `d(0, j) = j`
#   * `d(i, 0) = i`
# 
# #### Memoization insight
# 
# * Subproblems `(i, j)` repeat frequently
# * Cache results in a dictionary or 2D structure
# * Converts exponential recursion into polynomial time `O(n·m)`
# 
# #### Extensions (for exploration)
# 
# * Reconstruct the sequence of edits
# * Assign different costs to operations
# * Compare with Longest Common Subsequence (LCS)
# 
# ---
# 
# ## Related topics (brief pointers)
# 
# * Bottom-up tabulation vs top-down memoization
# * State definition and dimensionality in DP
# * Reconstruction of optimal solutions
# * Time–space tradeoffs in DP implementations
# 

# %%
# so the problem with TOP-DOWN memoization is that we are still left with recursive calls going over our stack limit

# %% [markdown]
# ## So how to solve the stack overflow problem?

# %%
# we could try the build up solution - meaning BOTTOM-UP method
# this will usually be an iterative(looping) solution so no worries about stack


# %% [markdown]
# ## Iterative version of Fibonacci with full table

# %%
# silly iterative version
# useful if you want to return ALL fibs
def fib_it(n): # so n will be 0 based
    fibs = [1,1] #so we are going to build our answers
    # lets pretend we do not know of any formulas and optimizations
#     n += 1 # fix this
    if n < 2:
        return fibs[n] # off by one errors
    ndx = 2
    while ndx <= n:
        fibs.append(fibs[ndx-1]+fibs[ndx-2]) # so I am building a 1-d table(array/list) of answers
        # so appending to list incurs some cost as well
        # in fib we could have of course just stored 2 previous values instead of all
        ndx+=1
    return fibs[n] # again off by one indexing 0 based in python and 1 based in our function


# %%
fib_it(2)

# %%
fib_it(4)

# %%
fib_it(100)

# %%
fib(0),fib(1),fib(2),fib(3)

# %%
fib_it(0)

# %%
fib_it(999)

# %%
%%timeit
fib(999)

# %%
%%timeit
fib_it(999)

# %%
%%timeit
fib_it(35)
# turns out this solution will be slower than memoized recursive solution
# why because we spend time setting up a list and appending items

# %%
%%timeit
fib_it(100)

# %%
%%timeit
fib_it(10_000)

# %%
len(str(fib_it(10_000)))

# %%
for n in range(0,10+1):
    print(fib_it(n))

# %%
fib_it(5),fib_it(6)

# %%
fib_it(35),fib_it(36)

# %%
%%timeit
fib_it(35)

# %%
# so one way we could improve is that we do not need to store all this knowledge about previous solutions,
# (unless we were building a table of ALL solutions)

# %%
# so we only need to store 2 values, but this would be improving constant and solving our space complexity
# instead of needing O(n) to store our fib(n), we just need O(1) - since we are onl storing two values
def fib_v2(n):
    prev, cur = 1, 1 # so we save memory by not storing all previous values
    if n <= 1:
        return prev
    ndx = 2
    while ndx <= n:
        prev, cur = cur, prev+cur # python makes it easy to assign 2 values at once with tuple unpacking, right side eval first
        # if your language does not support it you can simply use a third temp variable
        ndx += 1
    return cur

# %%
fib_v2(5),fib_v2(6)

# %%
fib_v2(999)

# %%
%%timeit
fib_v2(35)

# %%
%%timeit
fib_v2(100)

# %%
%%timeit
fib_v2(999)

# %%
%%timeit
fib_v2(100)

# %%
%%timeit
fib_v2(10_000)

# %%
len(str(fib_v2(10_000)))

# %% [markdown]
# ## Pascal's triangle
# ![Triangle](https://upload.wikimedia.org/wikipedia/commons/0/0d/PascalTriangleAnimated2.gif)

# %% [markdown]
# The combinatorial
# meaning of C(n,k) is the number of k-sized subsets you can get from a set of size n.

# %% [markdown]
# In mathematics, a combination is a selection of items from a collection, such that the order of selection does not matter (unlike permutations). https://en.wikipedia.org/wiki/Combination

# %%
# this is horrible again we have 2 recursive calls for each call
def C(n,k):
    # first base case
    if k == 0: return 1 # means we have chosen all k items
    if n == 0: return 0 # means we have no items to choose from
    return C(n-1,k-1) + C(n-1,k)

# %%
C(2,0),C(2,1),C(2,2)

# %%
C(3,0),C(3,1),C(3,2),C(3,3)

# %%
C(4,0),C(4,1),C(4,2),C(4,3),C(4,4)

# %%
for k in range(6):
    print(C(5,k), end=" ")
print()

# %%
C(20,12) # so choosing 12 items from 20

# %%
%%timeit
C(20,12)

# %%
import functools

# %%
# so exact same function just with caching of results
@functools.lru_cache(maxsize=None)
def C_mem(n,k):
    if k == 0: return 1
    if n == 0: return 0
    return C_mem(n-1,k-1) + C_mem(n-1,k)

# %%
C_mem(20,12)

# %%
%%timeit
C_mem(20,12)

# %%
%%timeit
C_mem(25,15)

# %%
%%timeit
C(22,14)

# %%
%%timeit
C_mem(22,14)


# %%
!python --version  # so have to wait for Google to upgrade Python to 3.9, but of course you can try at home on your own computer

# %%
C_mem(50,30)

# %%
C_mem(64,8)

# %%
%%timeit
C_mem(50,30)

# %% [markdown]
# ### lru_cache wrapper
# 
# Newer versions of Python have a decorator that does the same thing as our memoize function. It’s called lru_cache
# There is even a maxsize parameter that allows you to limit the size of the cache. This is useful if you know that
# you’ll only need the last n results. The name stands for “least recently used,” and it means that if the cache is full

# %%
C_mem(64,8) # so BRUTE FORCE for 8-queens problem would require checking this many

# %%
2**32 # no relation to above number

# %%
%%timeit
C_mem(20,12)

# %% [markdown]
# So 3 Million times faster
# And it will only get worse with larger n and k values
# 

# %%
C(22,10)  # keeps getting slower

# %%
C_mem(30,22)

# %%
C_mem(500,127)

# %%
C_mem(2000,1555) # so we calculated how many different ways we can pick 1555 items out of set of 2000 items

# %%
C_mem(49,6)

# %%
C_mem(55,7)  # so our odds in lotteries are not so great...

# %% [markdown]
# You may at times want to rewrite your code to make it iterative. This
# can make it faster, and you avoid exhausting the stack if the recursion depth gets excessive. There’s another reason, too:
# The iterative versions are often based on a specially constructed cache, rather than the generic “dict keyed by parameter
# tuples” used in my @memo.
# 
# This means that you can sometimes use more efficient structures, such as the multidimensional
# arrays of NumPy (this is a C type array dense and efficient), or even just nested lists.
# 
# This custom cache design
# makes it possible to do use DP in more low-level languages(ahem C, C++), where general, abstract solutions such as our @memo decorator
# are often not feasible.
# 
# Note that even though these two techniques often go hand in hand, you are certainly free to use an
# iterative solution with a more generic cache or a recursive one with a tailored structure for your subproblem solutions.
# 
# Let’s reverse our algorithm, filling out Pascal’s triangle directly.

# %%
from collections import defaultdict  # we could use a regular dict , just less work with defaultdict
# in your language check what collections are available, C#, Java have very nice collections libraries
# careful with C++ collections, check complexity on some of them, it might not be O(1) - map for one (which turns out to be ordered)
# you'd need to look up documentation for that particular structure - so in C++ you might need to use unordered map

# %%
def pascal_up(n,k):
    # so tabulated solution, we are going to build a table of solutions
    Cit = defaultdict(int)
    # Cit = {} # turns out going to plain dictionary did not help at all, slow down by 10%
    # careful from off by one errors
    for row in range(n+1):
        Cit[row,0] = 1 # we could have used previous row to calculate this one, technically just need first one
        for col in range(1,k+1): # looking like O(n*k) space and time complexity here right?
            # I am using get to avoid looking at edge cases (where we have no value to look up)
            Cit[row,col] = Cit.get((row-1,col-1),0) + Cit.get((row-1,col),0)
    return Cit[n,k]

# %% [markdown]
# ### Pascal triangle with iterative DP - tabulation

# %%
pascal_up(20,12)

# %%
%%timeit
pascal_up(20,12)

# %%
pascal_up(50,30)

# %%
%%timeit
pascal_up(50,30)

# %%
%%timeit
C_mem(20,12)

# %%
pascal_up(200,120)

# %%
C_mem(200,120)

# %%
pascal_up(2024,1223)

# %%
# C_mem(2000,1255) # so we see the need for iterative version - other way would be to allow tail call optimization in functional languages

# %%
# so we could futher save memory for our pascal_up by only saving the needed information meaning we only need the previous row

# %%


# %% [markdown]
# ### Pascal triangle with iterative DP - tabulation

# %%
pascal_up(20,12)

# %%
%%timeit
pascal_up(20,12)

# %%
pascal_up(50,30)

# %%
%%timeit
pascal_up(50,30)

# %%
%%timeit
C_mem(20,12)

# %%
pascal_up(200,120)

# %%
C_mem(200,120)

# %%
pascal_up(2000,1255)

# %%
# C_mem(2000,1255) # so we see the need for iterative version - other way would be to allow tail call optimization in functional languages

# %%
# so we could futher save memory for our pascal_up by only saving the needed information meaning we only need the previous row

# %% [markdown]
# ## Difference between TOP-DOWN (with memoization) and BOTTOM-UP (with filling up DP table)

# %% [markdown]
# Basically the same thing is going on. The main difference is that we need to figure out which cells in the cache
# need to be filled out, and we need to find a safe order to do it in so that when we’re about to calculate C[row,col], the
# cells C[row-1,col-1] and C[row-1,col] are already calculated. With the memoized function, we needn’t worry about
# either issue: It will calculate whatever it needs recursively.

# %%
## Back to LIS

# %%
# so recursive memoized solution - TOP/DOWN
def rec_lis(seq): # Longest increasing subseq.
    @functools.lru_cache(maxsize=None)
    def L(cur): # Longest ending at seq[cur]
        res = 1 # Length is at least 1 - because well because one number is always going to be a solution to non empty list
        # so for example reversely sorted list would have a solution 1 - because the numbers are going down
        for pre in range(cur): # Potential predecessors
            if seq[pre] <= seq[cur]: # A valid (smaller) predec.
                res = max(res, 1 + L(pre)) # Can we improve the solution?
        return res
    return max(L(i) for i in range(len(seq))) # The longest of them all

# %%
rec_lis([3,1,0,2,4])

# %%
naive_list([3,1,0,2,4,7,-6,9])

# %%
rec_lis([3,1,0,2,4,7,-6,9])  # so 5 should be answer here

# %%
# so recursive memoized solution - TOP/DOWN
# TODO add sequence passing
def rec_lis_full(seq): # Longest increasing subseq.
    @functools.lru_cache(maxsize=None)
    def L(cur): # Longest ending at seq[cur]
        res = 1 # Length is at least 1
        for pre in range(cur): # Potential predecessors
            if seq[pre] <= seq[cur]: # A valid (smaller) predec.
                res = max(res, 1 + L(pre)) # Can we improve the solution?
        return res
    return max(L(i) for i in range(len(seq))) # The longest of them all

# %%
# tabulated solution
# tabulation is the classical dynamic programming approach - BOTTOM - UP
def basic_lis(seq, debug=True):
    L = [1] * len(seq)
    for cur, val in enumerate(seq):
        for pre in range(cur): # so two nested loops smells quadratic right?
            if seq[pre] < val:
                L[cur] = max(L[cur], 1 + L[pre])
                if debug:
                    print(L)
    return max(L) # linear lookup

# %%
# TODO add iterative sequence passing

# %%
basic_lis([3,1,2,0,4])

# %%
basic_lis([3,1,0,2,4])

# %%
basic_lis([3,1,0,2,4,7,-6,9])

# %%
for i,n in enumerate("Valdis",start=100):  # just a Pythonic way of adding index to sequences
    print(i,n)

# %%
basic_lis([3,1,0,2,4,7,9,6])

# %%
# so basic_lis is tabulating and using two nested loops - thus O(n^2) (again not all nested loops will be n^2 but most are)
# can we do better for this increasing subsequence length

# %% [markdown]
# A crucial insight is that if more than one predecessor terminate subsequences of length m, it doesn’t matter which
# one of them we use—they’ll all give us an optimal answer. Say, we want to keep only one of them around; which one
# should we keep? The only safe choice would be to keep the smallest of them, because that wouldn’t wrongly preclude
# any later elements from building on it. So let’s say, inductively, that at a certain point we have a sequence end of
# endpoints, where end[idx] is the smallest among the endpoints we’ve seen for increasing subsequences of length idx+1
# (we’re indexing from 0). Because we’re iterating over the sequence, these will all have occurred earlier than our current
# value, val. All we need now is an inductive step for extending end, finding out how to add val to it. If we can do that, at
# the end of the algorithm len(end) will give us the final answer—the length of the longest increasing subsequence.

# %% [markdown]
# This devilishly clever little algorithm was first was first described by Michael L. Fredman in 1975
# 
# ## Optimal Longest Increasing Subsequence
# https://www.sciencedirect.com/science/article/pii/0012365X7590103X

# %%
# https://docs.python.org/3/library/bisect.html - basically we use binary search to find insertion points
from bisect import bisect  # provides support for maintaining a list in sorted order without having to sort the list after each insertion.
def lis(seq): # Longest increasing subseq.
    end = [] # End-values for all lengths
    for val in seq: # Try every value, in order
        idx = bisect(end, val) # no way to make this constant but this is logn
        if idx == len(end): # Can we build on an end val?
            end.append(val) # Longest seq. extended
        else:
            end[idx] = val # Prev. endpoint reduced
    return len(end) # The longest we found

# %%
lis([3,1,0,2,4,7,9,6])

# %% [markdown]
# ## So Top-Down
# * Create a recursive solution
# * memoize it - (cache it!)
# 
# ## Bottom-Up
# * figure out a way of storing previous results
# * tabulate(calculate) up
# * you might not need to store the full table maybe just previous row - can save space

# %% [markdown]
# 

# %%
## TODO tabulated solution to LIS problem that returns the actual sequence

# %% [markdown]
# ## Coin change solution using dynamic bottom-up programming
# 
# Idea is to use a table of previous results to calculate the next one
# Next solution has to be a sum of two previous solutions - so we can use the previous results to calculate the next one

# %% [markdown]
# Let's remember how our greedy solution failed on some cases
# 
# * For example Greedy would fail on [1, 3, 4] and 6 - where correct solution is 3,3 but greedy would give 4,1,1
# * Another fail would be on [1,10,25] and 31 - greedy would give 25,1,1,1,1,1,1 and correct solution is 10,10,10,1
# 
# Instead we will use a dynamic programming solution - we will use a table to store the results of the previous solutions and use them to calculate the next one

# %%
# we will use a list to store our results
# we will have a sorted list of coins for each amount
# if we have a coin matching the amount we will add it to the list
def find_minimum_coins(amount, coins=(1,5,10,25)):
    table = [0] * (amount + 1) # so we are going to store our results here
    for i in range(1, amount + 1): # so we are going to go through all amounts
        table[i] = min(table[i - c] + 1 for c in coins if c <= i) # so we are going to find the minimum number of coins for each amount
    return table[amount], table

# let's test it on 31
coin_cnt, full_solution = find_minimum_coins(31)
# print full solution with amounts
print(*list(enumerate(full_solution)), sep="\n")

# %%
# lets try it for amount 15, and coins being (1,7,10)
coin_cnt, full_solution = find_minimum_coins(15, (1,7,10))
# print full solution with amounts
print(*list(enumerate(full_solution)), sep="\n")

# %%
# now let's test 31 but use only coins (1,10,25)
coin_cnt, full_solution = find_minimum_coins(31, (1,10,25))
# print full solution with amounts
print(*list(enumerate(full_solution)), sep="\n")

# %%
# lets get max int from sys
import sys
sys.maxsize, 2**63-1 # which is 2^63 - 1 because we also have 0 in our range


# %%
# let's modify the function to store the actual coins used
def find_minimum_coins(amount, coins=(1,5,10,25)):
    table = [sys.maxsize] * (amount + 1) # so we are going to store our results here
    coins_used = [[]] * (amount + 1) # so we are going to store our results here
    for i in range(1, amount + 1): # so we are going to go through all amounts
        # table[i], coins_used[i] = min((table[i - c] + 1, c) for c in coins if c <= i) # so we are going to find the minimum number of coins for each amount
        if i in coins: # exact match so only 1 coin needed
            table[i] = 1
            coins_used[i] = [i]
        else: # now we need to find a minimum by combining previous solutions
            for n in range(i//2+1): # you could just go throuh i but this is a bit faster
                # we check previous solutions for minimum
                if table[n] + table[i-n] < table[i]:
                    table[i] = table[n] + table[i-n]
                    coins_used[i] = coins_used[n] + coins_used[i-n]
    return table[amount], coins_used

# test it on 31
coin_cnt, coins_used = find_minimum_coins(31)
# print coin_cnt
print(coin_cnt)
# print coins used
print(coins_used)

# %%
# now let's check with 1,10,25 on 31
coin_cnt, coins_used = find_minimum_coins(31, (1,10,25))
# print coin_cnt
print(coin_cnt)
# print coins used
print(*coins_used, sep="\n")

# %% [markdown]
# ## Algorithms that use Dynamic Programming
# 
# ### Graph algorithms
# 
# * Shortest path algorithms
# * Longest path algorithms
# * Minimum spanning tree algorithms
# * Maximum flow algorithms
# 
# ### String algorithms
# 
# * Longest common subsequence
# * Longest increasing subsequence
# * Edit distance
# 
# ### Combinatorial algorithms
# 
# * Binomial coefficients - Pascal's triangle
# * Fibonacci numbers
# * Factorials
# 
# ### Geometric algorithms
# 
# * Convex hull
# * Closest pair of points
# * Largest empty rectangle

# %% [markdown]
# ## More Exercises
# 
# ### Coin Change (Number of Ways)
# 
# **Problem Statement**
# Given a set of coin denominations and a target amount, compute the **number of distinct ways** to form that amount using **unlimited copies** of each coin.
# 
# #### Input
# 
# * `coins`: list of positive integers (denominations)
# * `target`: non-negative integer
# 
# #### Output
# 
# * Integer: number of combinations
# 
# #### Key Constraints / Assumptions
# 
# * Order **does not matter** (i.e., combinations, not permutations)
# * Each coin can be used infinitely many times
# 
# #### DP Formulation
# 
# * **State:**
#   `dp[a]` = number of ways to make amount `a`
# * **Base Case:**
#   `dp[0] = 1` (one way to form zero: choose nothing)
# * **Transition:**
#   For each coin ( c ):
#   [
#   dp[a] += dp[a - c] \quad \text{for } a \ge c
#   ]
# 
# #### Iteration Order (Critical)
# 
# ```python
# for coin in coins:
#     for a in range(coin, target + 1):
#         dp[a] += dp[a - coin]
# ```
# 
# #### Complexity
# 
# * Time: ( O(n \cdot target) )
# * Space: ( O(target) )
# 
# #### Common Pitfalls
# 
# * Reversing loop order → counts permutations instead of combinations
# * Forgetting base case `dp[0] = 1`
# 
# ---
# 
# ### 0/1 Knapsack
# 
# **Problem Statement**
# Given `n` items with weights and values, determine the **maximum total value** that can be obtained without exceeding a given capacity. Each item can be taken **at most once**.
# 
# #### Input
# 
# * `weights[0..n-1]`
# * `values[0..n-1]`
# * `capacity`
# 
# #### Output
# 
# * Maximum achievable value
# 
# #### DP Formulation
# 
# * **State:**
#   `dp[i][w]` = maximum value using first `i` items with capacity `w`
# * **Base Cases:**
# 
#   * `dp[0][w] = 0` (no items)
#   * `dp[i][0] = 0` (zero capacity)
# 
# #### Transition
# 
# For item ( i ):
# 
# * If not taken:
#   [
#   dp[i][w] = dp[i-1][w]
#   ]
# * If taken (when ( w \ge weight[i] )):
#   [
#   dp[i][w] = \max(dp[i-1][w],; value[i] + dp[i-1][w - weight[i]])
#   ]
# 
# #### Table Filling Strategy
# 
# * Iterate over items (outer loop)
# * Iterate over capacity (inner loop)
# 
# #### Space Optimization (1D)
# 
# ```python
# for i in range(n):
#     for w in range(capacity, weights[i] - 1, -1):
#         dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
# ```
# 
# #### Complexity
# 
# * Time: ( O(n \cdot capacity) )
# * Space:
# 
#   * 2D: ( O(n \cdot capacity) )
#   * Optimized: ( O(capacity) )
# 
# #### Common Pitfalls
# 
# * Iterating capacity **forward** in 1D version → incorrectly allows reuse of items
# * Confusing with **unbounded knapsack**
# 
# ---
# 
# ### Matrix Chain Multiplication (Advanced)
# 
# **Problem Statement**
# Given a sequence of matrices, determine the most efficient way to multiply them by choosing optimal parenthesization that minimizes scalar multiplication cost.
# 
# #### Input
# 
# * Dimensions array `p[0..n]`
# 
#   * Matrix ( A_i ) has dimensions ( p[i-1] \times p[i] )
# 
# #### Output
# 
# * Minimum number of scalar multiplications
# 
# #### DP Formulation
# 
# * **State:**
#   `dp[i][j]` = minimum cost to multiply matrices ( A_i \dots A_j )
# * **Base Case:**
#   `dp[i][i] = 0` (single matrix requires no multiplication)
# 
# #### Transition
# 
# For all splits ( k \in [i, j-1] ):
# [
# dp[i][j] = \min_{k} \left( dp[i][k] + dp[k+1][j] + p[i-1] \cdot p[k] \cdot p[j] \right)
# ]
# 
# #### Table Filling Order
# 
# * Increasing chain length ( L = 2 \dots n )
# * For each ( (i, j) ) with ( j = i + L - 1 )
# 
# #### Iterative Structure
# 
# ```python
# for L in range(2, n+1):
#     for i in range(1, n-L+2):
#         j = i + L - 1
#         dp[i][j] = INF
#         for k in range(i, j):
#             cost = dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j]
#             dp[i][j] = min(dp[i][j], cost)
# ```
# 
# #### Complexity
# 
# * Time: ( O(n^3) )
# * Space: ( O(n^2) )
# 
# #### Conceptual Focus
# 
# * **DP over intervals**
# * Non-local dependencies (every split must be evaluated)
# * Diagonal table filling
# 
# #### Common Pitfalls
# 
# * Incorrect indexing of dimension array
# * Filling table in wrong order (must ensure subproblems solved first)
# 
# ---
# 
# ## Related Concepts
# 
# * Unbounded vs bounded knapsack
# * DP over sequences vs DP over intervals
# * Order sensitivity in DP transitions
# * Space optimization patterns in tabulation
# 

# %% [markdown]
# ## References and Additional Readings
# 
# ## Materials used
# 
# * https://jeffe.cs.illinois.edu/teaching/algorithms/book/03-dynprog.pdf
# 
# * [Python Algorithms: Mastering Basic Algorithms in the Python Language](https://www.amazon.com/Python-Algorithms-Mastering-Basic-Language/dp/148420056X)
# 
# * Chapter on Dynamic Programming - CLRS https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/


