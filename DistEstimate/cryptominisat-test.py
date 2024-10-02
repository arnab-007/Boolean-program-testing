import subprocess


def parse_satisfying_assignment(output):
    lines = output.splitlines()
    #print(lines)
    assignments = list()
    for line in lines:
        if line.startswith('v '):
            # Extract the assignments
            assignments.append(line[2:].split()) # Skip 'v ' at the start
            # Convert to integers and filter out the '0' at the end
    return [item for sublist in assignments for item in sublist if item != '0']
    #return []



def solve_cnf(file_path):
    result = subprocess.run(['cryptominisat5', file_path], capture_output=True, text=True)
    
    
    assignment = parse_satisfying_assignment(result.stdout)
    if (len(assignment) != 0):
        print("SAT")
        print(assignment)
    else: 
        print("UNSAT")
solve_cnf('valid-reachability.cnf')


