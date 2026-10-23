*This Project has been created as a part of the 42 curriculum by tny-onin, rarabeto*

# Description
The goal of **Push Swap** project is to make you discover **algorithme complexity** in a very concrete way.

## The rules

The goal of the Push Swap project is to make you discover algorithm complexity in a very concrete way.
The rules

We must have 2 stacks, a and b.

At the beginning:

    - Stack a contains a random amount of negative and/or positive numbers without any duplicates.

    - Stack b is empty.

The goal is to sort numbers in ascending order into stack a. To do so, you have the following operations at your disposal:
    
| Operations    | Description |
|---------------|-------------|
|sa (swap a)  |Swap the first two elements at the top of stack a. Do nothing if there is only one or no element.|
|sb (swap b)  |Swap the first two elements at the top of stack b. Do nothing if there is only one or no element.|
|ss: sa and sb  at the same time.|
|pa (push a)  |Take the first element at the top of b and put it at the top of a. Do nothing if b is empty.|
|pb (push b)  |Take the first element at the top of a and put it at the top of b. Do nothing if a is empty.|
|ra (rotate a) |Shift up all elements of stack a by one. The first element becomes the last one.|
|rb (rotate b) |Shift up all elements of stack b by one. The first element becomes the last one.|
|rr |ra and rb  at the same time.|
|rra (reverse  rotate a) |Shift down all elements of stack a by one. The last element becomes the first one.|
|rrb (reverse  rotate b) |Shift down all elements of stack b by one. The last element becomes the first one.|
|rrr| rra and  rrb at the same time.|

## Algorithms
### MIN MAX extraction algorithm O(n²)

Min-Max extraction (often called bidirectional selection sort) is an optimized variant of classic selection sort that halves the number of passes through the array.

### Chunk-based sorting O(nsqrt(n))

Chunk-based sorting is a data processing strategy used primarily for algorithmic optimization. The core idea is to divide a massive dataset into manageable chunks, sort them individually, and then merge them.

### Binary indexed approaches O(log n)

The term "binary indexed approaches" refers to the use of bit-manipulated data structures. The most well-known is the Binary Indexed Tree (Fenwick Tree). It allows for updating elements and calculating prefix sums efficiently. Each index is responsible for a range whose size is determined by its least significant bit.

### Custom adaptive algorithm

The custom adaptive algorithm selects different internal methods depending on the measured disorder:

- Low disorder (< 0.2): Uses the simple algorithm (Min-Max extraction) in O(n²).

- Medium disorder (0.2 ≤ d < 0.5): Uses the medium algorithm (chunk-based sorting) in O(nsqrt(n))*.

- High disorder (≥ 0.5): Uses the complex algorithm (Fenwick Tree) in O(n log n).

### The approach is based on:

- Pre-sorting: Analyzing the numbers to identify already ordered sequences.

- Optimized transfer: Pushing elements to stack b by calculating the lowest possible "cost" of moving each number.

- Final sorting: Reinserting elements into stack a, ensuring each element is placed in its exact position.

# Instructions
## Compilation
The project include a `Makefile` for the compilation.

```bash
make

#for the bonus
make bonus
```
## Execution
Run the program with a list of an integer en arguments:

```bash
./push_swap 2 1 5 3 6 8 # default adaptive
./push_swap --simple 2 1 5 3 6 8
./push_swap --medium 2 1 5 3 6 8
./push_swap --complex 2 1 5 3 6 8
./push_swap --adaptive 2 1 5 3 6 8
```
```bash
# execute the bench
./push_swap --bench 2 1 5 3 6 8

# we can also run with sorting strategy
./push_swap --simple --bench 2 1 5 3 6 8
```

You can also run the following bash:
```bash
ARG="4 12 6 3 78 23";
./push_swap $ARG
```
## Checker
For checking if the stack is sorted or not, run:

```bash
ARG="3 6 7 0 2 -1";
./push_swap $ARG | ./checker_linux $ARG
```
## Checker Bonus
We can also check if the stack is sorted or not by running the bonus part.

```bash
./push_swap 1 5 4 87 2 | ./checker 1 5 4 87 2
```

This bonus project can be launched without executing ./push_swap. But in this way, we should enter the operation to sort input.

```bash
./checker 3 2 1 0
# eg of operation
rra
pb
sa
rra
pa
#it should display 'OK' 
```

```bash
./checker 3 2 1 0
# eg of operation
sa
rra
pb
#it should display 'KO' 
```
# Resources

## Core References & Documentation

- 42 Official Documentation: Guidelines and project constraints provided by the 42 Network.

- C Programming (W3Schools): Fundamental syntax and memory management in C.

- Data Structures (Stacks): Understanding LIFO (Last-In, First-Out) logic and pointer-based implementations.

- Algorithmic Complexity: Theoretical background on Big O notation and time/space optimization.

Advanced Algorithms

- Fenwick Tree (Binary Indexed Tree): Detailed implementation guide from CP-Algorithms.

- Sorting Concepts: Comparative study of selection sort and chunk-based sorting strategies.

Visualization & Testing

- Push_Swap Visualizer: Essential tool used to observe stack movements and identify bottlenecks in the sorting logic.

- Valgrind: Used for memory leak detection and profiling parse.c and main logic.

## AI Collaboration (Gemini & ChatGPT)

For this project, we integrated Generative AI as a collaborative partner to refine our approach:

- Architectural Brainstorming (Gemini): Used to discuss the viability of the Adaptive Algorithm and to determine the thresholds between "Low," "Medium," and "High" disorder regimes.

- Logic Validation (ChatGPT): Assisted in conceptualizing the Binary Indexed Tree transformation (index compression) to make it compatible with the push_swap instruction set.

- Debugging & Refinement: Leveraged AI for identifying subtle memory leaks in ft_split and for optimizing the cost-calculation logic during the transfer to stack B.

- Note: AI was used as a pedagogical tool to understand complex concepts; all final code was implemented and verified according to the 42 Norm.