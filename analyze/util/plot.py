'''
Created on Dec 13, 2013

@author: aokholmRetina
'''
import numpy as np
from analyze.util.plot_functions import list2cdf, wilson
import gviz_api
from django.utils.safestring import mark_safe

colorlist = ["#3366cc","#dc3912","#ff9900","#109618","#990099","#0099c6","#dd4477","#66aa00","#b82e2e","#316395","#994499","#22aa99","#aaaa11","#6633cc","#e67300","#8b0707","#651067","#329262","#5574a6","#3b3eac","#b77322","#16d620","#b91383","#f4359e","#9c5935","#a9c413","#2a778d","#668d1c","#bea413","#0c5922","#743411"]

class Plot:
    
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
    
    
    def addSeries (self, xlist, ylist, ids=None, line=False, legend=None):
        
        yListId = 'yval' + str(self.seriesIndex)
        self.columnOrder.append(yListId)
        if ids:
            yListToolId = 'yvaltool' + str(self.seriesIndex)
            self.columnOrder.append(yListToolId)
        
        for i in range(len(xlist)):
            row = { self.xvalues: xlist[i],
                   yListId : ylist[i],}
            if ids:
                row[yListToolId] = "Set No: %s" % ids[i]
            self.data.append(row)    
        
        descriptionString = legend if legend else "yval"
                
        self.description[yListId] = ("number" , descriptionString)
        if ids:
            self.description[yListToolId] = ("string","Tip1",{"role":"tooltip"})
       
        seriesOptions = {
            'color': colorlist[self.colorIndex],
            'visibleInLegend': 'false',
            }
         
        if not ids:
            seriesOptions['tooltip'] = 'none'
            seriesOptions['enableInteractivity'] = 'false'
         
        if line:
            seriesOptions['lineWidth'] = 2
            seriesOptions['pointSize'] = 0

        if legend:
            seriesOptions['visibleInLegend'] = 'true'
        
        self.option['series'][self.seriesIndex] = seriesOptions
        
        self.seriesIndex = self.seriesIndex + 1
        self.colorIndex = self.colorIndex + 1
    
    
    def addLine (self, xlist, ylist, **kwargs):    
        
        self.addSeries(xlist, ylist, line=True, **kwargs)
        

    def addDots (self, xlist, ylist, ids, **kwargs):
        
        self.addSeries(xlist, ylist, ids=ids, **kwargs)


    def addList (self, distList, id_set, **kwargs):
        
        if len(distList) <= 2:
            return False
        
        sorted_itgrade, sorted_id = zip(*sorted(zip(distList,id_set)))
        cumFreq = [(i+1)*(1/float(len(distList)+1)) for i in range(len(distList))]
        self.addDots(sorted_itgrade, cumFreq, sorted_id, **kwargs)
        self.colorIndex = self.colorIndex -1
        
        [xvalue , cdfvalue] = list2cdf(distList)
        self.addLine(xvalue, cdfvalue)
         

    
    def addQuerySet (self, messets, xvalue='itg_pcsl', addConfLines=True):
        
        xvalues = [getattr(messet, xvalue) for messet in messets]
        ids =  [messet.id for messet in messets]
        
        self.addList(xvalues, ids)
        
        if addConfLines:
            self.addConfidenceInterval(xvalues)
        

    
    def addConfidenceInterval (self, itgrade):    
        
        if len(itgrade) <= 2:
            return False
        
        conf_uls = 'conf_ul' + str(self.seriesIndex)
        conf_lls = 'conf_ll' + str(self.seriesIndex)
        
        self.columnOrder.append(conf_uls)
        self.columnOrder.append(conf_lls)
        
        [xvalue , cdfvalue] = list2cdf(itgrade)       
        [conf_ul, conf_ll] = wilson([x*len(itgrade) for x in cdfvalue] , len(itgrade) , 0.05)

        for i in range(len(xvalue)):
            self.data.append({
                self.xvalues : xvalue[i],
                conf_uls: conf_ul[i],
                conf_lls: conf_ll[i],
                })
        
        self.description.update({
            conf_uls : ("number", "conf_upper"),
            conf_lls : ("number", "conf_lower")
            })
        
        line1 = self.seriesIndex
        line2 = line1 + 1
        
        self.option['series'].update({
                line1: {
                    'lineWidth': 2,
                    'pointSize': 0,
                    'color': colorlist[self.seriesIndex],
                    'enableInteractivity': 'false',
                    'tooltip': 'none'
                },
                line2: {
                    'lineWidth': 2,
                    'pointSize': 0,
                    'color': colorlist[self.seriesIndex],
                    'enableInteractivity': 'false',
                    'tooltip': 'none'
                },
            })
        
        self.seriesIndex = self.seriesIndex + 2
    
    
    def addMessets(self, messetList):
        for messet in messetList:
            xvals = [getattr(measurementSet, self.xAxis) for measurementSet in messet.measurementSets]
            ids =  [measurementSet.id for measurementSet in messet.measurementSets]
            
            
            if self.xAxis and self.yAxis:
                yvals = [getattr(measurementSet, self.yAxis) for measurementSet in messet.measurementSets]
                self.addDots(xvals, yvals, ids, legend = messet.title)
            
            if self.xAxis and not self.yAxis:
                self.addList(xvals, ids, legend = messet.title)
                
    
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