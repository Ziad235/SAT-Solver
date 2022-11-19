back_input_file = open("dp_output.txt", "r")

solution = []
keys = {}

after0 = False
for i in back_input_file:
    line = []
    # print(i)
    if i == 'NOSOLUTION\n':
      print("No solution")
      outfile = open("back_output.txt", "w")
      outfile.write("NO SOLUTION")
      outfile.close()
      exit()

    if i == '0\n':
        after0 = True
        continue
    if after0 == False:
        i = i.rstrip('\n')
        line = i.split(' ')
        solution.append(line)
    elif after0 == True:
        i = i.rstrip('\n')
        # print(i.split(' ')[0], "::", i.split(' ')[1])
        keys[i.split(' ')[0]] = i.split(' ')[1]

back_input_file.close()

# print(solution)
# print(keys)

outfile = open("back_output.txt", "w")

for i in keys.keys():
  if "jump" in keys[i].lower():
    for j in solution:
        if i == j[0] and j[1] == 'T':
            outfile.write(keys[i] + '\n')

outfile.close()

f = open("back_output.txt", "r")
print(f.read())
f.close()
        