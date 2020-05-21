import helperFile as hp
import heapq as heap

#%%
source = (40.5028504, -74.4353862)      #First Node
destination = (40.5065907, -74.4312433) #Last Node

open_list = []
g_values = {}
f_values = {}

closed_list = []
path = []

sourceID = hp.getOSMId(source[0], source[1])
destID = hp.getOSMId(destination[0], destination[1])

g_values[sourceID] = 0
h_source = hp.calculateHeuristic(source, destination)

open_list.append((h_source,sourceID))

#%%
while(len(open_list)>0):
    curr_state = open_list[0][1]
    
    print(curr_state)
    print(hp.getLatLon(curr_state))
    
    heap.heappop(open_list)
    closed_list.append(curr_state)
    
    if(curr_state==destID):
        print("We have reached to the goal")
        break 
    
    nbrs = hp.getNeighbours(curr_state, destination)
    values = nbrs[curr_state]
    for eachNeighbour in values:
        
        neighbourId, neighbourHeuristic, neighbourCost = hp.getNeighbourInfo(eachNeighbour)
        current_inherited_cost = g_values[curr_state] + neighbourCost

        #Check if neighbour is in closed list, skip it
        if(neighbourId in closed_list):
            continue
        else:
            g_values[neighbourId] = current_inherited_cost
            neighbourFvalue = neighbourHeuristic + current_inherited_cost
            
            open_list.append((neighbourFvalue, neighbourId))
        
    open_list = list(set(open_list))
    heap.heapify(open_list)
