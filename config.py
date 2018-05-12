LIMIT_OF_INDIVIDUALS = 200
SLEEP_TIME_CONSUMER = 5 #in seconds
SLEEP_TIME_PRODUCER = 30 #in seconds
number_of_generations = 100 #number of generations
number_of_individuals = 100 #number of indivduals
number_of_games_per_worker = 1 #number of games a worker will play for single run through for a single game
number_of_simulations = 100 #number of games each indiv will play


from mpi4py import MPI

def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


# Initializations and preliminaries
comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object

# Define MPI message tags
tags = enum('READY', 'DONE', 'EXIT', 'START', 'SLEEP')
