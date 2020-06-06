# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-30 19:26:41'

"""
http://www.janpijpers.com/finding-vertex-groups-in-maya/
可以自动对选择的相邻顶点 - 自动分组
"""

import maya.OpenMaya as oldOpenMaya
import collections 
import time 
from maya import mel 

## Util needed for the old maya vertex itter. 
M_SCRIPT_UTIL = oldOpenMaya.MScriptUtil()
            
def getVertexGroups( mesh, vtxSelectionSet):
    '''
        This system finds vertex groups. 
        
        To solve a problem like this I like to think in analogies to remember the steps a bit better. ^_^ 
        
        So a vertex is a house number, and the connecting vertices are neighbors. 
        
        Think of it as neighbors living in houses but the city planing is horrible!. 
        City planning wants to divide the people in districts. 
        
        But they messed up the house numbers so they dont know who lives near who. 
        
        So we have have a list of house numbers and we want divide them into groups!
        i.e. list: 1,24,42,1337,...
                                
            We will ask house nr 1 if they have a moment to talk about ... their neighbors. 
                We ask on what number their neighbors live and we write everything down in our BIG NOTEBOOK. 
                    i.e. So house 1 is connected to neighbor 2,3,10,22 and 42
                    If one of these neighbors is in our list (Lets say nr 42) 
                        We walk over to this neighbor and ask the same question.
                        etc etc. 
                    When we no longer find any neighbors that are connected, we tear off the paper from the BIG NOTEBOOK and continue on the next. 
                        And call this group district one. 
                Now we go to house nr 2. 
                    We check if we already talked to house nr 2 while looking at neighbors!. 
                    If we did, we will go to nr3 etc. 

    '''
    
    
    ## Creates a selection list (doesn't actually get anything yet) 
    selList = oldOpenMaya.MSelectionList()
    ## Adds the mesh to the list 
    selList.add(mesh)
    ## Old style maya create an object 
    mObject = oldOpenMaya.MObject()
    ## Get the dependancy node and put it into the mObject
    selList.getDependNode(0, mObject)

    ## Create a vertex itterator loop. 
    iterVertLoop = oldOpenMaya.MItMeshVertex(mObject)
    
    ## Empty set to keep track of who we talked to. 
    talkedToNeighbours = set() 
    
    districtList = [] ## < OUR BIG NOTEBOOK!!!
    
            
    ## For every index in our provided set. Get the connecting / neighboring vertices. 
    for currentIndex in vtxSelectionSet:
        
        ## An empty set that holds all house numbers. 
        districtHouses = set() 
        ## If our current index is not in the talked to list. We can process it. 
        if not currentIndex in talkedToNeighbours:
            ## this nr is part of our list and not seen before. 
            ## so we add it to the district
            districtHouses.add( currentIndex )
            currentNeighbours = getNeighbours(iterVertLoop, currentIndex)
            
            ## As long as we have neighbours we need to keep asking around. 
            while currentNeighbours:
                ## Empty set to keep track of all the new neighbours we are about to find. 
                newNeighbours = set() 
                ## For each neighbour we currently know of. 
                for neighbour in currentNeighbours:
                    ## If they are on our list and we have not talked to them before. 
                    if neighbour in vtxSelectionSet and not neighbour in talkedToNeighbours:
                        talkedToNeighbours.add(neighbour) ## Note down we talked to them 
                        districtHouses.add(neighbour) ## Add them to our current district. 
                        
                        ## Add all their neighbours to the new neighbours list...
                        newNeighbours = newNeighbours.union(getNeighbours(iterVertLoop, neighbour)) 
                        
                ## We are done with asking all the neigbours we knew of ... so now we continue with all the new ones we found. 
                currentNeighbours = newNeighbours
                
            districtList.append( districtHouses )## << Write down data in our big notebook 
        

    return sorted(districtList, key = lambda x:min(x))

def getNeighbours( mVtxItter, index):
    mVtxItter.setIndex( index, M_SCRIPT_UTIL.asIntPtr()) 
    intArray = oldOpenMaya.MIntArray()
    mVtxItter.getConnectedVertices(intArray)
    return set(int(x) for x in intArray)


## First make a poly sphere of 200 Subdivision Axes and 200 Subdivision height. 
meshName = cmds.polySphere(sx=200,sy=200,ch=0)[0]
## then run this script. 
## Mock selection of vertecies. 
mel.eval("select -replace {meshName}.vtx[8000:9000] {meshName}.vtx[10000:12000] {meshName}.vtx[15338:15345] {meshName}.vtx[15538:15545] {meshName}.vtx[15738:15745] {meshName}.vtx[15938:15945] {meshName}.vtx[16138:16145] {meshName}.vtx[16338:16345] {meshName}.vtx[16538:16545] {meshName}.vtx[16738:16745] {meshName}.vtx[16938:16945] {meshName}.vtx[17138:17145] {meshName}.vtx[17338:17345] {meshName}.vtx[17361] {meshName}.vtx[17518:17519] {meshName}.vtx[17538:17545] {meshName}.vtx[17561:17565] {meshName}.vtx[17714:17719] {meshName}.vtx[17761:17768] {meshName}.vtx[17911:17919] {meshName}.vtx[17961:17968] {meshName}.vtx[18107:18119] {meshName}.vtx[18161:18168] {meshName}.vtx[18304:18319] {meshName}.vtx[18361:18367] {meshName}.vtx[18433:18446] {meshName}.vtx[18501:18519] {meshName}.vtx[18561:18567] {meshName}.vtx[18633:18646] {meshName}.vtx[18699:18719] {meshName}.vtx[18761:18767] {meshName}.vtx[18833:18846] {meshName}.vtx[18896:18919] {meshName}.vtx[18961:18967] {meshName}.vtx[19033:19046] {meshName}.vtx[19093:19118] {meshName}.vtx[19164:19167] {meshName}.vtx[19233:19246] {meshName}.vtx[19290:19315] {meshName}.vtx[19367] {meshName}.vtx[19433:19446] {meshName}.vtx[19487:19512] {meshName}.vtx[19633:19646] {meshName}.vtx[19685:19709] {meshName}.vtx[19797:19802] {meshName}.vtx[19833:19846] {meshName}.vtx[19882:19907] {meshName}.vtx[19997:20005] {meshName}.vtx[20033:20046] {meshName}.vtx[20079:20104] {meshName}.vtx[20197:20207] {meshName}.vtx[20233:20246] {meshName}.vtx[20278:20302] {meshName}.vtx[20397:20407] {meshName}.vtx[20433:20446] {meshName}.vtx[20478:20500] {meshName}.vtx[20597:20607] {meshName}.vtx[20633:20646] {meshName}.vtx[20678:20698] {meshName}.vtx[20797:20807] {meshName}.vtx[20833:20846] {meshName}.vtx[20878:20895] {meshName}.vtx[20997:21007] {meshName}.vtx[21033:21046] {meshName}.vtx[21078:21093] {meshName}.vtx[21197:21207] {meshName}.vtx[21233:21246] {meshName}.vtx[21278:21291] {meshName}.vtx[21397:21407] {meshName}.vtx[21433:21446] {meshName}.vtx[21478:21489] {meshName}.vtx[21597:21607] {meshName}.vtx[21633:21646] {meshName}.vtx[21678:21687] {meshName}.vtx[21797:21807] {meshName}.vtx[21833:21846] {meshName}.vtx[21878:21885] {meshName}.vtx[21998:22006] {meshName}.vtx[22033:22046] {meshName}.vtx[22078:22082] {meshName}.vtx[22202:22206] {meshName}.vtx[22233:22246] {meshName}.vtx[22279:22280] {meshName}.vtx[22404:22406] {meshName}.vtx[22433:22446] {meshName}.vtx[22633:22646] {meshName}.vtx[25531:25533] {meshName}.vtx[25557:25559] {meshName}.vtx[25727:25733] {meshName}.vtx[25757:25762] {meshName}.vtx[25923:25933] {meshName}.vtx[25958:25964] {meshName}.vtx[26122:26133] {meshName}.vtx[26158:26167] {meshName}.vtx[26322:26333] {meshName}.vtx[26358:26369] {meshName}.vtx[26522:26533] {meshName}.vtx[26558:26571] {meshName}.vtx[26722:26733] {meshName}.vtx[26758:26773] {meshName}.vtx[26921:26933] {meshName}.vtx[26959:26975] {meshName}.vtx[27121:27133] {meshName}.vtx[27159:27177] {meshName}.vtx[27321:27332] {meshName}.vtx[27359:27379] {meshName}.vtx[27520:27532] {meshName}.vtx[27559:27581] {meshName}.vtx[27720:27732] {meshName}.vtx[27760:27783] {meshName}.vtx[27920:27932] {meshName}.vtx[27960:27985] {meshName}.vtx[28119:28132] {meshName}.vtx[28160:28187] {meshName}.vtx[28319:28332] {meshName}.vtx[28361:28388] {meshName}.vtx[28519:28532] {meshName}.vtx[28561:28590] {meshName}.vtx[28718:28732] {meshName}.vtx[28761:28792] {meshName}.vtx[28918:28931] {meshName}.vtx[28962:28994] {meshName}.vtx[29117:29131] {meshName}.vtx[29162:29196] {meshName}.vtx[29317:29331] {meshName}.vtx[29363:29398] {meshName}.vtx[29400] {meshName}.vtx[29516:29531] {meshName}.vtx[29565:29602] {meshName}.vtx[29715:29731] {meshName}.vtx[29767:29805] {meshName}.vtx[29915:29931] {meshName}.vtx[29969:30007] {meshName}.vtx[30114:30130] {meshName}.vtx[30170:30210] {meshName}.vtx[30313:30330] {meshName}.vtx[30372:30411] {meshName}.vtx[30512:30530] {meshName}.vtx[30574:30610] {meshName}.vtx[30674:30676] {meshName}.vtx[30712:30730] {meshName}.vtx[30775:30810] {meshName}.vtx[30871:30877] {meshName}.vtx[30911:30930] {meshName}.vtx[30977:31009] {meshName}.vtx[31068:31079] {meshName}.vtx[31109:31129] {meshName}.vtx[31178:31208] {meshName}.vtx[31265:31280] {meshName}.vtx[31308:31329] {meshName}.vtx[31380:31407] {meshName}.vtx[31461:31481] {meshName}.vtx[31507:31529] {meshName}.vtx[31581:31606] {meshName}.vtx[31657:31683] {meshName}.vtx[31705:31729] {meshName}.vtx[31783:31805] {meshName}.vtx[31856:31885] {meshName}.vtx[31903:31928] {meshName}.vtx[31985:32004] {meshName}.vtx[32056:32089] {meshName}.vtx[32099:32128] {meshName}.vtx[32186:32203] {meshName}.vtx[32257:32328] {meshName}.vtx[32388:32401] {meshName}.vtx[32457:32527] {meshName}.vtx[32589:32599] {meshName}.vtx[32658:32727] {meshName}.vtx[32791:32799] {meshName}.vtx[32858:32926] {meshName}.vtx[32993:32997] {meshName}.vtx[33058:33126] {meshName}.vtx[33259:33326] {meshName}.vtx[33459:33525] {meshName}.vtx[33660:33724] {meshName}.vtx[33861:33924] {meshName}.vtx[34061:34123] {meshName}.vtx[34262:34323] {meshName}.vtx[34463:34522] {meshName}.vtx[34663:34721] {meshName}.vtx[34864:34920] {meshName}.vtx[35065:35119] {meshName}.vtx[35267:35318] {meshName}.vtx[35468:35516] {meshName}.vtx[35669:35715] {meshName}.vtx[35871:35913] {meshName}.vtx[36073:36111] {meshName}.vtx[36276:36308] {meshName}.vtx[36479:36505] {meshName}.vtx[36685:36699]".format(meshName=meshName))

## Get all vtx in set. (We dont care about the order. So set is faster then list.) 
## Using cmds and string conversion, as its faster then pymel. 
vtxSelectionSet = set( [int(x.split(".vtx[")[-1][:-1]) for x in set(cmds.ls(sl=True, o=False, fl = True)) - set(cmds.ls(sl=True, o=True))])

## Start a simple timer to know how long it takes. 
start = time.time() 

vertexGroups = getVertexGroups(meshName, vtxSelectionSet) 
   
print ("Duration: %s seconds" %str(time.time()- start ))

for groep, entries in enumerate(vertexGroups):
    print ("Groep : " ,groep)
    print ("\tMin : " ,min(entries))
    print ("\tMax : " ,max(entries))