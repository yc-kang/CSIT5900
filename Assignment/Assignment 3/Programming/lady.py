from z3 import *

# Define boolean variables for the presence of a lady in each room
lady_in_room1, lady_in_room2, lady_in_room3 = Bool('lady_in_room1'), Bool('lady_in_room2'), Bool('lady_in_room3')
solver = Solver()

# Constraint: Exactly one room contains a lady
solver.add(Or(And(lady_in_room1, Not(lady_in_room2), Not(lady_in_room3)),
              And(Not(lady_in_room1), lady_in_room2, Not(lady_in_room3)),
              And(Not(lady_in_room1), Not(lady_in_room2), lady_in_room3)))

# Constraints for the signs: At most one sign is true
sign1 = Not(lady_in_room1)
sign2 = lady_in_room2
sign3 = Not(lady_in_room2)
solver.add(Or(And(Not(sign1), Not(sign2), Not(sign3)),
              And(Not(sign1), Not(sign2), sign3),
              And(Not(sign1), sign2, Not(sign3)),
              And(sign1, Not(sign2), Not(sign3))))

# Check the satisfiability and print the model
print(solver.check())
print(solver.model())  # Expected output: [lady_in_room3 = False, lady_in_room1 = True, lady_in_room2 = False]

# Adding the negation of the solution to check for unsatisfiability
solver.add(Not(lady_in_room1))
print(solver.check())  # Expected output: unsat