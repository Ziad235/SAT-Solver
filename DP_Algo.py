import sys
import random
import copy

# if command line has a file name, read from that file.
# otherwise, read output file created by the frontend program
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    inputfile = "front_output.txt"
dp_input_file = open(inputfile, "r")

clauses = []
keys = {}

# read lines from input file and divide them into S and keys
after0 = False
for i in dp_input_file:
    line = []
    # print(i)
    if i == '0\n':
        after0 = True
        continue
    if after0 == False:
        i = i.rstrip('\n')
        line = i.split(' ')
        clauses.append(line)
    elif after0 == True:
        i = i.rstrip('\n')
        # print(i.split(' ')[0], "::", i.split(' ')[1])
        keys[i.split(' ')[0]] = i.split(' ')[1]

# print(clauses)
# list of all atoms stored by taking the keys of keys dictionary
all_atoms = keys.keys()

# davis putnam algorithm


V = {}
for i in all_atoms:
    V[i] = 'unassigned'

def davis_putnam(atoms, S, V):
    # while there are still easy S to be satisfied
    while (1):

        if S == []:
            # print("S is empty")
            for i in V:
                if V[i] == 'unassigned':
                    V[i] = random.choice(['F', 'T'])
            return V

        elif checkEmptyClause(S):
            # print("empty clause")
            return 'NULL'

        elif isPureLiteral(S, atoms):
            # print("pure literal")
            L = isPureLiteral(S, atoms)
            V = forceAssign(L, V)
            S = doPropogate(L, S, V)

        #   for i in S:
        #     if L in i:
        #       S.remove(i)
            continue

        elif isSingleton(S):
            # print("singleton")
            L = isSingleton(S)
            V = forceAssign(L, V)
            S = doPropogate(L, S, V)
            continue

        else:
            break

  #  Hard cases
    for i in V.keys():
        if V[i] == 'unassigned':
            V[i] = 'T'

            S1 = copy.deepcopy(S)
            V1 = copy.deepcopy(V)
            S1 = doPropogate(i, S1, V1)

            vnew = davis_putnam(atoms, S1, V1)

            if vnew != 'NULL':
                return vnew

            V[i] = 'F'
            S1 = doPropogate('-'+i, S, V)
            return (davis_putnam(atoms, S1, V))


# assign the value of the literal to the variable to make clause true
def forceAssign(atom, V):
    if int(atom) < 0:
        atom = atom.replace('-', '')
        V[atom] = 'F'
    elif int(atom) > 0:
        V[atom] = 'T'
    return V

# Propagate function to remove singelton S, and thus satisfiable S, the negation of pure literals


def doPropogate(atom, S, V):
    deleteCheck = False
    removelist = []
    if atom.count('-') > 0:
        atom = atom.replace('-', '')

    for i in S:
        if (atom in i and V[atom] == 'T') or ('-'+atom in i and V[atom] == 'F'):
            removelist.append(i)
            deleteCheck = True
        elif atom in i and V[atom] == 'F':
            i.remove(atom)
        elif '-'+atom in i and V[atom] == 'T':
            i.remove('-'+atom)

    if deleteCheck:
        for i in removelist:
            S.remove(i)

    return S


def isSingleton(S):
    # print("S: ", S)
    for i in S:
        if len(i) == 1:
            return i[0]
    return False


def isPureLiteral(S, atoms):
    all_literals = []
    # print("S: ", S)
    for i in S:
        for j in i:
            # print("j: ", j)
            all_literals.append(j)

    # print("all_literals: ", all_literals)

    for i in all_atoms:
        if (all_literals.count(i) > 0 and all_literals.count('-' + i) == 0):
            return i
        elif (all_literals.count(i) == 0 and all_literals.count('-' + i) > 0):
            return '-' + i
    return False


def checkEmptyClause(S):
    for i in S:
        if i == []:
            return True


solution = davis_putnam(all_atoms, clauses, V)
# print(solution)

# create list for output to file
outfile = open("dp_output.txt", "w")

if solution != 'NULL':
    for i in solution.keys():
        outfile.write(i + " " + solution[i] + '\n')
else:
    outfile.write("NOSOLUTION\n")
outfile.write('0\n')

for i in keys.keys():
    outfile.write(i + ' ' + keys[i] + '\n')
outfile.close()

f = open("dp_output.txt", "r")
print(f.read())
f.close()
