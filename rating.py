
# Categories of usefullness: 
        # 1. Useless: If we've already played it, we don't care
        # 2. Other; how we recon this is the difference between strategies
            # 1. We can discard the highest card,
            # 2. We can discard the highest chain card
        # 3. Essential: It's a 5, or we've discarded it before

class Rating():
    def __init__(self,index,category,difference):
        if category < 1 or category > 4:
            raise AttributeError("Rating category must be between 1-3")
        if difference < 0 or difference > 5:
            raise AttributeError("diff should be between 0,5")
        
        self.index = index
        self.category = category
        self.diff = difference
        
    def __eq__(self, other):
        if not isinstance(other,Rating):
            return False
        
        if other.category != self.category:
            return False
        
        if other.diff != self.diff:
            return False
    
        return True
    
    def __lt__(self,other):
        if self.category < other.category:
            return True

        if self.category == other.category and self.diff > other.diff:
            return True
        
        return False
        
