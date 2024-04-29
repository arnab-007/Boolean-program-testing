This repository contains (as of April 29th, '24) the driver code to verify whether a given candidate formula F, for a Boolean program, indeed satisfies the invariant property. The bash script driver.sh currently contains the instructions to verify, for the program file ex6.c, the candidate formula that has been provided via the configuration file ex6.json, residing in the folder /candidate_files.

Running the command ./driver.sh will output whether the given formula F is indeed an invariant for the program, ex6.c here for instance. If the tool outputs "UNSATISFIABLE", the formula F is indeed an invariant. Otherwise, the verifier tool outputs "SATISFIABLE" and generates a counterexample trace which makes the formula F violate the invariant property.
