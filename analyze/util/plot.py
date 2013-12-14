'''
Created on Dec 13, 2013

@author: aokholmRetina
'''
import numpy as np
from analyze.util.plot_functions import list2cdf
import gviz_api
from django.utils.safestring import mark_safe

colorlist = ["#3366cc","#dc3912","#ff9900","#109618","#990099","#0099c6","#dd4477","#66aa00","#b82e2e","#316395","#994499","#22aa99","#aaaa11","#6633cc","#e67300","#8b0707","#651067","#329262","#5574a6","#3b3eac","#b77322","#16d620","#b91383","#f4359e","#9c5935","#a9c413","#2a778d","#668d1c","#bea413","#0c5922","#743411"]

class Plot:
    
    def __init__(self):
        self.xvalues = "xvalues" 
        self.columnOrder = [self.xvalues]
        self.description = {self.xvalues: ("number" , "itgrade")}
        self.data =[]
        self.count = 0
        self.option = {
            'title': 'Acumulated frequency of IT grade for all data',
            'vAxis': {
                'title': 'Probability',
            },
            'hAxis': {
                'title': 'Tolerance (IT grade)',
            },
            'legend': 'none',
            'series': {  
            },
        }


    def addLine (self, xlist, ylist):    
        y = 'y' + str(self.count)

        self.columnOrder.append(y)
        
        for i in range(len(xlist)):
            self.data.append({
                self.xvalues: xlist[i],
                y : ylist[i],
                })

        self.description.update({
            y: ("number" , "yposition"),
            })
         
        line = self.count
        
        self.option['series'].update({# series 0 is the Scatter
                line: {
                    'lineWidth': 2,
                    'pointSize': 0,
                    'color': colorlist[self.count],
                    'enableInteractivity': 'false',
                    'tooltip': 'none'
                    },
                                      })
        
        self.count = self.count + 1

    def addDots (self, xlist, ylist, id_set):       
        ypos = 'ypos' + str(self.count)
        ypostool = 'ypostool' + str(self.count)

        self.columnOrder.append(ypos)
        self.columnOrder.append(ypostool)

        for i in range(len(id_set)):
            self.data.append({
                self.xvalues: xlist[i],
                ypos : ylist[i],
                ypostool: ("data from No. %s" % id_set[i])
                })

        self.description.update({
            ypos: ("number" , "yposition"),
            ypostool : ("string","Tip1",{"role":"tooltip"}),
            })
         
        dots = self.count
        
        self.option['series'].update({# series 0 is the Scatter
                dots: {
                    'color' : colorlist[self.count],
                    },
                })
        
        self.count = self.count + 1

    def addList (self, itgrade,id_set):
        
        if len(itgrade) <= 2:
            return False
        
        yvalue = np.linspace(0,1, len(itgrade)).tolist()
        sorted_itgrade, sorted_id = zip(*sorted(zip(itgrade,id_set)))
        
        cum_freq = 'cum_freq' + str(self.count)
        tooltip = 'tooltip' + str(self.count)
        best_fit = 'best_fit' + str(self.count)
        
        self.columnOrder.append(cum_freq)
        self.columnOrder.append(tooltip)
        self.columnOrder.append(best_fit)
        
        for i in range(len(id_set)):
            self.data.append({
                self.xvalues : sorted_itgrade[i],
                cum_freq: yvalue[i],
                tooltip : ("data from No. %s" % sorted_id[i])
                    })
    
        [xvalue , cdfvalue] = list2cdf(itgrade)
    
        for i in range(len(xvalue)):
            self.data.append({
                self.xvalues : xvalue[i],
                best_fit: cdfvalue[i],
                })
            
        self.description.update({
            cum_freq: ("number" , "cumulative frequency"),
            tooltip : ("string","Tip1",{"role":"tooltip"}),
            best_fit : ("number", "best fit")
            })
        
        dots = self.count
        line = dots + 1
        
        self.option['series'].update({# series 0 is the Scatter
                dots: {
                    'color' : colorlist[self.count],
                },
                line: {
                    'lineWidth': 2,
                    'pointSize': 0,
                    'color': colorlist[self.count],
                    'enableInteractivity': 'false',
                    'tooltip': 'none'
                },
            })
        
        self.count = self.count + 2
        
    def getOption(self):
        return self.option
        
    def getDescription(self):
        return self.description    
        
    def getData(self):
        return self.data
    
    def getData_table(self):
        data_table = gviz_api.DataTable(self.description)
        data_table.LoadData(self.data)
        
        return data_table
   
    def getColumnOrder(self):
        return tuple(self.columnOrder)
    
    def getJson(self):
        json = self.getData_table().ToJSon(columns_order=self.getColumnOrder())
        return mark_safe(json)

    def getValues(self):
        return self.description.keys()