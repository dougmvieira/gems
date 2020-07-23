""" Futures and generators

How can you delay a function execution? You can use a singleton generator. This
is useful for parallel programming so that you submit multiple jobs (e.g. to a
cluster) and lazily obtain the results. This pattern makes the code more
modular.

"""
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import chain


def lazy_eval(executor, compute, *args):
    future = executor.submit(compute, *args)
    return (f() for f in [future.result])


def f(x):
    time.sleep(1)
    return x


start = time.time()

with ThreadPoolExecutor(max_workers=4) as executor:
    results = (lazy_eval(executor, f, x) for x in ['foo', 'bar', 'baz'])
    for result in chain(*results):
        print(result)

end = time.time()

print(f'Time elapsed: {end - start} seconds.')
