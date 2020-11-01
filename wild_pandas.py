""" Wild pandas

Pandas is a really nice tool for fast exploratory data analysis. However, with
power comes great responsibility. Pandas sometimes has some unexpected
behaviour in corner cases. Here we investigate the undesired effects of some
automatic type casts.

"""
from hashlib import blake2b

import pandas as pd
import numpy as np


def uint64_hash(x):
    return np.uint64(int(blake2b(bytes(x), digest_size=8).hexdigest(), 16))


def example1():
    df1 = pd.DataFrame(dict(foo=range(5), bar=[uint64_hash(i) for i in range(5)]))
    df2 = pd.DataFrame(dict(foo=[-1]))

    df3 = pd.merge(df1, df2, 'outer', 'foo')
    # This merge adds a NaN on the `bar` column

    assert (df1.bar == df3.bar.loc[df1.index]).all()  # So far so good

    assert df1.bar.dtype == np.uint64
    assert df3.bar.dtype == np.float64
    # pandas has casted uint64 into float64! The reason for this is that NaN is
    # actually a float64.

    assert not (df1.bar == df3.bar.loc[df1.index].astype(np.uint64)).any()
    # casting float64 back to uint64 breaks equality

    assert not pd.merge(df1, df1, 'inner', 'bar').empty
    assert pd.merge(df1, df3, 'inner', 'bar').empty
    # Even though df3.bar is just df1.bar with an added NaN, the merge has
    # completely failed


def example2():
    df1 = pd.DataFrame(dict(foo=range(5), bar=[uint64_hash(i) for i in range(5)]))
    df2 = pd.DataFrame(dict(foo=[-1]))

    df1 = df1.astype(dict(bar='UInt64'))
    # To prevent casting to float64 upon a NaN value, we set `bar` to be a
    # nullable integer. We're now safe, right?

    df3 = pd.merge(df1, df2, 'outer', 'foo')
    # This merge now adds a uint64 pd.NA on the `bar` column

    assert (df1.bar == df3.bar.loc[df1.index].astype(np.uint64)).all()
    assert not pd.merge(df1, df3, 'inner', 'bar').empty
    # OK, problem solved! Or is it?

    df4 = df1.groupby('foo', as_index=False).first()
    assert df1.bar.dtype == df4.bar.dtype
    assert (df1.foo == df4.foo).all()
    assert not (df1.bar == df4.bar).all()
    # Wait, what? The values of df1.bar were corrupted after the group-by
    # operation

    df5 = df1.groupby('bar', as_index=False).sum()
    assert df5.bar.dtype == np.uint64
    # Ohno, the group-by operation changed our type again...

    df6 = pd.merge(df5, df2, 'outer', 'foo')
    try:
        pd.merge(df1, df6, 'inner', 'bar')
        assert False
    except TypeError:
        pass
    # Wow

    assert pd.merge(df1.astype(dict(bar=np.uint64)), df6, 'inner', 'bar').empty
    # Merging with df6 now fails, even though it worked for df3! We have become
    # unprotected again against casting to float64 due a NaN.


example1()
example2()
