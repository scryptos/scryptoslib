from test_util import *
from test_math import *
from test_rsa  import *
from test_knapsack import *

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
  return suite

