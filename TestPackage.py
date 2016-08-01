import unittest
import doctest

import Wert
import Ranking
import Ranker


suite = unittest.TestSuite()
for mod in Wert, Ranking, Ranker:
    suite.addTest(doctest.DocTestSuite(mod))
runner = unittest.TextTestRunner()
runner.run(suite)

print("Test completed - Starting Application")