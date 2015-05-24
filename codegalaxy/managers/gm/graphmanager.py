
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

# Order:                Blue,                    Red,                  Orange light,          Yellow,               Orange dark,                  Grey
color_tuples = [("#2a3963", "#3e5084"), ("#f04124", "#f76148"), ("#FF9437", "#ffa85d"), ("#FFA336", "#ffb257"), ("#FF621D", "#ff773b"), ("#949FB1", "#A8B3C5")]

# Struct used to represent colors in a graph
class ColorInfo:

    def __init__(self, fillColor="#f04124", strokeColor="#f04124", pointColor="#f04124", pointStrokeColor="#f04124"):
        self.fillColor = fillColor
        self.strokeColor = strokeColor
        self.pointColor = pointColor
        self.pointStrokeColor = pointStrokeColor

# Class which will build strings that can be used to generate graphs on an html page
# with the help of jquery (Chart.js)
class GraphManager:
    count = 0

    def __init__(self):
        pass

    # html for the canvas in which the graph will be displayed
    def canvasString(self, name, width, height):
        return '<canvas id= "' + name + '" width="' + str(width) + '" height="' + str(height) + '"></canvas>\n'

    # Postfix to identify between variables of the same graph
    def addDatavar(self, postfix):
        return 'Data' + str(GraphManager.count) + postfix

    # Adding script tags around other html code
    def addScript(self, html):
        return '<script>\n' + html + '</script>\n'

    # Global options for each graph (described in the chart.js documentation)
    def globalOptions(self):
        options = ''
        options += 'scaleLineColor: "rgba(255,255,255,0.5)",\n'
        options += 'scaleFontColor: "#8d8887",\n'
        return options

    # jquery lookup for the graph
    def addGetID(self, name):
        return 'var ' + self.addDatavar('O') + " = document.getElementById('" + name + "').getContext('2d');\n"

    # Labels are for the various datasets (ex. the slices of a pie chart)
    def addLabels(self, labels):
        labels_string = 'labels : ['
        for label in labels:
            labels_string += '"' + label + '",'
        return labels_string[:-1] + '],'

    # Fits the given data in a format for pie charts
    def addPieData(self, labels, data, colorInfos):
        data_string = ''
        data_string += 'var ' + self.addDatavar('D') + ' = [\n'
        for i in range(len(data)):
            data_string += '{ value: ' + str(data[i]) + ',\ncolor: "' + colorInfos[i][0] + '",\nhighlight: "' + colorInfos[i][1] + '",\nlabel :"' + labels[i] + '"},\n'
        data_string = data_string[:-1]
        data_string += '];\n'
        return data_string

    # Extra graphical options for Pie Charts
    def addPieExtras(self):
        extras_string = ''
        extras_string += 'var options = { \n'
        extras_string += 'segmentShowStroke : false,\n'
        extras_string += 'animationEasing : "easeOutBounce",'
        extras_string += 'animateScale : true\n,'
        extras_string += self.globalOptions()
        extras_string += '};\n'
        return extras_string

    # Gives the Chart a title (which is positioned aove the graph)
    def addTitle(self, chart, name):
        return "<p><span class='octicon octicon-chevron-right'></span> " + name + "</p>\n" + chart

    # Creates jquery/html for a Pie chart
    def makePieChart(self, name, width, height, colorInfos, labels, data, chart_name=None):
        total_string = ''

        total_string += self.addPieData(labels, data, colorInfos)
        total_string += self.addPieExtras()
        # The objects themself have postfix O
        total_string += self.addGetID(name)
        total_string += 'new Chart(' + self.addDatavar('O') + ').Pie(' + self.addDatavar('D') + ',options);\n'
        total_string = self.addScript(total_string)
        total_string = self.canvasString(name, width, height) + total_string
        if chart_name:
            total_string = self.addTitle(total_string, chart_name)
        GraphManager.count += 1
        return total_string

    # BARCHART==================================================================================================

    # Extra graphical options for Bar Charts
    def addBarExtras(self, percentages):
        extras_string = ''
        extras_string += 'var options = { \n'
        extras_string += 'animation: true,\n'
        extras_string += self.globalOptions()
        if percentages:
            extras_string += 'scaleOverride: true,\n'
            extras_string += 'scaleSteps: 10,\n'
            extras_string += 'scaleStepWidth: 10,\n'
            extras_string += 'scaleStartValue: 0,\n'
        extras_string += '};\n'
        return extras_string

    # data is a list of lists here (multiple different coloured bars -> colorinfos is list of Barcolors (see above))
    # labels still 1 list
    # Fits the given data in a format for Bar charts
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

    # Creates jquery/html for a Bar chart
    def makeBarChart(self, name, width, height, colorInfos, labels, data, datalabels, percentages=False):
        total_string = ''
        total_string += self.addBarData(labels, data, colorInfos, datalabels)
        total_string += self.addBarExtras(percentages)
        total_string += 'var ' + self.addDatavar('O') + ' = new Chart(document.getElementById("' + name + '").getContext("2d")).Bar(' + self.addDatavar('D') + ',options);\n'
        total_string = self.addScript(total_string)
        total_string = self.canvasString(name, width, height) + total_string
        GraphManager.count += 1
        return total_string
