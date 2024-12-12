from rating import Rating
import unittest

# Categories of usefullness: 
        # 1. Useless: If we've already played it, we don't care
        # 2. Other; how we recon this is the difference between strategies
            # 1. We can discard the highest card,
            # 2. We can discard the highest chain card
        # 3. Essential: It's a 5, or we've discarded it before

class Rating_tests(unittest.TestCase):
    def test_greater_than(self):
        index = 3
        r1 = Rating(index,1,5)
        r2 = Rating(index,2,5)
        self.assertLess(r1,r2)

        r3 = Rating(index,2,5)
        r4 = Rating(index,2,4) # the lower second value is greater
        self.assertLess(r3,r4)

        r5 = Rating(index,3,0)
        r6 = Rating(index,3,1)
        self.assertLess(r6,r5)

    def test_equal(self):
        index = 2
        r1 = Rating(index,1,5)
        r2 = Rating(index,1,5)
        self.assertAlmostEqual(r1,r2)