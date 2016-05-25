import sys
import os
import time

class Vertex:
  def __init__(self,key):
    self.id=key
    self.connectedTo={}
    ###home/away##
    self.doubles={}
    self.rank=0
    self.perf=0
    self.factor=0
    self.rating=0
    self.nrating=0
    self.w=0
    self.l=0
    self.t=0

  def addNeighbor(self,nbr,weight=0):
    if nbr in self.connectedTo:
      self.doubles[nbr]=weight
    else:
      self.connectedTo[nbr]=weight

  def __str__(self):
    return str(self.id)+' connectedTo: '+str([x.id for x in self.connectedTo])

  def getConnections(self):
    return self.connectedTo.keys()

  def getDConnections(self):
    return self.doubles.keys()

  def getId(self):
    return self.id

  def getDWeight(self,nbr):
    return self.doubles[nbr]

  def getWeight(self,nbr):
    return self.connectedTo[nbr]
  
  def getRecord(self):
    return (str(self.w)+'-'+str(self.l)+'-'+str(self.t))

class Graph:
  def __init__(self):
    self.vertList={}
    self.numVertices=0

  def addVertex(self,key):
    self.numVertices+=1
    newVertex=Vertex(key)
    self.vertList[key]=newVertex
    return newVertex

  def getVertex(self,n):
    if n in self.vertList:
      return self.vertList[n]
    else:
      return None

  def __contains__(self,n):
    return n in self.vertList

  def addEdge(self,f,t,cost=0):
    if f not in self.vertList:
      nv=self.addVertex(f)
    if t not in self.vertList:
      nv=self.addVertex(t)
    self.vertList[f].addNeighbor(self.vertList[t],cost)

  def getVertices(self):
    return self.vertList.keys()

  def __iter__(self):
    return iter(self.vertList.values())


def runSeason(games, season):
  for game in games:
   #print(game)
    score=int(game[1])-int(game[3])
    season.addEdge(game[0],game[2],int(game[1])-int(game[3]))
    season.addEdge(game[2],game[0],int(game[3])-int(game[1]))
   #print(score)
    if score > 0:
      season.vertList[game[0]].w+=1
      season.vertList[game[2]].l+=1
    elif score < 0:
      season.vertList[game[2]].w+=1
      season.vertList[game[0]].l+=1
    else:
      season.vertList[game[2]].t+=1
      season.vertList[game[0]].t+=1
      
  for team in season.vertList:
    temp=0
    count=0
   #print('team:',team)
    for c in season.vertList[team].getConnections():
      count+=1
      temp+=season.vertList[team].getWeight(c)
     #print('count:',count,'score:',season.vertList[team].getWeight(c),'total:',temp)
    for d in season.vertList[team].getDConnections():
      count+=1
      temp+=season.vertList[team].getDWeight(d)
     #print('count:',count,'score:',season.vertList[team].getDWeight(d),'total:',temp)

    season.vertList[team].perf=float(temp/count)
    season.vertList[team].rating=season.vertList[team].perf
   #print('performance:',season.vertList[team].perf)
   #print(' w-l-t\n',season.vertList[team].getRecord())
   #print([x.id for x in season.vertList[team].connectedTo])
   #print([x.id for x in season.vertList[team].doubles])
  k=5000  
  for i in range(k):
    for team in season.vertList:
      temp=0
      count=0
     # print('team:',team)
      for c in season.vertList[team].getConnections():
      #  print('played',c.id)
        count+=1
        temp+=c.rating
       # print('count:',count,'score:',c.rating,'total:',temp)
        if c in season.vertList[team].getDConnections():
        #  print('played',c.id)
          count+=1
          temp+=c.rating
         # print('count:',count,'score:',c.rating,'total:',temp)
      season.vertList[team].factor=float(temp/count)
     #print(('team',c.id))
     # print('sched:',season.vertList[team].factor)
    for team in season.vertList:
      season.vertList[team].rating=float(season.vertList[team].perf) + float(season.vertList[team].factor)
     #print(('team',team))
     # print('sched:',season.vertList[team].factor)
     # print('rating:',season.vertList[team].rating)
 
def printRecord(season,args): 
  fname='output_'+args[1] 
  with open(fname,'w') as f:
    newseason=[]
    index=0
    for i in season.vertList:
      newseason.append(['',i,season.vertList[i].getRecord()])
      newseason[index][0]=(season.vertList[i].rating)
      index+=1
    newseason.sort()
    newseason.reverse()
    t=["Rank","Team","W-L-T","Rating"]
    f.write("%3s %-32s %-8s %6s" % (t[0],t[1],t[2],t[3]))
    f.write('\n')
    for i in range(0,len(newseason)):  
      f.write("%3d  %-32s %-8s %6.3f" % (i+1,newseason[i][1],newseason[i][2],newseason[i][0]))
      f.write('\n')


def main(args):
  t1=time.time() 
  season=Graph()
  games=[]
  game=[]
  with open(args[1],'r')as f:
    for line in f:
      tokens=[]
      name=line[:33].rstrip()
      tokens.append(name)
      tokens.append(int(line[33:36]))
      name=line[37:71].rstrip()
      tokens.append(name)
      tokens.append(int(line[71:73]))
      games.append(tokens)
   #for g in games:  
     #print(g)


  runSeason(games,season)
  printRecord(season,args)
  t2=time.time()
  t2-=t1
 # for v in season.vertList:
  #  print(season.vertList[v].id,season.vertList[v].rating)
  print('time taken:',t2)




if __name__=='__main__':
  sys.exit(main(sys.argv))

