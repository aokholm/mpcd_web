'''
Created on Dec 13, 2013

@author: aokholmRetina
'''

class Plot:
    
    description = {}
    options = {}
    data = []
    series = []
    
    description5 = {
    "itg": ("number" , "IT grade"),
    "cum_freq1": ("number" , "cumulative frequency"),
    "tooltip1" : ("string","Tip1",{"role":"tooltip"}),
    "best_fit1" : ("number", "best fit"),
    "cum_freq2": ("number" , "cumulative frequency"),
    "tooltip2" : ("string","Tip2",{"role":"tooltip"}),
    "best_fit2" : ("number", "best fit")
    }
    
    data5= [{
            "itg": 3,
            "cum_freq2": 76,
            "tooltip2": ("data from No. %s" % 7)
                },
            {
            "itg": 5,
            "cum_freq2": 66,
            "tooltip2": ("data from No. %s" % 8)
                }]
    
    
    def __init__(self, xaxis, yaxis):
        self.xaxis = xaxis
        self.yaxis = yaxis
        
    def addSeries(self, series):
        self.series.append(series)
        
    def getDescription(self):
        return self.description    
        
    def getData(self):
        return self.data
    
#     def getOptions(self):
#         return self.options
#     
#         option5 = {
#         'title': 'comparison of acumulated frequency of first production run vs.  all data',
#         'vAxis': {
#             'title': 'Probability',
#         },
#         'hAxis': {
#             'title': 'tolerance (IT Grade)',
#         },
#         'legend': 'none',
#         'series': {
#             # series 0 is the Scatter
#             0: {
#             # you can omit this if you choose not to set any options for this series
#             },
#             # series 1 is the Line
#             1: {
#                 'lineWidth': 2,
#                 'pointSize': 0,
#                 'color': 'blue',
#                 'enableInteractivity': 'false',
#                 'tooltip': 'none'
#             },
#             2: {
#             # you can omit this if you choose not to set any options for this series
#             },
#             # series 1 is the Line
#             3: {
#                 'lineWidth': 2,
#                 'pointSize': 0,
#                 'color': 'orange',
#                 'enableInteractivity': 'false',
#                 'tooltip': 'none'
#             },
#         },
#     }
    
