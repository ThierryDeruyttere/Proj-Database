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
        pass

    def canvasString(self,name,width,height):
        return '<canvas id= ' + name +  ' width="' + width + '" height="' + height + '"></canvas>'

    def addData(self):
        return 'var Data = {'

    # colors is a special class
    def addLineData(self,labels,colorInfos,data):
        data_string = ''
        data_string += addData()

        data_string += '}'
        return



    def makeLineChart(self,name,width,height):
        total_string = ''
        total_string += canvasString(name,width,height)
        total_string += '<script>'
        # more adds

        total_string += '</script>'
        return total_string

'''<script>
// line chart data
var buyerData = {
labels : ["January","February","March","April","May","June"],
    datasets : [
        {
            fillColor : "rgba(172,194,132,0.4)",
            strokeColor : "#ACC26D",
            pointColor : "#fff",
            pointStrokeColor : "#9DB86D",
            data : [203,156,99,251,305,247]
        }
    ]
}
// get line chart canvas
var buyers = document.getElementById('buyers').getContext('2d');
// draw line chart
new Chart(buyers).Line(buyerData);
</script>'''
