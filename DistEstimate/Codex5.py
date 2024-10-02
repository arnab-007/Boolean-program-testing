import subprocess
import random
import re


def convert_decimal_state_to_binary(n,num_states):
    if n == 0:
        return "0"
    binary_str = ""
    while n > 0:
        binary_str = str(n % 2) + binary_str  # Append remainder (0 or 1) to the binary string
        n = n // 2  # Update n by dividing it by 2
    preassignment = [int(bit) for bit in binary_str]
    assignment = [0]*(num_states-len(preassignment)) + preassignment

    return assignment

def parse_dimacs(filename):
    """
    Parses a CNF DIMACS file and converts it into a list of clauses.
    
    Parameters:
    filename (str): Path to the CNF DIMACS file.
    
    Returns:
    list of list of int: List of clauses where each clause is a list of literals.
    """
    clauses = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('p cnf'):
                continue  # Skip the problem line
            if line.startswith('c'):
                continue  # Skip comment lines
            if line:
                literals = list(map(int, line.split()))
                if literals[-1] == 0:
                    literals.pop()  # Remove trailing 0
                if literals:
                    clauses.append(literals)
    return clauses

def evaluate_cnf(clauses, assignment):
    """
    Evaluate the CNF formula against the given assignment.
    
    Parameters:
    clauses (list of list of int): List of CNF clauses.
    assignment (list of bool): Boolean assignment to variables.
    
    Returns:
    bool: True if the assignment satisfies the CNF formula, False otherwise.
    """
    def literal_to_value(literal, assignment):
        if literal > 0:
            return assignment[literal - 1]
        else:
            return not assignment[-literal - 1]

    for clause in clauses:
        clause_satisfied = False
        for literal in clause:
            if literal_to_value(literal, assignment):
                clause_satisfied = True
                break
        if not clause_satisfied:
            return False
    return True





def read_file_to_list(filename):
    L = []  # List to store each line as a list of integers
    with open(filename, 'r') as file:
        for line in file:
            # Split the line by spaces and convert each element to an integer
            # Ignore the trailing zero
            clause = [int(x) for x in line.split() if int(x) != 0]
            L.append(clause)
    return L







# Function to run the C program with given arguments and capture the output
def ex5(x1, x2, x3):
    result = subprocess.run(['./a.out', str(x1), str(x2), str(x3)], 
                            capture_output=True, text=True)
    output = result.stdout.strip()
    return output

def ex6(x1, x2, x3, x4 ,x5):
    result = subprocess.run(['./a.out', str(x1), str(x2), str(x3), str(x4), str(x5)], 
                            capture_output=True, text=True)
    output = result.stdout.strip()
    return output


def ex8(x1, x2, r1, r2):
    result = subprocess.run(['./a.out', str(x1), str(x2), str(r1), str(r2)], 
                            capture_output=True, text=True)
    output = result.stdout.strip()
    return output

def ex9(x1, x2, x3, x4, x5, r1, r2, r3, r4):
    result = subprocess.run(['./a.out', str(x1), str(x2), str(x3), str(x4), str(x5), str(r1), str(r2), str(r3), str(r4)], 
                            capture_output=True, text=True)
    output = result.stdout.strip()
    return output


results = []

num_states = 5
subprocess.run(['./cmsgen/build/cmsgen', str('input-cnf')], 
                            capture_output=True, text=True)
filename = 'samples.out'  
L = read_file_to_list(filename)
L = [[0 if x < 0 else 1 for x in clause] for clause in L]
# Run the program 100 times with random inputs
for i in range(100):
    
    r1 = random.randint(0, 1)
    r2 = random.randint(0, 1)
    r3 = random.randint(0, 1)
    r4 = random.randint(0, 1)
    output = ex9(L[i][0], L[i][1], L[i][2], L[i][3], L[i][4], r1, r2, r3, r4)
    '''
    output =  ex5(L[i][0], L[i][1], L[i][2])
    '''
    results.append(output)
    
    element_counts = {}
    
    # Iterate over the multiset
    for element in results:
        # If the element is already in the dictionary, increment its count
        if element in element_counts:
            element_counts[element] += 1
        # Otherwise, add the element to the dictionary with an initial count of 1
        else:
            element_counts[element] = 1
    
    


print("Results from 100 runs:")
print(element_counts)
rev_distance = 0
candidate_file = 'candidate-cnf'
clauses = parse_dimacs(candidate_file) #parsing candidate CNF file
for element in element_counts:
    #print(element)
    assignment =  convert_decimal_state_to_binary(int(element),num_states)
    #print(assignment)
    rev_distance += (evaluate_cnf(clauses,assignment)*element_counts[element])
    #print(rev_distance)

distance = 1 - (rev_distance/100)
print("DistEstimate outputs: ",distance)



