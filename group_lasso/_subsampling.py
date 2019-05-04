import numpy as np


def _extract_from_singleton_iterable(inputs):
    if len(inputs) == 1:
        return inputs[0]
    return tuple(inputs)


def _random_row_idxes(num_rows, subsampling_scheme):
    if subsampling_scheme == 1:
        return range(num_rows)
    elif (
        isinstance(subsampling_scheme, str) and
        subsampling_scheme.lower() == 'sqrt'
    ):
        num_subsampled_rows = int(np.sqrt(num_rows))
    elif subsampling_scheme < 1:
        num_subsampled_rows = int(num_rows*subsampling_scheme)
    elif subsampling_scheme > 1 and isinstance(subsampling_scheme, int):
        assert subsampling_scheme < num_rows
        num_subsampled_rows = subsampling_scheme
    else:
        raise ValueError('Not valid subsampling scheme')

    inds = np.random.choice(num_rows, num_subsampled_rows, replace=False)
    inds.sort()
    return inds


def subsampling_fraction(num_rows, subsampling_scheme):
    return len(_random_row_idxes(num_rows, subsampling_scheme))/num_rows


def subsample(subsampling_scheme, *Xs):
    """Subsample along first (0-th) axis of the Xs arrays.

    Arguments
    ---------
    subsampling_scheme : int, float or str
        How to subsample:
         * int or float == 1 -> no subsampling
         * int > 1 -> that many rows are sampled
         * float < 1 -> the fraction of rows to subsample
         * sqrt -> subsample sqrt(num_rows) rows

    """
    assert len(Xs) > 0
    if subsampling_scheme == 1:
        return _extract_from_singleton_iterable(Xs)

    num_rows = len(Xs[0])
    inds = _random_row_idxes(num_rows, subsampling_scheme)
    return _extract_from_singleton_iterable([X[inds, :] for X in Xs])