'''
Created on Jan 4, 2014

@author: aokholmRetina
'''

class MessetContainer:
    
    def __init__(self, measurementSets, title=None):
        self.measurementSets = measurementSets
        self.title = title
    
    def setTitle(self, title):
        self.title = title
        