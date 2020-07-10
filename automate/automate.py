with open('input.txt', 'r') as t:
    passedfile = open('passedfile.txt', 'w')
    failedfile = open('failedfile.txt','w')
    # print(t.read())
    for line in t:
        line_split = line.split()
        if line_split[2] == 'P':
            passedfile.write(line)
        else:
            failedfile.write(line)
passedfile.close()
failedfile.close()
t.close()
