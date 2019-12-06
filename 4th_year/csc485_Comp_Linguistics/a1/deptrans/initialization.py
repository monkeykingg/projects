#!/usr/bin/env python3
"""Initialization functions"""

import torch


def he_initializer(shape, **kwargs):
    """Defines an initializer for the He initialization distribution.

    This function will be used as a variable initializer: it takes in a shape
    (tuple or 1-d array) and returns a random tensor of the specified shape
    drawn from the He initialization distribution.
    Specifically, the output should be sampled from a Gaussian distribution
    with mean 0 and standard deviation std = sqrt(2 / number of input units)
    e.g., if shape = (10, 20), sigma = sqrt(2 / 10)

    Args:
        shape:
            Tuple or 1-d array that species the dimensions of the requested
            tensor.
    Returns:
        out:
            torch.Tensor of specified shape sampled from the He distribution.

    Hint: You might find torch.normal() useful.
    """
    # *** BEGIN YOUR CODE ***
    sigma = torch.sqrt(torch.tensor(2.) / torch.tensor(shape[0]))
    out = torch.normal(0, sigma, size=shape)
    # *** END YOUR CODE ***
    return out


def test_initialization_basic():
    """Some simple tests for the initialization.
    """
    print("Running basic tests...")
    shape = (1,)
    he_mat = he_initializer(shape)
    assert he_mat.size() == shape

    shape = (1, 2, 3)
    he_mat = he_initializer(shape)
    assert he_mat.size() == shape
    print("Basic (non-exhaustive) He initialization tests pass")


if __name__ == "__main__":
    test_initialization_basic()
