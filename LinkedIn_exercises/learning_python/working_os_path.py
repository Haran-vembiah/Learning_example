import datetime
import os

# print the name of the OS
import time

print(os.name)

# Check for existence and type
print("Item exists: " + str(os.path.exists("textfile.txt")))
print("Item is a file: " + str(os.path.isfile("textfile.txt")))
print("Item is a directory: " + str(os.path.isdir("textfile.txt")))

# work with file paths
print("Item path: " + str(os.path.realpath("textfile.txt")))
print("Item path and filename: " + str(os.path.split(os.path.realpath("textfile.txt"))))

# Get the modification time of file
t = time.ctime(os.path.getmtime("textfile.txt"))
print(t)
print(datetime.datetime.fromtimestamp(os.path.getmtime("textfile.txt")))

# calculate how long ago the item was modified
td = datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime("textfile.txt"))
print("It has been " + str(td) + "since the file was modified")
