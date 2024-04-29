def generate_init_DIMACS_formula(formula, variable_mapping):
    dimacs_formula = []
    clauses = formula.split('&&')
    
    for clause in clauses:
        literals = clause.split('||')
        
        dimacs_clause = []
        literals = [literal.strip("() ") for literal in literals]
        # Filter out empty strings
        literals = list(filter(None, literals))
        
        
        for literal in literals:
            
            if literal.startswith('!'):
                dimacs_clause.append(-variable_mapping[literal[1:]+'_1'])
            else:
                dimacs_clause.append(variable_mapping[literal+'_1'])
        
        dimacs_formula.append(dimacs_clause)
    
    num_variables = len(variable_mapping)
    num_clauses = len(dimacs_formula)
    
    dimacs_str = f"p cnf {num_variables} {num_clauses}\n"
    
    
    for clause in dimacs_formula:
        dimacs_str += ' '.join(str(i) for i in clause) + ' 0\n'
    
    return dimacs_formula , dimacs_str

def generate_final_DIMACS_formula(formula, variable_mapping,updates):
    dimacs_formula = []
    clauses = formula.split('&&')
    
    for clause in clauses:
        literals = clause.split('||')
        
        dimacs_clause = []
        literals = [literal.strip("() ") for literal in literals]
        # Filter out empty strings
        literals = list(filter(None, literals))
        
        
        for literal in literals:
            
            if literal.startswith('!'):
                dimacs_clause.append(-variable_mapping[literal[1:]+'_'+str(1+updates[literal[1:]])])
            else:
                dimacs_clause.append(variable_mapping[literal+'_'+str(1+updates[literal])])
        
        dimacs_formula.append(dimacs_clause)
    
    num_variables = len(variable_mapping)
    num_clauses = len(dimacs_formula)
    
    dimacs_str = f"p cnf {num_variables} {num_clauses}\n"
    
    
    for clause in dimacs_formula:
        dimacs_str += ' '.join(str(i) for i in clause) + ' 0\n'
    
    return dimacs_formula , dimacs_str