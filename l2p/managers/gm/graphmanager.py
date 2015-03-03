#NOTE: the \n's in the strings are mostly for debugging clarity

class lineColorInfo:
    def __init__(self,fillColor = "rgba(172,194,132,0.4)",strokeColor = "#ACC26D"
    ,pointColor =  "#fff",pointStrokeColor = "#9DB86D"):
        self.fillColor = fillColor
        self.strokeColor = strokeColor
        self.pointColor = pointColor
        self.pointStrokeColor = pointStrokeColor

class GraphManager:
    '''Class which will build strings that can be used to generate graphs in an html page'''
    def __init__(self):
        # To avoid variables with the same name
        self.count = 0

    def canvasString(self,name,width,height):
        return '<canvas id= "' + name +  '" width="' + str(width) + '" height="' + str(height) + '"></canvas>\n'

    # postfix to identify between variables of the same graph
    def addDatavar(self,postfix):
        return 'Data' + str(self.count) + postfix

# LINEGRAPH==================================================================================

    def addLabels(self,labels):
        labels_string = 'labels : ['
        for label in labels:
            labels_string += '"' + label + '",'
        return labels_string[:-1] + '],'

    def addLineColors(self,colorInfos):
        return 'fillColor : "' + colorInfos.fillColor + '",\nstrokeColor : "' + colorInfos.strokeColor + '",\npointColor : "' + colorInfos.pointColor +'",\n               pointStrokeColor : "' + colorInfos.pointStrokeColor+'",\n'

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
        total_string += self.canvasString(name,width,height)
        total_string += '<script>\n'
        total_string += self.addLineData(labels,colorInfos,data)
        # The objects themself have postfix O
        total_string += 'var '+self.addDatavar('O') + " = document.getElementById('"+name+"').getContext('2d');\n"
        total_string += 'new Chart('+self.addDatavar('O')+').Line('+self.addDatavar('D')+');\n'
        total_string += '</script>\n'
        self.count += 1
        return total_string
