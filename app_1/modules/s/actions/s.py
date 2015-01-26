class Action():
    
    # init action constructor
    def __init__(self, bottle_obj=None, DOPOST=None, DOGET=None):
        self.DOPOST = DOPOST
        self.DOGET = DOGET
        self.bottle_obj = bottle_obj
        
    def s(self):
        return 'halo'
