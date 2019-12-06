#!/usr/bin/env python3
"""Utility functions"""

import torch.nn.functional as F


def one_hot_float(id_tensor, num_classes):
    """Create a one-hot float tensor from a tensor of indices

    torch.nn.functional.one_hot returns a LongTensor, but to enable easier
    multiplication with embedding matrices, this version converts to float.
    """
    return F.one_hot(id_tensor, num_classes).float()
