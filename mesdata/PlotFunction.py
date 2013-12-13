import numpy as np
import mesdata.PCfunctions as pc
import gviz_api


def lists2JsonOptions (list1,id1,list2,id2):

    description = {
    "itg": ("number" , "IT grade"),
    "cum_freq1": ("number" , "cumulative frequency"),
    "tooltip1" : ("string","Tip1",{"role":"tooltip"}),
    "best_fit1" : ("number", "best fit"),
    "cum_freq2": ("number" , "cumulative frequency"),
    "tooltip2" : ("string","Tip2",{"role":"tooltip"}),
    "best_fit2" : ("number", "best fit")
    }



    data =[]

    yvalue1 = [i*(1/float(len(list1)+1)) for i in range(1, len(list1)+1)]
    sorted_itg1, sorted_id1 = zip(*sorted(zip(list1,id1)))

    yvalue2 = [i*(1/float(len(list2)+1)) for i in range(1, len(list2)+1)]
    sorted_itg2, sorted_id2 = zip(*sorted(zip(list2,id2)))

    for i in range(len(sorted_id1)):
        data.append({
            "itg": sorted_itg1[i],
            "cum_freq1": yvalue1[i],
            "tooltip1": ("data from No. %s" % sorted_id1[i])
                })
    for i in range(len(sorted_id2)):
        data.append({
            "itg": sorted_itg2[i],
            "cum_freq2": yvalue2[i],
            "tooltip2": ("data from No. %s" % sorted_id2[i])
                })

    [xvalue1 , cdfvalue1] = pc.list2cdf(list1)
    [xvalue2 , cdfvalue2] = pc.list2cdf(list2)

    for i in range(len(xvalue1)):
        data.append({
            "itg": xvalue1[i],
            "best_fit1": cdfvalue1[i],
            })

    for i in range(len(xvalue2)):
        data.append({
            "itg": xvalue2[i],
            "best_fit2": cdfvalue2[i],
            })

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    json = data_table.ToJSon(columns_order=("itg","cum_freq1","tooltip1","best_fit1","cum_freq2","tooltip2","best_fit2"))

    option = {
        'vAxis': {
            'title': 'Probability',
        },
        'hAxis': {
            'title': 'tolerance (IT Grade)',
        },
        'legend': 'none',
        'series': {
            # series 0 is the Scatter
            0: {
            # you can omit this if you choose not to set any options for this series
            },
            # series 1 is the Line
            1: {
                'lineWidth': 2,
                'pointSize': 0,
                'color': 'blue',
                'enableInteractivity': 'false',
                'tooltip': 'none'
            },
            2: {
            # you can omit this if you choose not to set any options for this series
            },
            # series 1 is the Line
            3: {
                'lineWidth': 2,
                'pointSize': 0,
                'color': 'orange',
                'enableInteractivity': 'false',
                'tooltip': 'none'
            },
        },
    }
    return (json, option)

def lists2DescribtionDataOptions (list1,id1,num):
    
    description = {}
    
    var1 = 'xvalue'
    var2 = 'cum_freq' + str(num)
    var3 = 'tooltip' + str(num)
    var4 = 'best_fit' + str(num)
    
    description[var1] = ("number" , "IT grade")
    description[var2] = ("number" , "cumulative frequency")
    description[var3] = ("string","Tip1",{"role":"tooltip"})
    description[var4] = ("number", "best fit")

    data =[]

    yvalue1 = [i*(1/float(len(list1)+1)) for i in range(1, len(list1)+1)]
    sorted_itg1, sorted_id1 = zip(*sorted(zip(list1,id1)))

    for i in range(len(sorted_id1)):
        data.append({
            var1: sorted_itg1[i],
            var2: yvalue1[i],
            var3 : ("data from No. %s" % sorted_id1[i])
                })

    [xvalue1 , cdfvalue1] = pc.list2cdf(list1)
    for i in range(len(xvalue1)):
        data.append({
            var1: xvalue1[i],
            var4: cdfvalue1[i],
            })
    
    
    var5 = num*2-2
    var6 = var5 + 1
    
    colorlist = ["#3366cc","#dc3912","#ff9900","#109618","#990099","#0099c6","#dd4477","#66aa00","#b82e2e","#316395","#994499","#22aa99","#aaaa11","#6633cc","#e67300","#8b0707","#651067","#329262","#5574a6","#3b3eac","#b77322","#16d620","#b91383","#f4359e","#9c5935","#a9c413","#2a778d","#668d1c","#bea413","#0c5922","#743411"]
    
    
        
    option = {
        'vAxis': {
            'title': 'Probability',
        },
        'hAxis': {
            'title': 'tolerance (IT Grade)',
        },
        'legend': 'none',
        'series': {
            # series 0 is the Scatter
            var5: {
                'color' : colorlist[num],
            # you can omit this if you choose not to set any options for this series
            },
            # series 1 is the Line
            var6: {
                'lineWidth': 2,
                'pointSize': 0,
                'color': colorlist[num],
                'enableInteractivity': 'false',
                'tooltip': 'none'
            },
        },
    }
    return (description, data, option)