# Bruteforce Search for Popular Outcomes in a 2D Euclidean Roommates Game

A pyscript based application that allows you to manually or randomly generate an instance of the 2-Dimensional Euclidean Roommates Problem and generates all popular outcomes by brute force. We provide some instances with interesting properties

## No Popular Outcome in 2D
Room Size: 3

{0: [-2, 0],
 1: [-1, 1],
 2: [1, 1],
 3: [2, 0],
 4: [-6, 5],
 5: [6, 5],
 6: [-0.5, -1],
 7: [0.5, -1],
 8: [0, -6]}
 
## Pair with Smallest Distance (Greedy)
A pair with the smallest overall distance is not guaranteed to be in a popular outcome.

Room size: 2

{
    0: [-1, -5],
    1: [-1, -3],
    2: [-1, -1],
    3: [0, 0],
    4: [1, 0],
    5: [2, -1],
    6: [2, -2.5],
    7: [2, -5]
}

## In 1D consecutive matching (minimum sum of distances) is not guaranteed to be popular
Room size: 2

{
    0: [0, 0],
    1: [4, 0],
    2: [4.5, 0],
    3: [6, 0],
    4: [6.5, 0],
    5: [10.5, 0]
}

## Another interesting one in 1D
Room size: 2

{
    0: [0, 0],
    1: [0.5, 0],
    2: [7, 0],
    3: [9, 0],
    4: [9.5, 0],
    5: [10.5, 0],
    6: [11, 0],
    7: [13, 0]
}
