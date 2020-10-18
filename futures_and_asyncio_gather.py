""" Futures and `asyncio.gather`

This is the `asyncio` version of the "Futures and generators" code. The
`asyncio.gather` function accepts `asyncio.Future`s and coroutines, but not
`concurrent.futures.Future`, which is returned by `Executor.submit`. We
therefore need to use low-level API `EventLoop.run_in_executor` instead. I
believe this code is most useful when the remaining of the code already uses
`asyncio`, otherwise I would favour the singleton generators pattern because it
has less boilerplate.

"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import chain


async def lazy_eval(executor, compute, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, compute, *args)


async def submit_and_join(compute, args_lst):
    with ThreadPoolExecutor(max_workers=4) as executor:
        coros = (lazy_eval(executor, compute, *args) for args in args_lst)
        results = await asyncio.gather(*coros)
    return results


def f(x):
    time.sleep(1)
    return x


start = time.time()

results = asyncio.run(submit_and_join(f, [('foo',), ('bar',), ('baz',)]))
for result in results:
     print(result)

end = time.time()

print(f'Time elapsed: {end - start} seconds.')
