import requests
from bs4 import BeautifulSoup
import networkx as nx
from itertools import chain
from collections import Counter
import time

start_time=time.clock()

def ProgTime():
    return "["+str(time.clock()-start_time)+"s] "

def GetUserKeywords(user):
    soup=BeautifulSoup(
        requests.get("https://www.deviantart.com/"+user).text,
        'html.parser'
    )
    return soup.find_all('meta',attrs={"name":"keywords"})[0]['content'].split(", ")


def GetUserFriendsPage(user,count):
    soup=BeautifulSoup(
        requests.get("https://www.deviantart.com/"+user+"/modals/myfriends/?offset="+str(count)).text,
        'html.parser'
    )
    return [a['title'] for a in soup.find_all(attrs={"class":"avatar"})]

def GetUserFriends(user):
    out=[]
    count=0
    while(True):
        k=GetUserFriendsPage(user,count)
        if(len(k)==0):
            break
        out=out+k
        count=count+100
    return out
        

def GetDeviationTags(url):
    print(ProgTime()+"getting deviation tags for "+url)
    soup=BeautifulSoup(
        requests.get(url).text,
        'html.parser'
    )
    tags=soup.find(attrs={"class":"dev-about-tags-cc dev-about-breadcrumb"}).find_all(attrs={"class":"discoverytag"})
    return [a.contents[1] for a in tags]

#<div class="dev-about-tags-cc dev-about-breadcrumb">

def GetDeviations(user):
    # will only grab the first 24, more requires ajax requests which is a pain
    soup=BeautifulSoup(
        requests.get("https://www.deviantart.com/"+user+"/gallery/?catpath=/").text,
        'html.parser'
    )
    return [a['href'] for a in soup.find_all(attrs={"class":"torpedo-thumb-link"})]

def GetTagsForUser(user):
    return Counter(list(chain(*[GetDeviationTags(url) for url in GetDeviations(user)])))

# use tag similarity as distance metric?




# print(GetDeviationTags("https://www.deviantart.com/0-2-100/art/CLOSED-Lowblood-Troll-Adopts-Offer-To-Adopt-728467431"))

# print(GetTagsForUser("axsens"))

# a=GetUserFriends("nummypixels")
# print(len(a))

# print(GetUserFriends("lopoddity"))

# print(GetUserKeywords("aplexpony"))

# print(GetDeviationTags("https://www.deviantart.com/aplexpony/art/Three-faces-of-Rarity-783993670"))



def CreateNode(G,user):
    print(ProgTime()+"creating node "+user)
    G.add_node(user,tags=GetTagsForUser(user))
    # add node returns None
    
    
    
def AddFriends(G,user,depth):
    for friend in GetUserFriends(user):
        print(ProgTime()+friend)
        if friend not in G.nodes:
            CreateNode(G,friend)
            G.add_edge(user,friend)
            if(depth>0):
                AddFriends(G,user,depth-1)
        
def WriteJson(G,loc):
    f=open(loc,"w")
    f.write(string(nx.node_link_data(G)))
    f.close()



# creating the graph

G=nx.Graph()
print(ProgTime()+"created graph")

start="thekenzai1987"

print(ProgTime()+"creating initial node")
CreateNode(G,start)

max_depth=1

print(ProgTime()+"beginning recursion")
AddFriends(G,start,max_depth)

nx.write_gexf(G, "test.gexf")
nx.write_gml(G, "test.gml")
WriteJson(G,"test.json")

#nx.write_gpickle(G,"test.gpickle")
# maximum recursion depth exceeded


print(ProgTime()+"nodes: "+str(G.number_of_nodes()))
print(ProgTime()+"edges:"+str(G.number_of_edges()))

# Traceback (most recent call last):
  # File "deviantart.py", line 120, in <module>
    # nx.write_gexf(G, "test.gexf")
  # File "<C:\Users\Kevin\AppData\Local\Programs\Python\Python36-32\lib\site-packages\decorator.py:decorator-gen-628>", line 2, in write_gexf
  # File "C:\Users\Kevin\AppData\Local\Programs\Python\Python36-32\lib\site-packages\networkx\utils\decorators.py", line 240, in _open_file
    # result = func_to_be_decorated(*new_args, **kwargs)
  # File "C:\Users\Kevin\AppData\Local\Programs\Python\Python36-32\lib\site-packages\networkx\readwrite\gexf.py", line 88, in write_gexf
    # writer.add_graph(G)
  # File "C:\Users\Kevin\AppData\Local\Programs\Python\Python36-32\lib\site-packages\networkx\readwrite\gexf.py", line 315, in add_graph
    # self.add_nodes(G, graph_element)
  # File "C:\Users\Kevin\AppData\Local\Programs\Python\Python36-32\lib\site-packages\networkx\readwrite\gexf.py", line 362, in add_nodes
    # node_data, default)
  # File "C:\Users\Kevin\AppData\Local\Programs\Python\Python36-32\lib\site-packages\networkx\readwrite\gexf.py", line 442, in add_attributes
    # raise TypeError('attribute value type is not allowed: %s' % val_type)
# TypeError: attribute value type is not allowed: <class 'collections.Counter'>
    