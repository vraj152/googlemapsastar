import preprocessingGraph as pg
from pathlib import Path
from haversine import haversine

graphML = "map.graphml"
checkExists = Path("data/"+graphML)
if(not checkExists.exists()):
    pg.generateGraphML("data/map.osm",graphML)

xmldoc = pg.parseXML("data/"+graphML)
    
def getOSMId(lat, lon):
    itemlist = xmldoc.getElementsByTagName('node')
    for eachNode in range(len(itemlist)):
        dataPoints = itemlist[eachNode].getElementsByTagName('data')
        if(dataPoints[0].firstChild.data==str(lat)):
            if(dataPoints[1].firstChild.data==str(lon)):
                return (dataPoints[2].firstChild.data)  

def getLatLon(OSMId):
    ls = []
    itemlist = xmldoc.getElementsByTagName('node')
    for eachNode in range(len(itemlist)):
        dataPoints = itemlist[eachNode].getElementsByTagName('data')
        if(dataPoints[2].firstChild.data==str(OSMId)):
            ls.append(float(dataPoints[0].firstChild.data))
            ls.append(float(dataPoints[1].firstChild.data))
            break
    return tuple(ls)
    
def calculateHeuristic(curr,destination):
    return (haversine(curr,destination))
    
def getNeighbours(OSMId, destinationLetLon):
    neighbourDict = {}
    tempList = []
    itemList = xmldoc.getElementsByTagName('edge')
    for eachEdge in range(len(itemList)):
        length = 0
        if(itemList[eachEdge].attributes['source'].value==str(OSMId)):
            temp_nbr = {}
            
            dataPoints = itemList[eachEdge].getElementsByTagName('data')
            
            for eachData in range(len(dataPoints)):
                if(dataPoints[eachData].attributes['key'].value=="d12"):
                    length = dataPoints[eachData].firstChild.data
                    
            neighbour = itemList[eachEdge].attributes['target'].value
            curr = getLatLon(neighbour)
            heuristic = calculateHeuristic(curr, destinationLetLon)
            
            temp_nbr[neighbour] = [curr, length, heuristic]
            tempList.append(temp_nbr)
            
    neighbourDict[OSMId] = tempList
    return (neighbourDict)

def getNeighbourInfo(neighbourDict):
    neighbourId = 0
    neighbourHeuristic = 0
    neighbourCost = 0
    for key, value in neighbourDict.items():
        
        neighbourId = key
        neighbourHeuristic = float(value[2])
        neighbourCost = float(value[1])/1000
        
    return neighbourId, neighbourHeuristic, neighbourCost