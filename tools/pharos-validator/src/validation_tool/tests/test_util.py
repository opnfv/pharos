#!/usr/bin/env python3

import random

def test_approxsize():
    from pharosvalidator.util import approxsize
    assert approxsize(100, 95, 5) == True
    assert approxsize(100, 105, 5) == True

    assert approxsize(100, 94, 5) == False
    assert approxsize(100, 106, 5) == False

