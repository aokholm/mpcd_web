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
    
    
    def addSeries (self, xlist, ylist, tooltips=None, line=False, legend=None, certainty = True, color = False):
        
        yListId = 'yval' + str(self.seriesIndex)
        self.columnOrder.append(yListId)
        if tooltips:
            yListToolId = 'yvaltool' + str(self.seriesIndex)
            self.columnOrder.append(yListToolId)
        if not certainty:
            certaintyId = 'certainty' + str(self.seriesIndex)
            self.columnOrder.append(certaintyId)
        
        
        for i in range(len(xlist)):
            row = { self.xvalues: xlist[i],
                   yListId : ylist[i],}
            if tooltips:
                row[yListToolId] = tooltips[i]
            
            if not certainty:
                row[certaintyId] = False
            
            self.data.append(row)    
        
        descriptionString = legend if legend else "yval"
                
        self.description[yListId] = ("number" , descriptionString)
        if tooltips:
            self.description[yListToolId] = ("string","Tip1",{"role":"tooltip"})
        if not certainty:
            self.description[certaintyId] = ("boolean", "Certainty", {"role":"certainty"})
       
        seriesOptions = {
            'visibleInLegend': 'false',
            }
        
        if color:
            seriesOptions['color'] = colorlist[color]
        else:
            seriesOptions['color'] = colorlist[self.colorIndex]
         
        if not tooltips:
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
        

    def addDots (self, xlist, ylist, ids=False, tooltips=False, **kwargs):
        if ids:
            tooltips = ["Id: %s" % id for id in ids]
        self.addSeries(xlist, ylist, tooltips=tooltips, **kwargs)


    def addList (self, distList, tooltips, confInterval = False, **kwargs):
        
        if len(distList) <= 2:
            return False
        
        sorted_itgrade, sorted_tooltips = zip(*sorted(zip(distList,tooltips)))
        cumFreq = [(i+1)*(1/float(len(distList)+1)) for i in range(len(distList))]
        self.addDots(sorted_itgrade, cumFreq, sorted_tooltips, **kwargs)
        
        [xvalue , cdfvalue] = list2cdf(distList)
        self.addLine(xvalue, cdfvalue)
        
        if confInterval:
            [conf_ul, conf_ll] = wilson([x*len(distList) for x in cdfvalue] , len(distList) , 0.05)
            self.addLine(xvalue, conf_ul, certainty=False)
            self.addLine(xvalue, conf_ll, certainty=False)
            
    
    def addMessets(self, messetList, confInterval=True):
        for messet in messetList:
            xvals = [getattr(measurementSet, self.xAxis) for measurementSet in messet.measurementSets]
            tooltips = ["report: %s \nNr: %s, Id: %s" % (measurementSet.measurement_report.part_name, measurementSet.measurement_number, measurementSet.id) for measurementSet in messet.measurementSets]
            
            if self.xAxis and self.yAxis:
                yvals = [getattr(measurementSet, self.yAxis) for measurementSet in messet.measurementSets]
                self.addDots(xvals, yvals, tooltips=tooltips, legend = messet.title)
            
            if self.xAxis and not self.yAxis:
                self.addList(xvals, tooltips, legend = messet.title, confInterval=confInterval)
                
            self.colorIndex = self.colorIndex + 1
                
    
    def newColor(self):
        self.colorIndex = self.colorIndex + 1
    
    def setXAxis(self, xAxis, log=False):
        self.xAxis = xAxis
        
        if log:
            self.option['hAxis']['logScale'] = 'true'
        
    def setYAxis(self, yAxis, log=False):
        self.yAxis = yAxis
        
        if log:
            self.option['vAxis']['logScale'] = 'true'
    
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
    

def createStardardPlots(messets):
    
    plots = []
    
    guideLineColor = 3
    
     # ITG vs. ITG SPEC
    plot = Plot()
    plot.setXAxis('itg')
    plot.setYAxis('itg_pcsl')
    plot.addMessets(messets)
    plot.addLine([9, 15],[9,15], color=guideLineColor)
    plot.updateXLabel('Specified tolerance (ITgrade)')
    plot.updateYLabel('PCSL Tolerance (IT grade)')
    plot.updateTitle('Specified vs Actual Tolerances')
    
    plots.append(plot)
    
    # ITG PCSL
    plot = Plot()
    plot.setXAxis('itg_pcsl') 
    plot.addMessets(messets)
    plot.updateXLabel('Tolerance (IT grade)')
    plot.updateYLabel('Probability')
    plot.updateTitle('Process Capability')
    plots.append(plot)
    
    # Size vs. ITG PCSL
    plot = Plot()
    plot.setXAxis('target', log=True)
    plot.setYAxis('itg_pcsl')
    plot.addMessets(messets)
    plot.updateXLabel('Target (mm)')
    plot.updateYLabel('Tolerance (IT grade)')
    plot.updateTitle('Tolerance as a function of size')
    plots.append(plot)
    
    # normalized bias
        
    plot = Plot()
    plot.setXAxis('cb')
    plot.addMessets(messets)
    plot.updateXLabel('Normalized mean shift ()')
    plot.updateYLabel('Probability')
    plot.updateTitle('Normalized mean shift')
    plots.append(plot)
    
    # Normalized bias 2
    
#     for messet in messets:
#         for measurementSet in messet.measurementSets:
#             measurementSet.stdOverPcsl = measurementSet.std / measurementSet.pcsl 
#     
#     cpk = 5/3.0;
#     sigmaOverSymtolMax = 1/(cpk*3)
    
    plot = Plot()
    plot.setXAxis('ca_pcsl')
    plot.addMessets(messets)
    plot.updateXLabel('Ca_PCSL ()')
    plot.updateYLabel('Probability')
    plot.updateTitle('Process centering vs process precision (PCSL)')
    plots.append(plot)
    
    # Ca vs. sigma over symtol 2
    
    for messet in messets:
        for measurementSet in messet.measurementSets:
            measurementSet.stdOverSymtol = measurementSet.std / measurementSet.symtol 
    
    cpk = 5/3.0;
    sigmaOverSymtolMax = 1/(cpk*3)
    
    plot = Plot()
    plot.setXAxis('ca')
    plot.setYAxis('stdOverSymtol')
    plot.addMessets(messets)
    plot.addLine([0, 1, 1],[0,sigmaOverSymtolMax, 0], color=guideLineColor)
    plot.updateXLabel('Closeness to target - Ca')
    plot.updateYLabel('Normalised variance')
    plot.updateTitle('Process centering vs process precision')
    plots.append(plot)
    
    # CP vs. target
    
    plot = Plot()
    #plot.setXAxis('target', log=True)
    #plot.setXAxis('itg_pcsl') 
    plot.setXAxis('cb') 
    plot.setYAxis('cp', )
    plot.addMessets(messets)
    plot.updateXLabel('Normalized mean shift - Cb')
    plot.updateYLabel('Process variance index')
    plot.updateTitle('Process variance vs mean shift')
    plots.append(plot)
    
    return plots