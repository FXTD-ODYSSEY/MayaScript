# copySDK, 20110109
#
# Python definitions to mirror SDK setups to single/multiple objects.
# isoparmB
#
# - updated 20110117
#   Added 'driver' mode
#   Corrected mirror key behaviour for angular units
#
# - updated 20130916
#   Added moveSDK function
#   Added ability to rename target driver attributes
#   Added ability to create driver attribute if non-existant (createDriverAttr)
#   Added mirrorSelectedChannels convenience function
#   Format changes
#
# for questions or suggestions, email me at martinik24@gmail.com 

###############################################################################
import maya.cmds as cmds
import re, math

ANIM_CURVE_TYPES = ('animCurveUL', 'animCurveUA', 'animCurveUU',
                    'animCurveTL', 'animCurveTA', 'animCurveTU')


def copySDK(curAttrs=[], mirrorAttrs=[], source='', targets=[],
            search='', replace='', specialIter=[], sort=False, mode='driven',
            drAttrSearch='', drAttrReplace='', createDriverAttr=False):
    '''This definition is used to copy SDK setups from one node
to another node/s in Maya.  With no declarations, the script works by getting
the selection list. The first selected object is the source, everything else
is a target. The script will copy SDKs from the source and replicate it
on the targets.   SDKs will be linked to the original source driver by default.


Node and attribute options

curAttrs    - string or string list     - is for explicitly declaring
                        which attributes to copy SDKs from.  If you
                        don't declare it, the script will search for SDKs
                        on all keyable attributes of the source.

mirrorAttrs - string or string list     - is to tell the script
                        which attributes on the source object will receive
                        a negative value in their keyframes.

source      - string                    - is to explicitly declare
                        the source node to copy.  If this is declared, targets
                        must also be declared. If not declared, the selection
                        list is used and the first selected object
                        is the source.
                                        - if mode is set to driven, source
                        represents the source driven node, when mode is set
                        to driver, source represents the source driver node.

targets     - string or string list     - is to explicitly declare target nodes
                        to apply SDKs to.  If this is declared, source
                        must also be declared. If not declared, the selection
                        list is used and all other objects other than the first
                        comprise the targets list.
                                        - if mode is set to driven, targets
                        represents the destination driven node/s, when mode
                        is set to driver, targets represents the destination
                        driver node/s.



String search options for driver nodes:

search      - string                    - when mode is set to Driven, is used
                        for pattern searching in Driver names.  search
                        and replace both have to be declared. If not declared,
                        the SDK's are connected to the original driver node
                        attributes.  This attribute accepts regex
                        search strings.
                                        - when mode is set to Driver, this is
                        used instead to search for Driven object names. search
                        and replace MUST be declared in case of Driver-centric
                        operations.

replace     - string                    - when mode is set to Driven, is used
                        for pattern searching in Driver names, to look for
                        alternate Driver nodes. This provides the
                        replace string to use when looking for Driver nodes.
                        The replace string can use the special %s character
                        to provide more flexibility with choosing different
                        Drivers for multiple Driven nodes.
                                        - when mode is set to Driver, this
                        is used instead to search for Driven object names.
                        search and replace MUST be declared in case of
                        Driver-centric operations.

specialIter - int or string list or list of lists  - is used when you want to
                        provide a list or an iteratable object to use when you
                        want more flexibility in naming your driver object.
                        Your replace variable must contain a replace string
                        with %s, and that will get swapped by what you
                        enter here.
                                        - You can use a single list
                        ['a', 'b', 'c'], lists within lists for multiple %s's
                        [['a', 'b', 'c'], [1, 2, 3]], or python techniques
                        such as range e.g., range(0,12).
                                        - The only rule is that the lists
                        have to be as long as the number of targets.

sort        - boolean                   - Sort the target list alphabetically.
                        Helps to reorganize the targets list if you're using
                        the specialIter function.

mode        - string 'driver', 'driven' or 'guess' - Decides whether the script
                        operates via selecting a driven node, or a driver node.
                        Default is set to driven, meaning you have to select
                        the driven object you want to mirror over as your
                        first selection.  Options are either 'driver',
                        'driven', or 'guess' (if set to guess, will find
                        whether it has more outgoing or incomming
                        sdk keyframes), and the default is driven.
                                        - In driven mode, script wil find the
                        original driver from the driven node and seek out
                        alternate driver names via the search and replace
                        variables if declared, else it will use
                        the original driver/s.
                                        - In driver mode, script will seek out
                        all driven nodes and search for the alternate driven
                        node names based off the search and replace variables.
                        In driver mode, search and replace declaration
                        is required.

drAttrSearch  - string                  - If declared, search for this string
                        component in a source driver attribute, for
                        the purpose of replacing this string in
                        a target driver attribute.

drAttrReplace - string                  - If declared, use this string
                        to replace a found attrSearch component in a source
                        driver attr when looking for a target driver attr.

createDriverAttr - boolean              - Create the driver attribute on
                        a found target node if it did not already exist,
                        Default is False.  This only works in 'driver' mode.
'''
    # Make sure all variables are correct
    if not source.strip() or not targets:
        curlist = cmds.ls(sl=True, ap=True)
        if not curlist or len(curlist) < 2:
            print ('\nPlease select at least two objects.')
            return 1
        source = curlist[0]
        targets = curlist[1:]
    elif isinstance(targets, str) and targets.strip():
        targets = [targets]
    if sort:
        targets.sort()
    if curAttrs:
        
        if isinstance(curAttrs, str) and curAttrs.strip():
            curAttrs = [curAttrs]
        
        attrs = [cmds.attributeQuery(x, node=source, ln=True) for x in curAttrs
                 if cmds.attributeQuery(x, node=source, ex=True)]
        if not attrs:
            print ('Specified attributes %s, do not exist on driver %s .'
                   % (', '.join(attrs), source))
            return 1
    else:
        attrs = cmds.listAttr(source, k=True)
    
    if mirrorAttrs:
        if isinstance(mirrorAttrs, str):
            mirrorAttrs = [mirrorAttrs]
        tempMirrorAttrs = []
        for attr in mirrorAttrs:
            if not cmds.attributeQuery(attr, node=source, ex=True):
                continue
            tempMirrorAttrs.append(cmds.attributeQuery(attr, node=source, ln=True))
        tempMirrorAttrs = list(set(tempMirrorAttrs))
        if tempMirrorAttrs:
            mirrorAttrs = tempMirrorAttrs
        else:
            print ('Specified attributes to be mirrored %s, do not exist '
                   'on source node %s .' % (', '.join(mirrorAttrs), source))
            mirrorAttrs = []
    
    if mode.strip().lower() == 'driven':
        mode = True
    elif mode.strip().lower() == 'driver':
        mode = False
    elif mode.lower() == 'guess':
        driverNodes = []
        drivenNodes = []
        
        drivenNodes, blendWeightedNodes = \
            findSDKNodes(mirrorAttrs, source, attrs, True)
        if blendWeightedNodes:
            for node in blendWeightedNodes:
                SDKN2, SKN, ON = searchBWNodes(node)
                if SDKN2:
                    a = set(drivenNodes + SDKN2)
                    drivenNodes = list(a)
        driverNodes, blendWeightedNodes = \
            findSDKNodes(mirrorAttrs, source, attrs, False)
        
        if len(drivenNodes) >= len(driverNodes):
            mode = True
        else:
            mode = False
    else:
        print ('\nUnrecognized mode argument: "' + str(mode) +
               '", use either "driver", "driven", or "guess".')
        return 1
    
    # Determine special iteration parameters if there is a %s in the replace
    # variable. Used for complex Driver name searching, if each of your targets
    # has a different driver object.
    SDKResults = []
    BWNResults = []
    iterExec = None
    if (not search or not replace) and mode:
        search = None
        replace = None
    elif (not search or not replace) and not mode:
        print ('\nPlease "declare" search and "replace" variables '
               'when in driver mode.')
        return 1
    elif replace.count('%s') and not specialIter:
        print ('\nWhen using the "%s" character, you must declare '
               'a specialIter list')
        return 1
    elif replace.count('%s'):
        if (isinstance(specialIter[0], list) or
                isinstance(specialIter[0], tuple)):
            numArgs = len(specialIter)
            iterExec = 'feeder = ('
            iterScratch = []
            for x in range(0, numArgs):
                if len(specialIter[x]) != len(targets):
                    print ('\nspecialIter item ' + str(x) + ' length (' +
                           str(len(specialIter[x])) + ') must be the same as target'
                                                      ' length (' + str(len(targets)) + ') .')
                    return 1
                iterScratch.append('specialIter[%s][i]' % str(x))
            
            iterExec += ', '.join(iterScratch) + ' )'
        else:
            if len(specialIter) != len(targets):
                print ('\nspecialIter length (' + str(len(specialIter)) +
                       ') must be the same as target length (' +
                       str(len(targets)) + ') .')
                return 1
            iterExec = 'feeder = specialIter[i]'
    
    # Acquire SDK and blendweighted nodes from source
    SDKnodes, blendWeightedNodes = \
        findSDKNodes(mirrorAttrs, source, attrs, mode)
    
    # Go through all the targets and mirror SDK nodes and
    # blendWeighted nodes with SDK from source.
    i = 0
    for target in targets:
        if SDKnodes:
            doSDKs(SDKnodes, target, search, replace, i, iterExec, specialIter,
                   SDKResults, BWNResults, mode, createDriverAttr,
                   drAttrSearch, drAttrReplace)
        
        if blendWeightedNodes and mode:
            for node in blendWeightedNodes:
                
                SDKnodes2, SKnodes, otherNodes = searchBWNodes(node)
                
                if SDKnodes2:
                    newBlendNode = cmds.duplicate(node[0])[0]
                    doSDKs(SDKnodes2, newBlendNode, search, replace, i,
                           iterExec, specialIter, SDKResults, BWNResults,
                           True, createDriverAttr,
                           drAttrSearch, drAttrReplace)
                    if SKnodes:
                        for node2 in SKnodes:
                            newKeyNode = cmds.duplicate(node2[0])[0]
                            if node2[2]:
                                mirrorKeys(newKeyNode)
                            cmds.connectAttr('%s.output' % newKeyNode,
                                             '%s.%s' % (newBlendNode, node2[1]), f=True)
                    cmds.connectAttr('%s.output' % newBlendNode,
                                     '%s.%s' % (target, node[1]), f=True)
                    BWNResults.append('Connected Blend Weighted node '
                                      '%s.output to Driven node %s.%s' %
                                      (newBlendNode, target, node[1]))
                else:
                    print ('\nNo SDK nodes connected to blendWeighted node '
                           + node[0] + ', skipping...')
        i += 1
    
    return 0


def moveSDK(source=None, destination=None, curAttrs=[],
            drAttrSearch='', drAttrReplace='', deleteOldAttrs=False):
    ''' Move the specified set driven key attributes from once source driver
    attr to one target destination driver attr.
    '''
    
    if not source or not destination:
        source, destination = cmds.ls(sl=True)
    
    if not all((cmds.objExists(source), cmds.objExists(destination))):
        print ('One of the nodes does not exist, '
               'please check: %s, %s' % (source, destination))
        return 1
    
    if curAttrs:
        
        if isinstance(curAttrs, str) and curAttrs.strip():
            curAttrs = [curAttrs]
        
        attrs = [cmds.attributeQuery(x, node=source, ln=True) for x in curAttrs
                 if cmds.attributeQuery(x, node=source, ex=True)]
        if not attrs:
            print ('Specified attributes %s, do not exist on driver %s .'
                   % (', '.join(attrs), source))
            return 1
    else:
        attrs = cmds.listAttr(source, k=True)
    
    # Get the SDK's and any blendwheighted nodes with SDKs.
    driverNodes, blendWeightedNodes = findSDKNodes((), source, attrs, False)
    
    # Connect all the old connections from the source to the new attr
    # on the destinationn attribute.
    for nodeList in (driverNodes, blendWeightedNodes):
        for node in nodeList:
            # Create the new driver attr if it does not already exist.
            createDriverAttrFunc(source, destination, node[1].split('[')[0],
                                 drAttrSearch, drAttrReplace)
            
            cmds.connectAttr('%s.%s' % (destination,
                                        node[1].replace(drAttrSearch, drAttrReplace)),
                             '%s.%s' % (node[0], node[3]), f=True)
    
    # If specified, delete the old driver attr.
    if not deleteOldAttrs:
        return
    userDefinedAttrs = cmds.listAttr(source, ud=True)
    for attr in attrs:
        if attr in userDefinedAttrs and \
                not cmds.listConnections('%s.%s' % (source, attr),
                                         scn=True, d=True, s=True, p=False):
            cmds.deleteAttr('%s.%s' % (source, attr))


def findSDKNodes(mirrorAttrs, source, attrs, mode):
    '''Searches for SDK nodes or blendWeighted nodes on a given node.
    Mode determines whether to search for incomming or outgoing connections
    (True is incommingm False is outgoing).

    Will return a list of found SDK nodes and blendWeighted nodes.'''
    
    SDKN = []
    BWN = []
    
    if mode:
        listConLambda = lambda source, attr: cmds.listConnections(
            '%s.%s' % (source, attr), scn=True, d=False, s=True, p=True)
    else:
        listConLambda = lambda source, attr: cmds.listConnections(
            '%s.%s' % (source, attr), scn=True, d=True, s=False, p=True)
    
    for attr in attrs:
        conns = listConLambda(source, attr)
        if conns:
            for conn in conns:
                conn, targetAttr = conn.split('.')[0], \
                                   '.'.join(conn.split('.')[1:])
                nodeType = cmds.ls(conn, st=True)[1]
                mirrorAttr = False
                if attr in mirrorAttrs:
                    mirrorAttr = True
                if nodeType in ('animCurveUL', 'animCurveUA', 'animCurveUU'):
                    SDKN.append((conn, attr, mirrorAttr, targetAttr))
                elif nodeType == 'blendWeighted' and mode:
                    BWN.append((conn, attr, mirrorAttr, targetAttr))
    return SDKN, BWN


def searchBWNodes(node):
    '''Searches for SDK nodes, keyframe nodes and other connections on
    a blendWeighted node. Will return a list of found SDK nodes,
    keyframe nodes and any other node connection types.'''
    
    SDKN2 = []
    SKN = []
    ON = []
    attrs = cmds.listAttr('%s.input' % node[0], multi=True)
    if not attrs:
        print ('\nNo SDK nodes connected to blendWeighted node %s'
               ', skipping...' % node[0])
        return [], [], []
    
    for attr in attrs:
        conn = cmds.listConnections(
            '%s.%s' % (node[0], attr), scn=True, d=False, s=True, p=True)
        if conn:
            nodetype = cmds.ls(conn[0].split('.')[0], st=True)[1]
            mirrorAttr = node[2]
            if nodetype in ('animCurveUL', 'animCurveUA', 'animCurveUU'):
                SDKN2.append((conn[0].split('.')[0], attr, mirrorAttr))
            elif nodetype in ('animCurveTL', 'animCurveTA', 'animCurveTU'):
                SKN.append((conn[0].split('.')[0], attr, mirrorAttr))
            else:
                ON.append((conn[0], attr, mirrorAttr))
    
    return SDKN2, SKN, ON


def connectToConn(replace, iterExec, curNode, curNode2,
                  repPattern, mode, newKeyNode, origBW):
    ''' Connect the newKeyNode basked on she search/replace
    parameters specified.
    '''
    
    errorCheck = False
    if replace.count('%s'):
        currentRep = replace
        exec (iterExec) in locals()
        currentRep = currentRep % feeder
        newConn = curNode2.split('.')[0].replace(repPattern, currentRep)
    else:
        newConn = curNode2.split('.')[0].replace(repPattern, replace)
    
    if cmds.objExists(newConn) and \
            cmds.attributeQuery(
                '.'.join(curNode2.split('.')[1:]), node=newConn, ex=True) and \
            mode:
        cmds.connectAttr(
            '%s.%s' % (newConn, '.'.join(curNode2.split('.')[1:])),
            '%s.input' % newKeyNode, f=True)
    
    # In driver mode, check for blendWeighted nodes. If the target
    # has a blendWeighted node, check to see if it has the same number
    # of input multi attrs, otherwise make a new one.
    elif cmds.objExists(newConn) and (
                cmds.attributeQuery(
                    '.'.join(curNode2.split('.')[1:]), node=newConn, ex=True) or
                cmds.attributeQuery(
                    curNode2.split('.')[1].split('[')[0], node=newConn, ex=True)) \
            and not mode:
        
        targetCon = cmds.listConnections(
            '%s.%s' % (newConn, '.'.join(curNode2.split('.')[1:])),
            s=True, d=False, p=True, scn=True)
        makeNewBW = False
        if targetCon:
            nodeType = cmds.ls(targetCon[0].split('.')[0], st=True)[1]
            if nodeType == 'blendWeighted':
                targetBWInSize = len(cmds.listAttr(
                    '%s.input' % targetCon[0].split('.')[0], multi=True))
                origBWInSize = len(cmds.listAttr(
                    '%s.input' % origBW.split('.')[0], multi=True))
                if targetBWInSize == origBWInSize:
                    cmds.connectAttr('%s.output' % newKeyNode,
                                     '%s.%s' % (targetCon[0].split('.')[0],
                                                '.'.join(curNode.split('.')[1:])), f=True)
                else:
                    makeNewBW = True
            else:
                makeNewBW = True
        else:
            makeNewBW = True
        
        if makeNewBW and origBW:
            newBW = cmds.duplicate(origBW.split('.')[0])[0]
            cmds.connectAttr('%s.output' % newKeyNode,
                             '%s.%s' % (newBW, '.'.join(curNode.split('.')[1:])), f=True)
            cmds.connectAttr('%s.output' % newBW,
                             '%s.%s' % (newConn, '.'.join(curNode2.split('.')[1:])), f=True)
        else:
            cmds.connectAttr('%s.output' % newKeyNode,
                             '%s.%s' % (newConn, '.'.join(curNode2.split('.')[1:])), f=True)
    
    elif mode and cmds.objExists(newConn) and \
            not cmds.attributeQuery(
                '.'.join(curNode2.split('.')[1:]), node=newConn, ex=True):
        print ('\nDriver node %s does not have the attribute %s .'
               % (newConn, '.'.join(curNode2.split('.')[1:])))
        cmds.delete(newKeyNode)
    
    else:
        errorCheck = True
    
    return errorCheck, newConn


def createDriverAttrFunc(sourceDriver, targetDriver, origAttr,
                         drAttrSearch, drAttrReplace, skipRecursion=False):
    ''' Recursive function that takes an attribute on one node and replicates
    it on another.  Will handle compound attributes.
    '''
    
    sourceNodeAttr = '%s.%s' % (sourceDriver, origAttr)
    
    # If we're dealing with a compound attr like a double3,
    # create the parent first.
    parentAttr = cmds.addAttr(sourceNodeAttr, **{'q': True, 'parent': True})
    targetParentAttr = None
    if parentAttr and parentAttr != origAttr:
        targetParentAttr = parentAttr.replace(drAttrSearch, drAttrReplace)
        if not skipRecursion:
            createDriverAttrFunc(sourceDriver, targetDriver, parentAttr,
                                 drAttrSearch, drAttrReplace)
    
    targetNodeAttr = '%s.%s' % (targetDriver,
                                origAttr.replace(drAttrSearch, drAttrReplace))
    targetAttr = origAttr.replace(drAttrSearch, drAttrReplace)
    if cmds.attributeQuery(targetAttr, node=targetDriver, ex=True):
        return
    
    attrDict = {}
    keyable = cmds.getAttr("%s.%s" % (sourceDriver, origAttr), k=True)
    attrDict['ln'] = targetAttr
    attrDict['at'] = cmds.getAttr(sourceNodeAttr, type=True)
    if attrDict['at'] in ('double', 'long', 'float'):
        for curAttr in ('min', 'max', 'dv'):
            if isinstance(cmds.addAttr(
                    sourceNodeAttr, **{'q': True, curAttr: True}),
                    type(None)):
                continue
            attrDict[curAttr] = cmds.addAttr(
                sourceNodeAttr, **{'q': True, curAttr: True})
    
    if cmds.addAttr(sourceNodeAttr, **{'q': True, 'dt': True})[0] == 'string':
        attrDict['dt'] = 'string'
    if targetParentAttr:
        attrDict['p'] = targetParentAttr
    
    cmds.addAttr(targetDriver, **attrDict)
    for childAttr in \
                    cmds.attributeQuery(origAttr, node=sourceDriver, lc=True) or []:
        createDriverAttrFunc(sourceDriver, targetDriver, childAttr,
                             drAttrSearch, drAttrReplace, skipRecursion=True)
    for childAttr in \
                    cmds.attributeQuery(origAttr, node=sourceDriver, lc=True) or []:
        childKeyable = cmds.getAttr(
            "%s.%s" % (sourceDriver, childAttr), k=True)
        if childKeyable:
            try:
                cmds.setAttr("%s.%s" % (targetDriver,
                                        childAttr.replace(drAttrSearch, drAttrReplace)),
                             e=True, keyable=True)
            except:
                pass
    
    if keyable:
        try:
            cmds.setAttr(targetNodeAttr, e=True, keyable=True)
        except:
            pass


def doSDKs(SDKnodes, target, search, replace, i, iterExec, specialIter,
           SDKResults, BWNResults, mode, createDriverAttr,
           drAttrSearch, drAttrReplace):
    ''' This is the procedure that actually performs the SDK replication
    '''
    
    # Declare search direction of connectionInfo command, based of tool mode.
    if mode:
        conInfoLambda = lambda node: cmds.listConnections(
            '%s.input' % node[0], d=False, s=True, p=True, scn=True)
    else:
        conInfoLambda = lambda node: cmds.listConnections(
            '%s.output' % node[0], d=True, s=False, p=True, scn=True)
    
    for node in SDKnodes:
        
        # Check what's connected to SDK nodes and see if the target nodes
        # have the same attributes as the source node, if no reults or
        # no matching attributes, continue.
        connections = conInfoLambda(node)
        if not connections or (not createDriverAttr and (
                    not cmds.attributeQuery(
                        node[1].replace(drAttrSearch, drAttrReplace),
                        node=target, ex=True) and
                    not cmds.attributeQuery(
                        node[1].split('[')[0].replace(drAttrSearch, drAttrReplace),
                        node=target, ex=True))):
            print 'CONTINUED', node  # delete me
            continue
        
        # If createDriverAttr is set to True and the driver attribute
        # doesn't exist, try to create it on the new driver.
        elif (not cmds.attributeQuery(
                node[1].replace(drAttrSearch, drAttrReplace),
                node=target, ex=True) and
                  not cmds.attributeQuery(
                      node[1].split('[')[0].replace(drAttrSearch, drAttrReplace),
                      node=target, ex=True)):
            if mode or not createDriverAttr:
                continue
            sourceDriver = cmds.listConnections(
                '%s.input' % node[0],
                d=False, s=True, p=False, scn=True)[0]
            createDriverAttrFunc(sourceDriver, target, node[1].split('[')[0],
                                 drAttrSearch, drAttrReplace)
        
        if isinstance(connections, str):
            connections = [connections]
        
        # Duplicate keyframe node and mirror if asked.
        newKeyNode = cmds.duplicate(node[0])[0]
        if node[2]:
            mirrorKeys(newKeyNode)
        
        # Go through all the connections.
        for curNode in connections:
            
            # If in driver mode, check to see if node connected to keyframe
            # is a blendWeighted node.
            origBW = ''
            if not mode:
                nodeType = cmds.ls(curNode.split('.')[0], st=True)[1]
                if nodeType == 'blendWeighted':
                    origBW = curNode
                    connections2 = cmds.listConnections(
                        '%s.output' % curNode.split('.')[0],
                        d=True, s=False, p=True, scn=True)
                else:
                    connections2 = [curNode]
            else:
                connections2 = [curNode]
            
            # Connect the duplicated keyframes
            # to their respective target connections.
            for curNode2 in connections2:
                if search or not mode:
                    # regex search pattern section.
                    curRegexer = re.search(search, curNode2)
                    errorCheck = False
                    print (replace, iterExec, curNode,
                           curNode2, mode, newKeyNode, origBW)  # delete me
                    if hasattr(curRegexer, 'group'):
                        repPattern = curRegexer.group(0)
                        if repPattern:
                            (errorCheck, newConn) = \
                                connectToConn(replace, iterExec, curNode,
                                              curNode2, repPattern, mode, newKeyNode, origBW)
                        else:
                            errorCheck = True
                    else:
                        errorCheck = True
                    
                    if errorCheck:
                        if mode:
                            print ('\nFailure to find a driver for node %s '
                                   'based on search criteria %s for driver node %s .'
                                   % (target, search, curNode2.split('.')[0]))
                            cmds.delete(newKeyNode)
                        else:
                            print ('\nFailure to find a driven for nodes %s '
                                   'based on search criteria %s for driven node %s .'
                                   % (target, search, curNode2.split('.')[0]))
                        continue
                
                elif mode:
                    cmds.connectAttr(curNode2, '%s.input' % newKeyNode, f=True)
                    newConn = curNode2
                
                # Connect the new SDK's to the new driver attrs.
                if mode:
                    cmds.connectAttr('%s.output' % newKeyNode,
                                     '%s.%s' % (target, node[1]), f=True)
                else:
                    cmds.connectAttr('%s.%s' % (target,
                                                node[1].replace(drAttrSearch, drAttrReplace)),
                                     '%s.input' % newKeyNode, f=True)
                
                SDKResults.append('Connected Driver node %s.%s.output to '
                                  'Driven node %s.%s .' %
                                  (newConn, '.'.join(curNode2.split('.')[1:]), target, node[1]))


def mirrorSelectedChannels(node=None, attrs=None, mode='driver'):
    ''' Mirror any keyrames found in the specified attributes on these node.
    If no nodes and attrs are specified, the selection list is used, and
    whatever channels are specified in the channel box are used.

    mode determines whether the command will look for keyframes that are
    driving the attribute, or are driven by an attribute (driver, driven).

    This is meant as more of a convenience function to adjust SDK's after
    they've been copied.
    '''
    
    if not node:
        nodes = cmds.ls(sl=True)
    if not attrs:
        attrs = cmds.channelBox('mainChannelBox', q=True, sma=True) or []
    
    if not nodes:
        print ('No nodes specified to flip.')
        return
    
    for node in nodes:
        if cmds.ls(node, st=True)[1] in ANIM_CURVE_TYPES:
            mirrorKeys(node)
        for attr in attrs:
            if not cmds.attributeQuery(attr, node=node, ex=True):
                continue
            if mode == 'driver':
                source, destination = False, True
            elif mode == 'driven':
                source, destination = True, False
            
            keyframes = [x for x in cmds.listConnections(
                '%s.%s' % (node, attr), scn=True, d=destination,
                s=source, p=False) or []
                         if cmds.ls(x, st=True)[1] in ANIM_CURVE_TYPES]
            for keyframe in keyframes:
                mirrorKeys(keyframe)


def mirrorKeys(newKeyNode):
    '''Mirror keyframe node procedure, in case you need to flip your SDK's.
    Also works with ordinary keyframe nodes.
    '''
    
    keyType = cmds.ls(newKeyNode, st=True)[1]
    try:
        cmds.selectKey(clear=True)
    except:
        pass
    
    # Get the number of keyframes.
    numKeys = len(cmds.listAttr(newKeyNode + '.ktv', multi=True)) / 3
    
    # Iterate through each key and multiply the values by -1,
    # then set the keyframe value.
    for x in range(0, numKeys):
        v = cmds.getAttr(newKeyNode + '.keyTimeValue[' + str(x) + ']')
        v = [v[0][0], v[0][1] * -1]
        if keyType in ('animCurveTU', 'animCurveTA', 'animCurveTL'):
            cmds.selectKey(newKeyNode, add=True, k=True, t=(v[0], v[0]))
        elif keyType in ('animCurveUU', 'animCurveUA', 'animCurveUL'):
            cmds.selectKey(newKeyNode, add=True, k=True, f=(v[0], v[0]))
        
        if keyType in ('animCurveTA', 'animCurveUA'):
            cmds.keyframe(animation='keys', absolute=True,
                          valueChange=math.degrees(v[1]))
        else:
            cmds.keyframe(animation='keys', absolute=True, valueChange=v[1])
        try:
            cmds.selectKey(clear=True)
        except:
            pass


copySDK([], [], '', [],search='Lf_', replace='Rt_')