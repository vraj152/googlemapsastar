import convertJSON as cj
import heapq as heap
import time

def aStar(source, destination):
    open_list = []
    g_values = {}
    
    path = {}
    closed_list = {}
    
    sourceID = cj.getOSMId(source[0], source[1])
    destID = cj.getOSMId(destination[0], destination[1])
    
    g_values[sourceID] = 0
    h_source = cj.calculateHeuristic(source, destination)
    
    open_list.append((h_source,sourceID))
    
    s = time.time()
    while(len(open_list)>0):
        curr_state = open_list[0][1]
        
        #print(curr_state)
        heap.heappop(open_list)
        closed_list[curr_state] = ""
        
        if(curr_state==destID):
            print("We have reached to the goal")
            break 
        
        nbrs = cj.getNeighbours(curr_state, destination)
        values = nbrs[curr_state]
        for eachNeighbour in values:
            neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon = cj.getNeighbourInfo(eachNeighbour)
            current_inherited_cost = g_values[curr_state] + neighbourCost
    
            if(neighbourId in closed_list):
                continue
            else:
                g_values[neighbourId] = current_inherited_cost
                neighbourFvalue = neighbourHeuristic + current_inherited_cost
                
                open_list.append((neighbourFvalue, neighbourId))
            
            path[str(neighbourLatLon)] = {"parent":str(cj.getLatLon(curr_state)), "cost":neighbourCost}
            
        open_list = list(set(open_list))
        heap.heapify(open_list)
    
    print("Time taken to find path(in second): "+str(time.time()-s))
    return path