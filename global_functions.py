directory = ""

#def setDirectory(directory_path):
#	directory = directory_path

def createFile(filename):
	file_pointer = open(directory + filename, 'w')
	
	return file_pointer

def openFile(filename):
	file_pointer = open(directory + filename, "r")
	
	return file_pointer
	
def closeFile(file_pointer):
	file_pointer.close()
	
	return True

def eraseFile(filename):
	file_pointer = createFile(filename)
	closeFile(file_pointer)
	
	return True
	
def readLineFromFile(file_pointer):
	return file_pointer.read().split(";")[:-1] #TO REMOVE EMPTY ENTRY

def readFromFile(file_pointer):
	result = []
	
	for line in file_pointer:
		result.append(line.split('\n')[0])
	
	return result

def writeToFile(file_pointer, data):
	file_pointer.write(data + "\n")

	return True

def addToFile(filename, data):
	file_pointer = open(directory + filename, 'a')
	file_pointer.write(data)
	file_pointer.close()
	
	return True

def addToFileWithBreakline(filename, data):
	file_pointer = open(directory + filename, 'a')
	file_pointer.write(data + "\n")
	file_pointer.close()
