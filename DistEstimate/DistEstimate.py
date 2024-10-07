import subprocess
import random
import re
import os
import json
PATH = os.path.realpath("")
assumed_shape = " "


def get_config(progname):
    with open(os.path.join(PATH, "candidate_files", progname + ".json"), "r") as f:
        config = json.load(f)
    return config

def convert_decimal_state_to_binary(n,num_states):
    if n == 0:
        return "0"
    binary_str = ""
    while n > 0:
        binary_str = str(n % 2) + binary_str  
        n = n // 2 
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
    L = []  
    with open(filename, 'r') as file:
        for line in file:
            
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

def ex10(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, r1, r2, r3, r4, r5, r6, r7):
    result = subprocess.run(['./a.out', str(x1), str(x2), str(x3), str(x4), str(x5), str(x6), str(x7), str(x8), str(x9), str(x10), str(x11), str(x12), str(x13), str(x14), str(x15), str(x16), str(x17), str(r1), str(r2), str(r3), str(r4), str(r5), str(r6), str(r7)], 
                            capture_output=True, text=True)
    output = result.stdout.strip()
    return output


results = []

num_states = 5
with open(os.path.join(PATH, "program-list.txt"), "r") as f:
    prognames = f.read().strip().split("\n")


for progname in prognames:
    config = get_config(progname)
    prog_variables = config["Program_variables"]["Bools"]
    cand = config["Candidate"]["Expression"]
    init_states = config["Initial states"]["Expression"]
    k = config["Number of iterations"]["while"]
    rand = config["Random_variables"]["Bools"]

    print(rand)
'''
command = ['./cmsgen/build/cmsgen', '--samples=500', '--samplefile=samples.out', 'input-cnf']
result = subprocess.run(command, check=True, capture_output=True, text=True)
'''
filename = 'samples.out'  
L = read_file_to_list(filename)
L = [[0 if x < 0 else 1 for x in state] for state in L]
violating_init_states = list()
element_counts = {}
print(len(L))
#print(k)
# Run the program 10000 times with random inputs
for p in range(len(L)):
    L1 = L[p]
    #print(L1)
    for q in range(10):
        for r in range(k):
            
            r1 = random.randint(0, 1)
            r2 = random.randint(0, 1)
            r3 = random.randint(0, 1)
            r4 = random.randint(0, 1)
            output = ex9(L1[0], L1[1], L1[2], L1[3], L1[4], r1, r2, r3, r4)
            #print("Output: ",output)
            
            
            L1 = [int(bit) for bit in bin(int(output))[2:].zfill(5)]
        
        
        results.append(output)
        
        element_counts = {}
        
        
        L1 = L[p]
    for element in results:
            
        if element in element_counts:
            element_counts[element] += 1
            
        else:
            element_counts[element] = 1
    
    #print(L[p])
    #print(element_counts)


print("Results from 600 runs:")
print(element_counts)
rev_distance = 0
candidate_file = 'candidate-cnf'
counterexamples = list()
clauses = parse_dimacs(candidate_file) #parsing candidate CNF file
for element in element_counts:
    #print(element)
    assignment =  convert_decimal_state_to_binary(int(element),num_states)
    #print(assignment)
    ind_distance = evaluate_cnf(clauses,assignment)*element_counts[element]
    rev_distance += ind_distance
    #print(rev_distance)
    if (ind_distance == 0):
        counterexamples.append(element)

distance = 1 - (rev_distance/(len(L)*10))
print("DistEstimate outputs: ",distance)


counterexamples_dict = {}

for element in counterexamples:
    counterexamples_dict[element] = element_counts[element]/(len(L)*10)

print("Set of counterexamples: ",counterexamples_dict)

input_dict = {"progname":progname,"candidate":cand,"init_states":init_states,"iterations":k}
output_dict = {"Reachability_dict":element_counts,"DistEstimate_value":distance,"counterexamples":counterexamples_dict}

total_dict = {"input_dict":input_dict,"output_dict":output_dict}

'''
counterexamples_file = 'Experimental results/Job_01'

with open(counterexamples_file, 'w') as file:
    file.write("Inputs: \n")
    file.write("Set of counterexamples\n")
    file.write("State : probability of violation\n")
    for counterexample in counterexamples:
        file.write(f"{counterexample}\n") 

'''
results_directory = os.path.join(os.getcwd(), 'DistEstimate_results')
if not os.path.exists(results_directory):
    os.makedirs(results_directory)



existing_files = os.listdir(results_directory)
file_number = 1

# Loop until you find an unused file name (exp1.json, exp2.json, etc.)
while f"exp{file_number}.json" in existing_files:
    file_number += 1

# Create the new filename in the results subdirectory
filename = os.path.join(results_directory, f"exp{file_number}.json")

# Write the data to the new file
with open(filename, 'w') as json_file:
    json.dump(total_dict, json_file, indent=4)




