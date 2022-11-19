import sys

atoms = {}
clauses = []

jumps = []
pegs = []

peglines = []        



# print("Enter filename: ")
filename = input("Enter filename: ")

all_pegs = []

input_file = open(filename, 'r')
line1 = input_file.readline()

time = int(line1.rstrip('\n').split(' ')[0])
empty_start_peg = line1.split(' ')[1].rstrip()

tripleStore = []
for line in input_file:
    if(line=='0\n'):
        break
    line = line.rstrip('\n')
    templine = line.split(' ')
    tripleStore.append(templine)
input_file.close()

for i in tripleStore:
    peglines.append([i[2], i[1], i[0]])
    peglines.append([i[0], i[1], i[2]])
    for j in i:
        if j not in all_pegs:
            all_pegs.append(j)



def createatoms(atoms):
    global jumps, pegs, peglines, all_pegs, time, empty_start_peg
    counter = len(atoms)
    for i in peglines:
        row = []
        for j in range(time-2):
            row.append("Jump("+i[0]+","+i[1]+","+i[2]+","+str(j+1)+")")
            counter+=1
            atoms[row[j]] = str(counter)
        jumps.append(row)

    # set all possible peg atoms in the time frame
    for i in all_pegs:
        row = []
        for j in range(time-1):
            row.append("Peg("+i+","+str(j+1)+")")
            counter+=1
            atoms[row[j]] = str(counter)
        pegs.append(row)

    return atoms

def startaxioms(clauses, atoms):
    global jumps, pegs, peglines, all_pegs, time, empty_start_peg
    #set the starting state 
    cholder = []
    for i in range(len(all_pegs)):
        # print(all_pegs[i], empty_start_peg)
        if all_pegs[i] == empty_start_peg:
            cholder.append("-"+atoms[pegs[i][0]])
            # print("-"+atoms[pegs[i][0]])
        else:
            cholder.append(atoms[pegs[i][0]])    
            # print(atoms[pegs[i][0]])
    clauses.extend(cholder)

    axioms(clauses, atoms)
    return clauses

def axioms(clauses, atoms):
    global jumps, pegs, peglines, all_pegs, time, empty_start_peg
    #precondition axioms
    cholder = []
    
    #causal axioms
    for i in range(len(jumps)):
        for t in range(len(jumps[i])):
            cstring = "-"+atoms[jumps[i][t]] + ' -' + atoms["Peg("+str(peglines[i][0])+","+str(t+2)+')']
            cholder.append(cstring)
            cstring = "-"+atoms[jumps[i][t]] + ' -' + atoms["Peg("+str(peglines[i][1])+","+str(t+2)+')']
            cholder.append(cstring)
            cstring = "-"+atoms[jumps[i][t]] + ' '  + atoms["Peg("+str(peglines[i][2])+","+str(t+2)+')']
            cholder.append(cstring)
    
    for i in range(len(jumps)):
        for t in range(len(jumps[i])):
            cstring = "-"+atoms[jumps[i][t]] + ' ' + atoms["Peg("+str(peglines[i][0])+","+str(t+1)+')']
            cholder.append(cstring)
            cstring = "-"+atoms[jumps[i][t]] + ' ' + atoms["Peg("+str(peglines[i][1])+","+str(t+1)+')']
            cholder.append(cstring)
            cstring = "-"+atoms[jumps[i][t]] + ' -' + atoms["Peg("+str(peglines[i][2])+","+str(t+1)+')']
            cholder.append(cstring)


    #frame axioms
    for i in range(len(pegs)):
        for t in range(len(pegs[i])-1):
            cstring = "-"+atoms[pegs[i][t]]+" "+atoms[pegs[i][t+1]]
            for j in range(len(peglines)):
                if peglines[j][0] == str(i+1) or peglines[j][1] == str(i+1):
                    cstring+=" "+atoms[jumps[j][t]]
            cholder.append(cstring)

    #one action at a time axioms
    for i in range(len(jumps)):
        for j in range(i+1, len(jumps)):
            for t in range(len(jumps[i])):
                cstring = "-"+atoms[jumps[i][t]]+" -"+atoms[jumps[j][t]]
                cholder.append(cstring)

    clauses.extend(cholder)
    endstateaxioms(clauses, atoms)
    return clauses

def endstateaxioms(clauses, atoms):
    global jumps, pegs, peglines, all_pegs, time, empty_start_peg
    #end state axioms
    cholder = []
    for i in range(len(pegs)):
        for j in range(i+1, len(pegs)):
            cstring = "-" + atoms[pegs[i][time-2]] + " -" + atoms[pegs[j][time-2]]
            cholder.append(cstring)

    cstring = ''
    for i in range(len(pegs)):
        cstring += atoms[pegs[i][time-2]] + " "
    cstring = cstring.rstrip()
    cholder.append(cstring)

    clauses.extend(cholder)
    return clauses

allatoms = createatoms(atoms)
allclauses = startaxioms(clauses, atoms)

outfile = open("front_output.txt", "w")
for i in allclauses:
    outfile.write(i.rstrip(" ")+'\n')

outfile.write('0\n')

for i in allatoms:
    outfile.write(atoms[i] + " " + i+'\n')

outfile.close()

f = open("front_output.txt", "r")
print(f.read())
f.close()