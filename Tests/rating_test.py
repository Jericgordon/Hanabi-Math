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

        r5 = Rating(index,4,5)
        r6 = Rating(index,3,5)
        self.assertLess(r6,r5)

        r3 = Rating(index,2,5)
        r4 = Rating(index,2,4)
        self.assertLess(r4,r3)
        
        r7 = Rating(index,4,5)
        r8 = Rating(index,4,4)
        self.assertLess(r8,r7)

    def test_equal(self):
        index = 2
        r1 = Rating(index,1,5)
        r2 = Rating(index,1,5)
        self.assertAlmostEqual(r1,r2)
