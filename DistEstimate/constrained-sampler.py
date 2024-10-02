import z3
import random

def cnf_to_z3(clauses, num_vars):
    """
    Convert CNF formula to Z3 format.
    """
    solver = z3.Solver()  # Use z3.Solver() directly
    variables = [z3.Bool(f"x{i+1}") for i in range(num_vars)]  # Create Boolean variables

    # Add the CNF clauses to the Z3 solver
    for clause in clauses:
        z3_clause = []
        for lit in clause:
            if lit > 0:
                z3_clause.append(variables[lit - 1])  # Positive literal
            else:
                z3_clause.append(z3.Not(variables[-lit - 1]))  # Negative literal
        solver.add(z3.Or(*z3_clause))  # Add the clause as a disjunction (OR)
    
    return solver, variables

def find_satisfying_assignments(solver, variables):
    """
    Find all satisfying assignments using Z3.
    """
    assignments = []
    while solver.check() == z3.sat:  # Check if the formula is satisfiable
        model = solver.model()  # Get the current model (assignment)
        solution = [(v() if model[v] else -v()) for v in variables]
        assignments.append(solution)

        # Add a blocking clause to avoid finding the same solution again
        blocking_clause = z3.Or([z3.Not(var) if model[var] else var for var in variables])
        solver.add(blocking_clause)
    
    return assignments

def uniformly_sample_satisfying_assignment(assignments):
    """
    Uniformly sample a satisfying assignment.
    """
    if assignments:
        return random.choice(assignments)
    else:
        return None

# Example CNF formula (x1 || x2) && (!x1 || x3)
cnf_clauses = [[1, 2], [-1, 3]]
num_vars = 3

# Convert CNF to Z3 and find assignments
solver, variables = cnf_to_z3(cnf_clauses, num_vars)
satisfying_assignments = find_satisfying_assignments(solver, variables)

if satisfying_assignments:
    print("All Satisfying Assignments:")
    for assignment in satisfying_assignments:
        print(assignment)

    # Sample one uniformly
    sampled_assignment = uniformly_sample_satisfying_assignment(satisfying_assignments)
    print("\nSampled Satisfying Assignment:")
    print(sampled_assignment)
else:
    print("No satisfying assignments found.")

