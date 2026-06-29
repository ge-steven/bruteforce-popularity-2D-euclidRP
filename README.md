# Bruteforce Search for Popular Outcomes in a 2D Euclidean Roommates Game

A pyscript based application that allows you to manually or randomly generate an instance of the 2-Dimensional Euclidean Roommates Problem and generates all popular outcomes by brute force. The purpose of this application is to use the instances of the 2-Dimensional Euclidean Roommates Problem with their corresponding popular outcomes to potentially find a structure that allows us to create a polynomial time algorithm or help us construct a harness proof.

We provide some instances with interesting properties.

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

## In 1D consecutive matching (minimum sum of DISTANCES) is not guaranteed to be popular
Room size: 2

{
    0: [0, 0],
    1: [4, 0],
    2: [4.5, 0],
    3: [6, 0],
    4: [6.5, 0],
    5: [10.5, 0]
}

## In 1D consecutive matching (minimum sum of RANKS) is not guaranteed to be popular
Room size: 2

{ 0: [0, 0], 1: [0.5, 0], 2: [7, 0], 3: [9, 0], 4: [9.5, 0], 5: [10.5, 0], 6: [11, 0], 7: [13, 0], 8: [20, 0], 9: [20.5, 0] }

## Other interesting ones in 1D
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

{
    0: [0, 0],
    1: [5, 0],
    2: [6.5, 0],
    3: [7, 0],
    4: [7.1, 0],
    5: [7.6, 0],
    6: [9.1, 0],
    7: [14.1, 0]
}

{0: [0, 0.0], 1: [2, 0.0], 2: [3.5, 0.0], 3: [5.5, 0.0], 4: [6, 0.0], 5: [6.1, 0.0], 6: [9, 0.0], 7: [13, 0.0], 8: [14, 0.0], 9: [16, 0.0]}
