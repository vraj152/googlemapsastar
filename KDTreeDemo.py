import numpy as np
from sklearn.neighbors import KDTree
import xmltodict
import time

#%%
doc = {}
with open('data/map.graphml') as fd:
    doc = xmltodict.parse(fd.read())

#%%
nodes = doc["graphml"]["graph"]["node"]
locations = []
for eachNode in range(len(nodes)):
    locations.append((nodes[eachNode]["data"][0]["#text"],nodes[eachNode]["data"][1]["#text"]))

locations_arr = np.asarray(locations, dtype=np.float32)

#%%
s= time.time()
point = (40.48834484237183,-74.4464808486693)
point = np.asarray(point, dtype=np.float32)

tree = KDTree(locations_arr, leaf_size=2)
dist, ind = tree.query(point.reshape(1,-1), k=3) 

print(dist)
ans = (float(locations[ind[0][0]][0]), float(locations[ind[0][0]][1]))
print(ans)
#print(locations[ind])
print(time.time()-s)