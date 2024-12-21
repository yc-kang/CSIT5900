from z3 import *

# Define boolean variables for the ranks of each person
lisa_ranks = [Bool(f'Lisa Rank {i}') for i in range(1, 5)]
bob_ranks = [Bool(f'Bob Rank {i}') for i in range(1, 5)]
jim_ranks = [Bool(f'Jim Rank {i}') for i in range(1, 5)]
mary_ranks = [Bool(f'Mary Rank {i}') for i in range(1, 5)]

solver = Solver()

# Constraints: Each person can only have one rank
for ranks in [lisa_ranks, bob_ranks, jim_ranks, mary_ranks]:
    solver.add(Sum([If(rank, 1, 0) for rank in ranks]) == 1)

# Constraints: Each rank can only be assigned to one person
for i in range(4):
    solver.add(Sum([If(ranks[i], 1, 0) for ranks in [lisa_ranks, bob_ranks, jim_ranks, mary_ranks]]) == 1)

# Define boolean variables for majors
lisa_bio_major = Bool('Lisa is a biology major')
mary_bio_major = Bool('Mary is a biology major')

# Fact 1: Lisa and Bob cannot have consecutive ranks
solver.add(Not(And(lisa_ranks[0], bob_ranks[1])), Not(And(bob_ranks[0], lisa_ranks[1])),
           Not(And(lisa_ranks[1], bob_ranks[2])), Not(And(bob_ranks[1], lisa_ranks[2])),
           Not(And(lisa_ranks[2], bob_ranks[3])), Not(And(bob_ranks[2], lisa_ranks[3])))

# Fact 2: If Lisa is a biology major, Jim's rank is one less than Lisa's
solver.add(Implies(lisa_bio_major, Or(And(jim_ranks[0], lisa_ranks[1]), And(jim_ranks[1], lisa_ranks[2]), And(jim_ranks[2], lisa_ranks[3]))))
solver.add(Implies(mary_bio_major, Or(And(jim_ranks[0], mary_ranks[1]), And(jim_ranks[1], mary_ranks[2]), And(jim_ranks[2], mary_ranks[3]))))

# Fact 3: Bob's rank is one less than Jim's
solver.add(Or(And(bob_ranks[0], jim_ranks[1]), And(bob_ranks[1], jim_ranks[2]), And(bob_ranks[2], jim_ranks[3])))

# Fact 4: Either Lisa or Mary is a biology major, but not both
solver.add(Or(And(lisa_bio_major, Not(mary_bio_major)), And(Not(lisa_bio_major), mary_bio_major)))

# Fact 5: Either Lisa or Mary is ranked first
solver.add(Or(lisa_ranks[0], mary_ranks[0]))

# Check the satisfiability and print the model
print(solver.check())
model = solver.model()
[print(var, '= True') for var in model.decls() if model[var] == True]

# The answer is (Mary, Bob, Jim, Lisa)