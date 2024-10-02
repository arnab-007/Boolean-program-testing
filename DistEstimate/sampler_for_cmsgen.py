import os 
import json
PATH = os.path.realpath("")
assumed_shape = " "



"""
[get_config] loads the json object in [progname]'s configuration file
"""
def get_config(progname):
    with open(os.path.join(PATH, "candidate_files", progname + ".json"), "r") as f:
        config = json.load(f)
    return config

def cnf_to_dimacs(cnf_formula, variable_mapping):
    dimacs = []
    for clause in cnf_formula:
        dimacs_clause = []
        for literal in clause:
            if literal.startswith('!'):
                dimacs_clause.append(-variable_mapping[literal[1:]])
            else:
                dimacs_clause.append(variable_mapping[literal])
        dimacs.append(dimacs_clause)
    return dimacs




with open(os.path.join(PATH, "program-list.txt"), "r") as f:
    prognames = f.read().strip().split("\n")

results = {}
for progname in prognames:
    config = get_config(progname)
    prog_variables = config["Program_variables"]["Bools"]
    cand = config["Candidate"]["Expression"]
    init_states = config["Initial states"]["Expression"]


init_list_clauses = init_states.split('&&')
#print(cand_list_clauses)
init_list = list()
for clause in init_list_clauses:

    literals = clause.split('||')
    literals = [literal.strip("() ") for literal in literals]
    # Filter out empty strings
    literals = list(filter(None, literals))
    init_list.append(literals)

print(init_list)
    
cand_list_clauses = cand.split('&&')
#print(cand_list_clauses)
cand_list = list()
for clause in cand_list_clauses:

    literals = clause.split('||')
    literals = [literal.strip("() ") for literal in literals]
    # Filter out empty strings
    literals = list(filter(None, literals))
    cand_list.append(literals)

print(cand_list)



# Example CNF formula
cnf_formula_cand = cand_list
cnf_formula_init = init_list
# Variable mapping (manual assignment of variables to integers)
variable_mapping = {'x1': 1, 'x2': 2, 'x3': 3, 'x4': 4, 'x5': 5}

# Convert to DIMACS format
dimacs_cand = cnf_to_dimacs(cnf_formula_cand, variable_mapping)
dimacs_init = cnf_to_dimacs(cnf_formula_init, variable_mapping)

def write_dimacs_to_file(dimacs, num_vars, num_clauses, file_name):
    with open(file_name, 'w') as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in dimacs:
            f.write(" ".join(map(str, clause)) + " 0\n")

# Write DIMACS formula to file
num_vars = len(variable_mapping)  # Number of variables
num_clauses = len(dimacs_cand)  # Number of clauses
write_dimacs_to_file(dimacs_cand, num_vars, num_clauses, 'candidate-cnf')
write_dimacs_to_file(dimacs_init, num_vars, num_clauses, 'input-cnf')



import subprocess

# Path to your bash script
script_path = './cmsgen-sampler.sh'

# Run the bash script
result = subprocess.run([script_path], capture_output=True, text=True)


# Define the variable mapping
variable_mapping = {1: 'x1', 2: 'x2', 3: 'x3', 4: 'x4', 5: 'x5'}





def convert_sample(sample_line):
    # Split the line into tokens
    tokens = sample_line.split()
    # Initialize an empty list to hold the formatted variables
    formatted_vars = []
    
    for token in tokens:
        num = int(token)
        if num != 0:
            if num > 0:
                var_name = variable_mapping.get(num)
                if var_name:
                    formatted_vars.append(f"{var_name}")
            else:
                var_name = variable_mapping.get(-num)
                if var_name:
                    formatted_vars.append(f"!{var_name}")
    
    return " && ".join(formatted_vars)

# Read the input file and convert the content
with open('samples.out', 'r') as file:
    lines = file.readlines()

converted_lines = [convert_sample(line) for line in lines]


# Write the converted content to a new file
with open('samples_converted.txt', 'w') as file:
    file.write("\n".join(converted_lines))




