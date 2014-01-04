'''
Created on Dec 13, 2013

@author: aokholmRetina
'''
import numpy as np
from analyze.util.plot_functions import list2cdf, wilson
import gviz_api
from django.utils.safestring import mark_safe

colorlist = ["#3366cc","#dc3912","#ff9900","#109618","#990099","#0099c6","#dd4477","#66aa00","#b82e2e","#316395","#994499","#22aa99","#aaaa11","#6633cc","#e67300","#8b0707","#651067","#329262","#5574a6","#3b3eac","#b77322","#16d620","#b91383","#f4359e","#9c5935","#a9c413","#2a778d","#668d1c","#bea413","#0c5922","#743411"]

class Plot(object):
    
    def __init__(self):
        self.xvalues = "xval" 
        self.columnOrder = [self.xvalues]
        self.description = {self.xvalues: ("number" , "xval")}
        self.data =[]
        self.seriesIndex = 0
        self.colorIndex = 0
        self.option = {
            'title': 'title',
            'vAxis': {
                'title': 'x-axis',
            },
            'hAxis': {
                'title': 'y-axis',
            },
            #'legend': 'none',
            'series': {  
            },
            'height': 400,
            'pointSize': 2,
        }
        self.xAxis = None
        self.yAxis = None
    
    
    def addSeries (self, xlist, ylist, ids=None, line=False, legend=None, certainty = True):
        
        yListId = 'yval' + str(self.seriesIndex)
        self.columnOrder.append(yListId)
        if ids:
            yListToolId = 'yvaltool' + str(self.seriesIndex)
            self.columnOrder.append(yListToolId)
        if not certainty:
            certaintyId = 'certainty' + str(self.seriesIndex)
            self.columnOrder.append(certaintyId)
        
        
        for i in range(len(xlist)):
            row = { self.xvalues: xlist[i],
                   yListId : ylist[i],}
            if ids:
                row[yListToolId] = "Set No: %s" % ids[i]
            
            if not certainty:
                row[certaintyId] = False
            
            self.data.append(row)    
        
        descriptionString = legend if legend else "yval"
                
        self.description[yListId] = ("number" , descriptionString)
        if ids:
            self.description[yListToolId] = ("string","Tip1",{"role":"tooltip"})
        if not certainty:
            self.description[certaintyId] = ("boolean", "Certainty", {"role":"certainty"})
       
        seriesOptions = {
            'color': colorlist[self.colorIndex],
            'visibleInLegend': 'false',
            }
         
        if not ids:
            seriesOptions['tooltip'] = 'none'
            seriesOptions['enableInteractivity'] = 'false'
         
        if line:
            seriesOptions['pointSize'] = 0
        
            if certainty:
                seriesOptions['lineWidth'] = 2
            else:
                seriesOptions['lineWidth'] = 1

        if legend:
            seriesOptions['visibleInLegend'] = 'true'
        
        self.option['series'][self.seriesIndex] = seriesOptions
        
        self.seriesIndex = self.seriesIndex + 1
        
    
    def addLine (self, xlist, ylist, **kwargs):    
        
        self.addSeries(xlist, ylist, line=True, **kwargs)
        

    def addDots (self, xlist, ylist, ids, **kwargs):
        
        self.addSeries(xlist, ylist, ids=ids, **kwargs)


    def addList (self, distList, id_set, confInterval = False, **kwargs):
        
        if len(distList) <= 2:
            return False
        
        sorted_itgrade, sorted_id = zip(*sorted(zip(distList,id_set)))
        cumFreq = [(i+1)*(1/float(len(distList)+1)) for i in range(len(distList))]
        self.addDots(sorted_itgrade, cumFreq, sorted_id, **kwargs)
        
        [xvalue , cdfvalue] = list2cdf(distList)
        self.addLine(xvalue, cdfvalue)
        
        if confInterval:
            [conf_ul, conf_ll] = wilson([x*len(distList) for x in cdfvalue] , len(distList) , 0.05)
            self.addLine(xvalue, conf_ul, certainty=False)
            self.addLine(xvalue, conf_ll, certainty=False)
            
    
    def addMessets(self, messetList, confInterval=True):
        for messet in messetList:
            xvals = [getattr(measurementSet, self.xAxis) for measurementSet in messet.measurementSets]
            ids =  [measurementSet.id for measurementSet in messet.measurementSets]
            
            
            if self.xAxis and self.yAxis:
                yvals = [getattr(measurementSet, self.yAxis) for measurementSet in messet.measurementSets]
                self.addDots(xvals, yvals, ids, legend = messet.title)
            
            if self.xAxis and not self.yAxis:
                self.addList(xvals, ids, legend = messet.title, confInterval=confInterval)
                
            self.colorIndex = self.colorIndex + 1
                
    
    def newColor(self):
        self.colorIndex = self.colorIndex + 1
    
    def setXAxis(self, xAxis):
        self.xAxis = xAxis
        
    def setYAxis(self, yAxis):
        self.yAxis = yAxis    
    
    def updateTitle(self,title):
        self.option.update({'title': title })
    
    def updateXLabel(self,label):    
        self.option['hAxis'].update({'title': label})
    
    def updateYLabel(self,label):  
        self.option['vAxis'].update({'title': label})
        
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