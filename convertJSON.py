import xmltodict
from haversine import haversine

doc = {}
with open('data/map.graphml') as fd:
    doc = xmltodict.parse(fd.read())

def getLatLon(OSMId):
    lat, lon = 0, 0
    nodes = doc['graphml']['graph']['node']
    for eachNode in range(len(nodes)):
        if(nodes[eachNode]["@id"] == str(OSMId)):
            lat = float(nodes[eachNode]["data"][0]["#text"])
            lon = float(nodes[eachNode]["data"][1]["#text"])
    return (lat, lon)

def getOSMId(lat, lon):
    OSMId = 0
    nodes = doc['graphml']['graph']['node']
    for eachNode in range(len(nodes)):
        if(nodes[eachNode]["data"][0]["#text"]==str(lat)):
            if(nodes[eachNode]["data"][1]["#text"]==str(lon)):
                OSMId = nodes[eachNode]["data"][2]["#text"]
            
    return OSMId
    
def calculateHeuristic(curr,destination):
    return (haversine(curr,destination))

def getNeighbours(OSMId, destinationLetLon):
    neighbourDict = {}
    tempList = []
    edges = doc['graphml']['graph']['edge']
    for eachEdge in range(len(edges)):
        if(edges[eachEdge]["@source"]==str(OSMId)):
            temp_nbr = {}
            
            neighbourCost = 0
            neighbourId = edges[eachEdge]["@target"]
            neighbourLatLon = getLatLon(neighbourId) 
            
            dataPoints = edges[eachEdge]["data"]
            for eachData in range(len(dataPoints)):
                if(dataPoints[eachData]["@key"]=="d12"):
                    neighbourCost = dataPoints[eachData]["#text"]
            
            neighborHeuristic = calculateHeuristic(neighbourLatLon, destinationLetLon)
            
            temp_nbr[neighbourId] = [neighbourLatLon, neighbourCost, neighborHeuristic]
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