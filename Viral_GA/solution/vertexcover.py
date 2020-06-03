import numpy as np

class edge:
    def __init__(self,weight,v1,v2):
        self.v1=v1
        self.v2=v2
        self.weight=weight
        self.removed= False
    
    def __repr__(self):
        return "({},{},{})\n".format(self.v1,self.v2,self.weight)

class node:
    def __init__(self,name,value,adj=[],degree=0):
        self.name=name
        self.value=value
        self.adj=adj
        self.degree=degree

    def __repr__(self):
        return "({},{},{})\n".format(self.name,self.degree,self.adj)

class Graph:
    def __init__(self,n):
        self.nodes=[]
        for i in range(n):
            self.nodes.append(node(i,i))
        self.node_count=n
        self.edges = []
        self.edge_count=0
        self.total_edges=0
        self.sorted_edges=[]
        self.worst_edge_idx = 0
        self.adj=[]
        for i in range(n):
            self.adj.append([])
    
    def add_edge(self,v1,v2,weight):
        e=edge(weight,v1,v2)
        self.edges.append(e)
        self.nodes[v1].edges.append(e)
        self.nodes[v1].degree+=1
        self.nodes[v2].edges.append(e)
        self.nodes[v2].degree+=1
        self.edge_count+=1
        pass
    
    def remove_edge(self,i):
        e=self.sorted_edges[i]
        v1,v2=self.edges[e].v1,self.edges[i].v2
        self.nodes
        self.sorted_edges[i] = -1
        self.edge_count-=1
        pass

    def disconnect_vertex(self,i):
        e=self.adj[i]
        ## if it has index of sorted then its quick
        for v in e:
            if  self.sorted_edges[v] != -1:
                self.sorted_edges[v] = -1
                self.edge_count-=1

        self.adj[i]=[]
        self.nodes[i].degree=0
        pass

    def get_worst_edge(self):
        t=self.worst_edge_idx
        w=self.sorted_edges[self.worst_edge_idx]
        while self.sorted_edges[t+1] == -1:
            t+=1
            if t+1 == self.total_edges:
                break
        self.worst_edge_idx=t
        return w





def distance(v,u):
    d=np.sqrt(np.sum((v-u)**2))
    return d

def f_weight(v1,v2,d):
    w=100/((v1+v2)*(1+d))
    return w

def ppl_to_graph(ppl,d):
    n=len(ppl)
    G = Graph(n)
    #print("graph initlaied succcesful")
    if n <= 1 :
        return G

    weights = []
    idx = []
    lv1=[]
    lv2=[]
    count=0
    for i in range(n-1):
        j=i+1
        while j < n:
            dist = distance(ppl[i].var_objective,ppl[j].var_objective)
            if dist < d:
                w=f_weight(i,j,dist)
                #print("1 more less than d "+str(dist))
                weights.append(w)
                idx.append(count)
                lv1.append(i)
                lv2.append(j)
                count+=1
            j+=1
    #print("total less than d " +str(count))
    G.total_edges=count
    # sorted edges by weight
    if count > 0:
        #print("yes making sorted edges \n")
        G.sorted_edges = [x for _,x in sorted(zip(weights,idx))]

        s = [x for _,x in sorted(zip(G.sorted_edges,idx))]
        #print(s)
        #print(lv1,lv2)
        for i in range(len(idx)):
            e=edge(weights[i],lv1[i],lv2[i])
            G.edges.append(e)
            G.adj[lv1[i]].append(s[i])
            G.nodes[lv1[i]].degree+=1
            G.adj[lv2[i]].append(s[i])
            G.nodes[lv2[i]].degree+=1
            G.edge_count+=1
            

    return G

# n^2 + E*log(E) + sum{VC}( {get_worst_edge} 1 + remove_edge + 2*disocnnect_vertex)
# input is population withour elit and its neighbours removed

# dv = 2*|E_v|
# re = 1+2*1
def vertex_cover(ppl,d):
    G=ppl_to_graph(ppl,d) # n^2
    #print("graph made succesful")
    #print("edges \n: "+str(G.edges))
    #print("Nodes\n: "+str(G.nodes))
    #print("soreted edges\n: "+str(G.sorted_edges))
    VC = []
    
    # if there are no points closer than d
    if G.edge_count == 0:
        return VC

    #print("adj:\n"+str(G.adj))
    # loop below until no edges remain in graph
    while G.edge_count > 0:
        ## find the worst edge in list add its both v,u to VC
        i=G.sorted_edges[G.worst_edge_idx]
        #print("wost edg "+str(i))
        v1,v2=G.edges[i].v1,G.edges[i].v2
        #print("v1v2:"+str(v1)+","+str(v2))
        VC.append(v1)
        VC.append(v2)
        ## remove all the edges on v,u from graph
        ### this requires to remove all edges incenent on v1 & v2
        G.disconnect_vertex(v1)
        G.disconnect_vertex(v2)

        t=G.worst_edge_idx
        while True:
            t+=1
            if t == G.total_edges:
                break
            if G.sorted_edges[t]!=-1:
                break
        G.worst_edge_idx=t

        #print(G.edge_count)
        #print("edges \n: "+str(G.edges))
        #print("soreted edges\n: "+str(G.sorted_edges))
        #print("adj:\n"+str(G.adj))
    

    return VC


class vvvv:
    def __init__(self,var_decision,var_objective):
        self.var_decision=var_decision
        self.var_objective=var_objective
    def __repr__(self):
        return str(self.var_decision)+", "+str(self.var_objective) +"\n"

"""n=1000
sp=10000
ppl = [vvvv(sp*np.random.rand(2),sp*np.random.rand(2)) for i in range(n)]

#print(ppl)
vc=vertex_cover(ppl,d=10)
print(len(vc)/n,vc,sep='\n')"""