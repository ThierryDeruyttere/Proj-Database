
# Making Graphs (parameters):
# every graph uses:
# name: no use at the moment, could be used for legend
# width/height: self explanatory: dimensions of the graph
# specifics of graphs:

# All graphs use the function prototype
#
# -makeLine/Pie/BarChart(name, width, height, colorInfos, labels, data)
# only the barchart has an extra parameter "datalabels"
# every color is a string of following structure: "rgba(*values for the color*)" or "#*hexagonal value*"
# LINECHART:
#   colorInfo's -> list of ColorInfo(fillColor, strokeColor, pointColor, pointStrokeColor) objects
#       fillcolor = color under the line
#       strokecolor = color of the line
#       point(stroke)color = color of the point (unhovered/hovered over)
#   labels -> list of strings displayed on the x-axis of the graph
#   data -> list of values(ints/flots) which will determine the relative height of the point
# PIECHART:
#   colorInfo's -> list of tuples with (color, highlightcolor) of a piece of the pie
#   labels -> list of strings displayed on the pie
#   data -> list of values(ints/flots) which will determine size of the piece of pie
# BARCHART:
#   colorInfo's -> colorInfo(fillColor, strokeColor, highlightFill, highlightStroke) object
#       fillcolor = color of the bar
#       strokecolor = color of the line
#       highlightFill = hover color of the bar
#       highlightStroke = hover color of the line
#       NOTE: lists of lists for data/labels/colors (used for comparing but still needed if talking about one thing)
#   labels -> list of strings displayed on the pie
#   data -> list of values(ints/flots) which will determine the height of the bar
#   datalabels -> currently useless, feel free to make a list of empty strings for now(= the amount of things you are comparing, could be used for legend)
# Data and labels need to be equally long lists!
# Date[i] will match with label[i] and with colorinfos[i]
# Colors+highlighted colors

# Order:                Red,                    Blue,                  Orange light,          Yellow,             Orange dark,           Grey
color_tuples = [("#f04124", "#f04124"), ("#2a3963", "#2a3963"), ("#FF9437", "#FF9437"), ("#FFA336", "#FFA336"), ("#FF621D", "#FF621D"), ("#949FB1", "#A8B3C5")]

class ColorInfo:

    def __init__(self, fillColor="#f04124", strokeColor="#f04124", pointColor="#f04124", pointStrokeColor="#f04124"):
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

    def canvasString(self, name, width, height):
        return '<canvas id= "' + name + '" width="' + str(width) + '" height="' + str(height) + '"></canvas>\n'

    # postfix to identify between variables of the same graph
    def addDatavar(self, postfix):
        return 'Data' + str(GraphManager.count) + postfix

    def addScript(self, html):
        return '<script>\n' + html + '</script>\n'

    def globalOptions(self):
        options = ''
        options += 'scaleLineColor: "rgba(255,255,255,0.5)",\n'
        options += 'scaleFontColor: "rgba(0,0,0,1)",\n'
        #options += 'pointLabelFontSize : 20,\n'
        #options += 'pointLabelSeperator: "\\n",\n'
        #options += 'scaleLabel : "<%=' + self.javaScriptTextWidthchecker() + '%>",\n'
        #options += 'scaleOverride: true,'
        #options += 'scaleSteps: 10,\n'
        #options += 'scaleStepWidth: 10,\n'
        #options += 'scaleStartValue: 0,\n'
        return options

    def addGetID(self, name):
        return 'var ' + self.addDatavar('O') + " = document.getElementById('" + name + "').getContext('2d');\n"
# LINEGRAPH======================================================================================================================

    def addLabels(self, labels):
        labels_string = 'labels : ['
        for label in labels:
            labels_string += '"' + label + '",'
        return labels_string[:-1] + '],'

    def addLineColors(self, colorInfos):
        return 'fillColor : "' + colorInfos.fillColor + '",\nstrokeColor : "' + colorInfos.strokeColor + '",\npointColor : "' + colorInfos.pointColor + '",\npointStrokeColor : "' + colorInfos.pointStrokeColor + '",\n'

    # colors is a special class
    def addLineData(self, labels, colorInfos, data):
        data_string = ''
        # D postfix for data
        data_string += 'var ' + self.addDatavar('D') + ' = {\n'
        data_string += self.addLabels(labels) + '\n'
        data_string += 'datasets : [ { \n'
        data_string += self.addLineColors(colorInfos)
        data_string += 'data : ['
        for info in data:
            data_string += str(info) + ','
        data_string = data_string[:-1] + ']\n}\n]\n}\n'
        return data_string

    def makeLineChart(self, name, width, height, colorInfos, labels, data):
        total_string = ''
        total_string += self.addLineData(labels, colorInfos, data)
        # The objects themself have postfix O
        total_string += self.addGetID(name)
        total_string += 'new Chart(' + self.addDatavar('O') + ').Line(' + self.addDatavar('D') + ');\n'
        total_string = self.addScript(total_string)
        total_string = self.canvasString(name, width, height) + total_string
        GraphManager.count += 1
        return total_string

# PIECHART=========================================================================================================

    # Colorinfo's will be a list of tuples here
    def addPieData(self, labels, data, colorInfos):
        data_string = ''
        data_string += 'var ' + self.addDatavar('D') + ' = [\n'
        for i in range(len(data)):
            data_string += '{ value: ' + str(data[i]) + ',\ncolor: "' + colorInfos[i][0] + '",\nhighlight: "' + colorInfos[i][1] + '",\nlabel :"' + labels[i] + '"},\n'
        data_string = data_string[:-1]
        data_string += '];\n'
        return data_string

    def addPieExtras(self):
        extras_string = ''
        extras_string += 'var options = { \n'
        extras_string += 'segmentShowStroke : false,\n'
        # add more stuff here
        extras_string += 'animationEasing : "easeOutBounce",'
        extras_string += 'animateScale : true\n,'
        extras_string += self.globalOptions()
        extras_string += '};\n'
        return extras_string

    # Colorinfo's will be a list of tuples here
    def makePieChart(self, name, width, height, colorInfos, labels, data):
        total_string = ''
        total_string += self.addPieData(labels, data, colorInfos)
        total_string += self.addPieExtras()
        # The objects themself have postfix O
        total_string += self.addGetID(name)
        total_string += 'new Chart(' + self.addDatavar('O') + ').Pie(' + self.addDatavar('D') + ',options);\n'
        total_string = self.addScript(total_string)
        total_string = self.canvasString(name, width, height) + total_string
        GraphManager.count += 1
        return total_string

# BARCHART==================================================================================================

    def addBarExtras(self, percentages):
        extras_string = ''
        extras_string += 'var options = { \n'
        #extras_string += 'responsive : true,\n'
        extras_string += 'animation: true,\n'
        extras_string += self.globalOptions()
        if percentages:
            extras_string += 'scaleOverride: true,\n'
            extras_string += 'scaleSteps: 10,\n'
            extras_string += 'scaleStepWidth: 10,\n'
            extras_string += 'scaleStartValue: 0,\n'
        #extras_string += 'tooltipFillColor: "rgba(0,0,0,0.8)",\n'
        #extras_string += 'multiTooltipTemplate: "<%= datasetLabel %> - <%= value %>"\n'
        # add more stuff here
        extras_string += '};\n'
        return extras_string

    # data is a list of lists here (multiple different coloured bars -> colorinfos is list of Barcolors (see above))
    # labels still 1 list
    def addBarData(self, labels, data, colorInfos, datalabels):
        data_string = ''
        data_string += 'var ' + self.addDatavar('D') + ' = {\n'
        data_string += self.addLabels(labels) + '\n'
        data_string += 'datasets : [  \n'
        # loop over lists of data
        for i in range(len(data)):
            data_string += '{ label: "' + datalabels[i] + '",\nfillColor: "' + colorInfos[i].fillColor + '",\nstrokeColor: "' + colorInfos[i].strokeColor + '",\nhighlightFill: "' + colorInfos[i].pointColor + '",\nhighlightStroke: "' + colorInfos[i].pointStrokeColor + '",\n'
            data_string += 'data : ['
            # per list, do:
            for info in data[i]:
                data_string += str(info) + ','
            data_string = data_string[:-1] + ']\n},\n'
        data_string += ']\n}\n'
        return data_string

    def makeBarChart(self, name, width, height, colorInfos, labels, data, datalabels, percentages=False):
        total_string = ''
        total_string += self.addBarData(labels, data, colorInfos, datalabels)
        total_string += self.addBarExtras(percentages)
        total_string += 'var ' + self.addDatavar('O') + ' = new Chart(document.getElementById("' + name + '").getContext("2d")).Bar(' + self.addDatavar('D') + ',options);\n'
        total_string = self.addScript(total_string)
        #total_string = '<div id="legendDiv' + str(GraphManager.count) + '"></div>\n' + total_string
        total_string = self.canvasString(name, width, height) + total_string
        GraphManager.count += 1
        return total_string
