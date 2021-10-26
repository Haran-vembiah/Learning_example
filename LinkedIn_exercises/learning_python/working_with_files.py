# open a file for writing and create it if doesn't exist
f = open("textfile.txt", "w+")

# Open the file to append data at end
f = open("textfile.txt", "a")

# open to read the file
f = open("textfile.txt", "r")
# read() and readLines() to get the data from the file.

# write some lines of data to the file
for i in range(10):
    f.write("This is the line " + str(i) + "\r\n")

f.close()
