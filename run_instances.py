# Script to solve the 1-D bin packing instances from OR-Library 
# utilizing the algorithms implemented in binp.py file.
from binp import *
import os
import functools
import time

INSTANCE_PATH = os.path.join(os.curdir, "instances")

INSTANCE_FILES = ["binpack1.txt", "binpack2.txt", "binpack3.txt"
                  ,"binpack4.txt", "binpack5.txt", "binpack6.txt"
                  ,"binpack7.txt", "binpack8.txt"]

def timed(f):
    """This function is used as a decorator to measure time spent by each algorithm"""
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        start = time.clock()
        result = f(*args, **kwds)
        end = time.clock()
        elapsed = "%.2f" % (end - start)
        return elapsed, result
    return wrapper

def execute_exp():
    """Execution of the experiment reading the OR-Library instances and running them with
    all implemented algorithms"""
    for instance_file in INSTANCE_FILES:
        instances = ORLibraryInstanceReader.get_instances(os.path.join(INSTANCE_PATH, instance_file))
        run_first_fit_with(instances)
        run_descending_first_fit_with(instances)

def run_first_fit_with(instances):
    """Execution of each instance with First Fit algorithm"""
    for instance in instances:
        constructor = FirstFitConstructor(instance)
        time_elapsed, solution = solve_instance(constructor)
        print(generate_result_string(instance, solution, time_elapsed))

def run_descending_first_fit_with(instances):
    """Execution of each instance with Descending First Fit algorithm"""
    for instance in instances:
        constructor = DescendingFirstFitConstructor(instance)
        time_elapsed, solution = solve_instance(constructor)
        print(generate_result_string(instance, solution, time_elapsed))

@timed
def solve_instance(constructor):
    """It simply calls the generate_solution() method. Defined in a function to be timed alone."""
    return constructor.generate_solution()

def generate_result_string(instance, solution, time_elapsed):
    """Returns a string representing the results of a algorithm.
    It is in format: instance_name boxes_in_solution boxes_in_best_known_solution time_spent"""
    return "{0}\t{1}\t{2}\t{3}".format(instance.instance_name, len(solution.boxes), 
                                       instance.best_known_sol, time_elapsed)

if __name__ == "__main__":
    execute_exp()