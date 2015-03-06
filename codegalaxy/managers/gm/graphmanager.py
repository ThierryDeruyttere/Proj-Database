#NOTE: the \n's in the strings are mostly for debugging clarity
#Data and labels need to be equally long lists!

#Colors+highlighted colors
#Order: Red,Green,Yellow,Dark Grey,Purple,Grey
color_tuples = [("#F7464A","#FF5A5E"),("#46BFBD","#5AD3D1"),("#FDB45C","#FFC870"),("#4D5360","#616774"),("#B48EAD","#C69CBE"),("#949FB1","#A8B3C5")]

class ColorInfo:
    def __init__(self,fillColor = "rgba(172,194,132,0.4)",strokeColor = "#ACC26D"
    ,pointColor =  "#fff",pointStrokeColor = "#9DB86D"):
        self.fillColor = fillColor
        self.strokeColor = strokeColor
        # Ok so this is a bit fked, use these as highlightFill and highlightStroke for bars
        self.pointColor = pointColor
        self.pointStrokeColor = pointStrokeColor

class GraphManager:
    count = 0
    '''Class which will build strings that can be used to generate graphs in an html page'''
    def __init__(self):
        # To avoid variables with the same name
        pass

    def canvasString(self,name,width,height):
        return '<canvas id= "' + name +  '" width="' + str(width) + '" height="' + str(height) + '"></canvas>\n'

    # postfix to identify between variables of the same graph
    def addDatavar(self,postfix):
        return 'Data' + str(GraphManager.count) + postfix

    def addScript(self,html):
        return '<script>\n'+html+'</script>\n'

    def addGetID(self,name):
        return 'var '+self.addDatavar('O') + " = document.getElementById('"+name+"').getContext('2d');\n"
# LINEGRAPH======================================================================================================================

    def addLabels(self,labels):
        labels_string = 'labels : ['
        for label in labels:
            labels_string += '"' + label + '",'
        return labels_string[:-1] + '],'

    def addLineColors(self,colorInfos):
        return 'fillColor : "' + colorInfos.fillColor + '",\nstrokeColor : "' + colorInfos.strokeColor + '",\npointColor : "' + colorInfos.pointColor +'",\npointStrokeColor : "' + colorInfos.pointStrokeColor+'",\n'

    # colors is a special class
    def addLineData(self,labels,colorInfos,data):
        data_string = ''
        # D postfix for data
        data_string += 'var '+self.addDatavar('D') + ' = {\n'
        data_string += self.addLabels(labels) + '\n'
        data_string += 'datasets : [ { \n'
        data_string += self.addLineColors(colorInfos)
        data_string += 'data : ['
        for info in data:
            data_string += str(info) + ','
        data_string = data_string[:-1] + ']\n}\n]\n}\n'
        return data_string

    def makeLineChart(self,name,width,height,colorInfos,labels,data):
        total_string = ''
        total_string += self.addLineData(labels,colorInfos,data)
        # The objects themself have postfix O
        total_string += self.addGetID(name)
        total_string += 'new Chart('+self.addDatavar('O')+').Line('+self.addDatavar('D')+');\n'
        total_string = self.addScript(total_string)
        total_string = self.canvasString(name,width,height) + total_string
        GraphManager.count += 1
        return total_string

# PIECHART=========================================================================================================

    # Colorinfo's will be a list of tuples here
    def addPieData(self,labels,data,colorInfos):
        data_string = ''
        data_string += 'var '+self.addDatavar('D') + ' = [\n'
        for i in range(len(data)):
            data_string += '{ value: '+str(data[i])+',\ncolor: "'+colorInfos[i][0]+'",\nhighlight: "'+colorInfos[i][1]+'",\nlabel :"'+labels[i]+'"},\n'
        data_string = data_string[:-1]
        data_string += '];\n'
        return data_string

    def addPieExtras(self):
        extras_string = ''
        extras_string += 'var options = { \n'
        extras_string += 'segmentShowStroke : false,\n'
        # add more stuff here
        extras_string += 'animationEasing : "easeOutBounce",'
        extras_string += 'animateScale : true\n'
        extras_string += '};\n'
        return extras_string

    # Colorinfo's will be a list of tuples here
    def makePieChart(self,name,width,height,colorInfos,labels,data):
        total_string = ''
        total_string += self.addPieData(labels,data,colorInfos)
        total_string += self.addPieExtras()
        # The objects themself have postfix O
        total_string += self.addGetID(name)
        total_string += 'new Chart('+self.addDatavar('O')+').Pie('+self.addDatavar('D')+',options);\n'
        total_string = self.addScript(total_string)
        total_string = self.canvasString(name,width,height) + total_string
        GraphManager.count += 1
        return total_string

# BARCHART==================================================================================================

    def addBarExtras(self):
        extras_string = ''
        extras_string += 'var options = { \n'
        #extras_string += 'responsive : true,\n'
        extras_string += 'animation: true,\n'
        #extras_string += 'tooltipFillColor: "rgba(0,0,0,0.8)",\n'
        #extras_string += 'multiTooltipTemplate: "<%= datasetLabel %> - <%= value %>"\n'
        # add more stuff here
        extras_string += '};\n'
        return extras_string

    # data is a list of lists here (multiple different coloured bars -> colorinfos is list of Barcolors (see above))
    # labels still 1 list
    def addBarData(self,labels,data,colorInfos,datalabels):
        data_string = ''
        data_string += 'var '+self.addDatavar('D') + ' = {\n'
        data_string += self.addLabels(labels) + '\n'
        data_string += 'datasets : [  \n'
        # loop over lists of data
        for i in range(len(data)):
            data_string += '{ label: "'+ datalabels[i]+ '",\nfillColor: "'+colorInfos[i].fillColor+'",\nstrokeColor: "'+colorInfos[i].strokeColor+'",\nhighlightFill: "'+colorInfos[i].pointColor+'",\nhighlightStroke: "'+colorInfos[i].pointStrokeColor+'",\n'
            data_string += 'data : ['
            # per list, do:
            for info in data[i]:
                data_string += str(info) + ','
            data_string = data_string[:-1] + ']\n},\n'
        data_string += ']\n}\n'
        return data_string


    def makeBarChart(self,name,width,height,colorInfos,labels,data,datalabels):
        total_string = ''
        total_string += self.addBarData(labels,data,colorInfos,datalabels)
        total_string += self.addBarExtras()
        total_string += 'var '+self.addDatavar('O')+' = new Chart(document.getElementById("'+name+'").getContext("2d")).Bar('+self.addDatavar('D')+',options);\n'
        total_string = self.addScript(total_string)
        total_string =  '<div id="legendDiv'+str(GraphManager.count)+'"></div>\n' + total_string
        total_string = self.canvasString(name,width,height) + total_string
        GraphManager.count += 1
        return total_string
