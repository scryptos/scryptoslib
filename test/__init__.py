from __future__ import division, absolute_import, generators, print_function
from .test_util import *
from .test_math import *
from .test_rsa import *
from .test_knapsack import *
from .test_prng import *
from .test_rc4 import *
from .test_tls import *


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestHexUtil))
    suite.addTests(unittest.makeSuite(TestStringUtil))
    suite.addTests(unittest.makeSuite(TestNum))
    suite.addTests(unittest.makeSuite(TestContfrac))
    suite.addTests(unittest.makeSuite(TestVector))
    suite.addTests(unittest.makeSuite(TestRSA))
    suite.addTests(unittest.makeSuite(TestKnapsack))
    suite.addTests(unittest.makeSuite(TestLattice))
    suite.addTests(unittest.makeSuite(TestMT19937))
    suite.addTests(unittest.makeSuite(TestLCG))
    suite.addTests(unittest.makeSuite(TestRC4))
    suite.addTests(unittest.makeSuite(TestTLS))
    return suite
