from time import perf_counter

"""
This function simply calls the passed in function and prints the time it takes to execute it.
The passed function in should be a lambda.
"""


def benchmarkWrapper(func):
    tic = perf_counter()
    output = func()
    toc = perf_counter()
    print(
        f"BENCHMARK =========> Buffer rating took: {round(toc-tic, 3)} seconds")
    return output
