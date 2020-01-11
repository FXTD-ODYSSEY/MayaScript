# -*- coding: utf-8 -*-

#####################################################################################
#
# Spring Magic for Maya
#
# Calculate bone chain animation by settings, support collisions and wind force
# Can work with rigging controller as well
#
# Need pringMagic.ui file to work with
# This script need also icon file support, which should be put in same folder
# 
# feel free to mail me redtank@outlook.com for any bug or issue
#
# Yanbin Bai
# 2017.10
#
#####################################################################################

############################
# Build History
############################

# 3.2
# - fix wind effect cannot set key issue

# 3.1
# - add bind controller
# - add wind
# - add flex setting
# - improve performance
# - fix twist bug
# - add capsule icon
# - seperate skinTools to spring magic and skin magic

# 3.0
# - re-write spring magic to improve performance
# - add capsule collision for spring magic
# - add donate page

# 2.7.8
# - fix script stop working issue cause by highend3d.com changed their web page

# 2.7.7
# - add time out for update checking in case of network issue

# 2.7.6
# - fix spring magic calculation issue on MAYA 2016
# - update UI for MAYA 2016
# Thanks for all the help from Nobuyuki Kobayashi nobuyuki@unity3d.com

# 2.7.5
# - add floor collision to spring magic

# 2.7
# - Add spring magic



#################
# Imports
#################

import os
import time
import subprocess
import math
import sys
import inspect
import pickle
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import webbrowser
import re
from string import ascii_lowercase
from string import ascii_uppercase
from itertools import chain
import pymel.core.datatypes as dt
import copy
import urllib2
from shutil import copyfile
import random
from itertools import izip
import datetime


SM_version = 30200

SM_scriptName = inspect.getframeinfo(inspect.currentframe()).filename
SM_scriptPath = os.path.dirname(os.path.abspath(SM_scriptName))

# Parameter Initialization 
SM_MainUIFile = SM_scriptPath+os.sep+'springMagic.ui'
SM_paypalLink = r'https://www.paypal.me/Yanbin'
SM_linkedinLink = r'https://ca.linkedin.com/in/baiyanbin'
SM_vimeoLink = r''
SM_bilibiliLink = r'https://animbai.com/zh/2017/10/14/skintools-tutorials/'
SM_youtubeLink = r'https://animbai.com/2017/10/14/skintools-tutorials/'
SM_bitcoin = r'1HT1L4tGobHVmJJZMsj2GG1oZRaowedwUs'
SM_updateLink = r'https://animbai.com/category/download/'
SM_versionCheckLink = r'http://animbai.com/skintoolsver/'
SM_spam_word = ['','','','','']

############################################
# Utility Functions
############################################

# to get object parrent
# parent = obj.getParent()

# to get all parents of a joint
# parentList = joint.getAllParents() 

# to get root bone
# rootBone = joint.root()

# to get object all children
# children = pm.listRelatives( obj, allDescendents = 1)

# to make sure the selection is a mesh
# pm.nodeType(pm.ls(sl=1, type='transform')[0].getShape()) == 'mesh'

# to get vertex in selection as flatten
# pm.ls(sl=1, type='float3', flatten=True)[0]

# to get skin cluster
# pm.listHistory( pm.ls(sl=1), type='skinCluster' )[0]

# to get all influcent bone of a skin cluster
# obj.getInfluence()

# About path module

# from pymel.util.path import path
# filePath = 'c:/temp/test/myTestFile.txt'
# fpPathObj = path(filePath)
# fpPathObj
# # Result: path('c:/temp/test/myTestFile.txt') #
# fpPathObj.basename()
# # Result: 'myTestFile.txt' #
# # .name is a property which returns the same
# fpPathObj.name
# # Result: 'myTestFile.txt' #
# # namebase returns fileName only w/o extension
# fpPathObj.namebase
# # Result: 'myTestFile' #
# # return directory above file
# fpPathObj.parent
# # Result: path('c:/temp/test') #
# # check extension
# fpPathObj.endswith('txt')
# # Result: True #
# # check existance
# fpPathObj.exists()
# # Result: True #
# # check to see if folder type
# fpPathObj.parent.isdir()
# # Result: True #
# fpPathObj.parent.parent.name
# # Result: 'temp' # 



#############################################
#Button respons
############################################

def SM_showSpam():
    sWrod = SM_spam_word[random.randint(0,4)]
    # print as unicode
    SM_printTextLable( SM_main_processLable, unicode(sWrod, "utf8", errors="ignore") )


def SM_linkinCmd( ignoreInputs ):
    # open my linked in page :)
    url = SM_linkedinLink

    webbrowser.open(url,new=2)



def springPasteCmd( ignoreInputs ):
    pass

def springSetCmd( ignoreInputs ):
    springMutipleChain(op='bindPose')

def springStraightCmd( ignoreInputs ):
    springMutipleChain(op='straight')

def springApplyCmd( ignoreInputs ):
    springMutipleChain(op='apply')

def springCopyCmd( ignoreInputs ):
    copyBonePose()

def springPasteCmd( ignoreInputs ):
    pasteBonePose()

def springWebCmd( ignoreInputs ):
    # open my linked in page :)
    url = r"http://www.scriptspot.com/3ds-max/scripts/spring-magic"

    webbrowser.open(url,new=2)

def springTwistChangeCmd( ignoreInputs = False ):
    SM_limitTextEditValue(springXspring_lineEdit, defaultValue = 0.7)

def springChangeCmd( ignoreInputs = False ):
    SM_limitTextEditValue(springSpring_lineEdit, defaultValue = 0.7)

def springTensionChangeCmd( ignoreInputs = False ):
    SM_limitTextEditValue(springTension_lineEdit, defaultValue = 0.5)

def springSubDivChangeCmd( ignoreInputs = False ):
    # SM_limitTextEditValue(springSubDiv_lineEdit, defaultValue = 1)
    pass

def springAddWindCmd( ignoreInputs ):
    springAddWindObj()

def springAddBodyCmd( ignoreInputs ):
    springAddBody()

def springRemoveBodyCmd( ignoreInputs ):
    springRemoveBody(clear=False)

def springClearBodyCmd( ignoreInputs ):
    springRemoveBody(clear=True)

def springBindControllerCmd( ignoreInputs ):
    springBindController()

def springClearBindCmd( ignoreInputs ):
    springClearBind()

def SM_goShelfCmd( ignoreInputs ):
    SM_goShelf()

def SM_languageCmd( ignoreInputs ):
    if SM_language_list.getVisible():
        SM_language_list.setVisible(False)
    else:
        SM_language_list.setVisible(True)

def SM_languageSelectedCmd( ignoreInputs = False ):
    SM_language_list.setVisible(False)
    SM_applyLanguage(int(SM_language_list.getSelectIndexedItem()[0]))


def SM_bilibiliCmd( ignoreInputs ):
    url = SM_bilibiliLink

    try:
        webbrowser.open(url,new=2)
    except:
        pass

def SM_youtubeCmd( ignoreInputs ):
    url = SM_youtubeLink

    try:
        webbrowser.open(url,new=2)
    except:
        pass
def SM_vimeoCmd( ignoreInputs ):
    # url = SM_vimeoLink

    # try:
    #     webbrowser.open(url,new=2)
    # except:
    #     pass
    pass

def SM_donatePayPal_buttonCmd( ignoreInputs ):
    url = SM_paypalLink

    try:
        webbrowser.open(url,new=2)
    except:
        pass    

def SM_dockScriptEditorCmd( ignoreInputs ):

    try:
        pm.deleteUI('scriptEditorPanel1Window')

    except:
        pass

    pm.dockControl(area = 'right', content = 'scriptEditorPanel1Window', width = 500, label = 'Scripts Editor', r = True)

# def renameUpdatePreview():
#     renameUpdatePreview_real( initial = True )


def SM_updatePageCmd( ignoreInputs ):
    # open creative crash page
    url = SM_updateLink

    try:
        webbrowser.open(url,new=2)
    except:
        pass


def SM_applyLanguage(lanId):
    lanDict = {
                1:'_chn',
                2:'_eng',
                3:'_jpn' 
                }
    if lanId in lanDict.keys():
        # get new language ui file path
        newUIFile = SM_scriptPath+os.sep+os.path.basename(SM_MainUIFile).split('.')[0]+lanDict[lanId]+'.'+os.path.basename(SM_MainUIFile).split('.')[1]
        copyfile(newUIFile,SM_MainUIFile)
        
    execfile(SM_scriptPath+os.sep+'springMagic.py')


def SM_detectMayaLanguage():
    mayaLan = None
    try:
        mayaLan = os.environ['MAYA_UI_LANGUAGE']
    except:
        import locale
        mayaLan = locale.getdefaultlocale()[0]

    if mayaLan == 'en_US':
        SM_applyLanguage(2)
    elif mayaLan == 'zh_CN':
        SM_applyLanguage(1)
    elif mayaLan == 'ja_JP':
        SM_applyLanguage(3)





##########################
#Main Part
##########################









def SM_printTextEdit( textEdit, inputString ):
    ctime = time.ctime()
    ptime = ctime.split(' ')
    inputString = ptime[3] + '  -  ' + inputString
    pm.scrollField(
                    textEdit,
                    edit = True,
                    insertionPosition = 0,
                    insertText  = inputString + '\n'
                    )


def SM_printTextLable( label, inputString ):
    pm.text(
            label,
            edit = True,
            label = inputString
            )

SM_realProgress = 0

def SM_runProgressBar( bar, inputNumber = 0.0 ):
#process ProgressBar
    global SM_realProgress
    if 0 < inputNumber < 100:
        SM_realProgress = SM_realProgress + inputNumber        
        pm.progressBar( bar, edit = True, progress = SM_realProgress )
    else:
        SM_realProgress = 0
        pm.progressBar( bar, edit = True, progress = inputNumber )

def SM_setProgressBar( bar, inputNumber ):
    if 0 <= inputNumber <= 100:
        pm.progressBar( bar, edit = True,  progress = inputNumber )
    elif inputNumber < 0:
        pm.progressBar( bar, edit = True, progress = 0 )
    else:
        pm.progressBar( bar, edit = True, progress = 100 )




####################################
#Build UI
####################################






try:
    pm.deleteUI(SM_MainUI)

except:
    pass

# title = pm.window( pm.loadUI( uiFile = SM_MainUIFile ))

SM_MainUI = pm.loadUI( uiFile = SM_MainUIFile )

SM_centralwidget = SM_MainUI + '|centralwidget'
SM_spring_tab = SM_centralwidget + '|main_tab|spring_tab'
SM_donate_tab = SM_centralwidget + '|main_tab|donate_tab'

#Main UI
SM_main_progressBar = SM_centralwidget + '|main_progressBar'
SM_main_processLable = SM_centralwidget + '|main_processLable'
SM_main_lineEdit = SM_centralwidget + '|main_textEdit'
SM_lang_id = pm.text( SM_centralwidget + '|main_lang_id', edit = True )

SM_language_list = pm.textScrollList( SM_centralwidget + '|spring_language_list', edit = True )

springSpring_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|springSpring_lineEdit', edit = True )
springSubs_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|springSubs_lineEdit', edit = True )
springXspring_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|springXspring_lineEdit', edit = True )
springTension_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|springTension_lineEdit', edit = True )
springExtend_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|springExtend_lineEdit', edit = True )
springSubDiv_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|keyRange_groupBox|springSubDiv_lineEdit', edit = True )
springLoop_checkBox = pm.checkBox( SM_spring_tab + '|spring_groupBox|keyRange_groupBox|springLoop_checkBox', edit = True )
springClearSubFrame_checkBox = pm.checkBox( SM_spring_tab + '|spring_groupBox|keyRange_groupBox|springClearSubFrame_checkBox', edit = True )
springFrom_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|keyRange_groupBox|springFrom_lineEdit', edit = True )
springEnd_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|keyRange_groupBox|springEnd_lineEdit', edit = True )
springActive_radioButton = pm.radioButton( SM_spring_tab + '|spring_groupBox|keyRange_groupBox|springActive_radioButton', edit = True )
springFrom_radioButton = pm.radioButton( SM_spring_tab + '|spring_groupBox|keyRange_groupBox|springFrom_radioButton', edit = True )
# springUpAxis_comboBox = pm.optionMenu( SM_spring_tab + '|spring_groupBox|springUpAxis_comboBox', edit = True )
springApply_Button = pm.button( SM_spring_tab + '|spring_groupBox|springApply_Button', edit = True )

springCollision_checkBox = pm.checkBox( SM_spring_tab + '|spring_groupBox|collision_groupBox|springCapsule_checkBox', edit = True )
springFastMove_checkBox = pm.checkBox( SM_spring_tab + '|spring_groupBox|collision_groupBox|springFastMove_checkBox', edit = True )
springFloor_checkBox = pm.checkBox( SM_spring_tab + '|spring_groupBox|collision_groupBox|springFloor_checkBox', edit = True )
springFloor_lineEdit = pm.textField( SM_spring_tab + '|spring_groupBox|collision_groupBox|springFloor_lineEdit', edit = True )

springBindPose_button = pm.button( SM_spring_tab + '|spring_groupBox|springBonePose_groupBox|springBindPose_button', edit = True )
springStraight_button = pm.button( SM_spring_tab + '|spring_groupBox|springBonePose_groupBox|springStraight_button', edit = True )
springCopy_button = pm.button( SM_spring_tab + '|spring_groupBox|springBonePose_groupBox|springCopy_button', edit = True )
springPaste_button = pm.button( SM_spring_tab + '|spring_groupBox|springBonePose_groupBox|springPaste_button', edit = True )


# donate UI
donateSM_Bitcoin_lineEdit = pm.textField( SM_donate_tab + '|eng_groupBox|donateBitcoin_lineEdit', edit = True )
donateSM_Bitcoin_lineEdit.setText(SM_bitcoin)


SM_miscUpdate_button = pm.button( SM_centralwidget + '|miscUpdate_pushButton', edit = True )

SM_showSpam()

SM_runProgressBar( SM_main_progressBar, 0 )

pm.showWindow( SM_MainUI )

# print type(SM_centralwidget)

def SM_resetUI():
#reset UI valve to default
    #Main part
    SM_showSpam()

    SM_runProgressBar( SM_main_progressBar, 0 )

    SM_printTextEdit( SM_main_lineEdit, 'UI Reseted' )

    # weight_paintVertexCheckBox.setValue( False )
    pm.select( clear = True )
    # lodReset()



#########################
# Check update
########################


def SM_find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def SM_checkUpdate():
    global SM_spam_word

    SM_miscUpdate_button.setVisible(0)

    page_source = None

    try:
        page_source = urllib2.urlopen(SM_versionCheckLink, timeout = 5).read()
    except:
        pass

    if page_source:
        if len(page_source.split('|springMagic|'))>1:
            new_SM_version = int(page_source.split('|springMagic|')[1])

            if new_SM_version > SM_version:
                SM_miscUpdate_button.setVisible(1)
            SM_spam_word=[]
            if SM_lang_id.getLabel() == 'chn':
                SM_spam_word.append(page_source.split('|spam1chn|')[1])
                SM_spam_word.append(page_source.split('|spam2chn|')[1])
                SM_spam_word.append(page_source.split('|spam3chn|')[1])
                SM_spam_word.append(page_source.split('|spam4chn|')[1])
                SM_spam_word.append(page_source.split('|spam5chn|')[1])     
            else:
                SM_spam_word.append(page_source.split('|spam1|')[1])
                SM_spam_word.append(page_source.split('|spam2|')[1])
                SM_spam_word.append(page_source.split('|spam3|')[1])
                SM_spam_word.append(page_source.split('|spam4|')[1])
                SM_spam_word.append(page_source.split('|spam5|')[1])
 
    else:
        SM_printTextLable( SM_main_processLable,
                        'Check update failed, try later.' )

    SM_showSpam()



SM_checkUpdate()




##############################################
#   Misc
##############################################





def SM_goShelf():
    parentTab = mel.eval('''global string $gShelfTopLevel;string $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;''')
    pm.shelfButton( commandRepeatable = True, image1 = SM_scriptPath+os.sep+"icons"+os.sep+"Title.png", label = "Spring Magic", parent = parentTab,
                    command = "execfile(r'{0}\springMagic.py')".format(SM_scriptPath) )


###################################
# spring magic
####################################
SM_capsuleNameBase = '_collision_capsule'
SM_windObjName = 'spring_wind'
SM_springProxySubFix = '_SpringProxy'

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def distance(a, b):
    return (b-a).length()

def lerp_vec(a,b,t):
    return a*(1-t) + b*t

def dist_to_plane(q, n, d):
    return n.dot(q) - d / n.dot(n)

def dist_to_line(a,b,p):
    ap = p-a
    ab = b-a
    result = a + ap.dot(ab)/ab.dot(ab) * ab
    return distance(result,p)

def is_same_side_of_plane(pt, test_pt, n, d):
    d1 = math.copysign(1, dist_to_plane(pt, n, d))
    d2 = math.copysign(1, dist_to_plane(test_pt, n, d))

    # print(pt, test_pt, d1,d2)
    return d1 * d2 == 1.0

def proj_pt_to_plane(pt, n, d):
    t = n.dot(pt) - d
    return pt - n*t

def pt_in_sphere(pt, c, r):
    return (pt-c).length() <= r

def pt_in_cylinder(pt, p, q, r):
    n = (q-p).normal()
    d = n.dot(p)
    if not is_same_side_of_plane(pt, (p+q)/2.0, n, d):
        return False
    n = (q-p).normal()
    d = n.dot(q)
    if not is_same_side_of_plane(pt, (p+q)/2.0, n, d):
        return False

    proj_pt = proj_pt_to_plane(pt, n, d)
    # print("proj_pt",proj_pt)
    # print("q",q)
    # print("distance(proj_pt,q)", distance(proj_pt,q))
    return distance(proj_pt,q) <= r

def segment_sphere_isect(sa, sb, c, r):
    NotFound = (False, None)
    
    p = sa
    d = (sb-sa).normal()

    m = p - c
    b = m.dot(d)
    c = m.dot(m) - r * r

    if c > 0.0 and b > 0.0:
        return NotFound

    discr = b*b - c
    if discr < 0.0:
        return NotFound

    t = -b - math.sqrt(discr)
    if t < 0.0:
        return NotFound

    dist = distance(sa, sb)
    q = p + d * t
    return ((t>=0 and t<=dist), q)


def segment_cylinder_isect(sa, sb, p, q, r):
    SM_EPSILON = 1e-6
    d = q-p
    m = sa-p
    n = sb-sa
    md = m.dot(d)
    nd = n.dot(d)
    dd = d.dot(d)

    NotFound = (False, None)
    if md < 0 and md + nd < 0:
        return NotFound

    if md > dd and md + nd > dd:
        return NotFound

    nn = n.dot(n)
    mn = m.dot(n)

    a = dd*nn - nd*nd
    k = m.dot(m) - r*r
    c = dd*k - md*md

    if abs(a) < SM_EPSILON:
        if c > 0:
            return NotFound
        if md < 0:
            t = -mn / nn
        elif md > dd:
            t = (nd - mn) / nn
        else:
            t = 0
        return (True, lerp_vec(sa, sb, t))

    b = dd*mn - nd*md
    discr = b*b - a*c
    if discr < 0:
        return NotFound

    t = (-b - math.sqrt(discr)) / a;
    if t < 0.0 or t > 1.0:
        return NotFound
    if (md + t * nd < 0.0):
        if nd <= 0.0:
            return NotFound
        t = -md / nd;
        return (k + 2 * t * (mn + t * nn) <= 0.0,
                lerp_vec(sa, sb, t))
    elif md + t * nd > dd:
        if nd >= 0.0:
            return NotFound
        t = (dd - md) / nd;
        return (k + dd - 2 * md + t * (2 * (mn - nd) + t * nn) <= 0.0,
                lerp_vec(sa, sb, t))

    return (True, lerp_vec(sa, sb, t))

def pt_in_capsule(pt, p, q, r):
    return pt_in_cylinder(pt, p, q, r) or pt_in_sphere(pt, p, r) or pt_in_sphere(pt, q, r)

def segment_capsule_isect(sa, sb, p, q, r):
    # sa = dt.Vector()
    #    ray start point pos vector
    # sb = dt.Vector()
    #    ray end point pos vector
    # p = dt.Vector()
    #    capsle one sphere tip pos
    # q = dt.Vector()
    #    capsle another sphere tip pos
    # r = float
    #    radio of capsle sphere

    if pt_in_capsule(sa, p, q, r) and pt_in_capsule(sb, p, q, r):
        # both inside.  extend sb to get intersection
        newb = sa + (sb-sa).normal() * 200.0
        sa, sb = newb, sa
    elif pt_in_capsule(sa, p, q, r):
        sb, sa = sa, sb
    
    d = (sb-sa).normal()

    i1 = segment_sphere_isect(sa, sb, p, r)
    i2 = segment_sphere_isect(sa, sb, q, r)
    i3 = segment_cylinder_isect(sa, sb, p, q, r)

    dist = float('inf')
    closest_pt = None
    hit = False
    hitCylinder = False
    if i1[0]:
        hit = True
        pt = i1[1]
        if distance(sa, pt) < dist:
            closest_pt = pt
        dist = min(dist, distance(sa, pt))
        # draw_locator(i1[2], 'i1')
    if i2[0]:
        hit = True
        pt = i2[1]
        if distance(sa, pt) < dist:
            closest_pt = pt
        dist = min(dist, distance(sa, pt))
    if i3[0]:
        hit = True
        hitCylinder = True
        pt = i3[1]
        if distance(sa, pt) < dist:
            closest_pt = pt
        dist = min(dist, distance(sa, pt))

    return (hit, closest_pt, hitCylinder)

def offsetPosByDirection(sDirection,tPos,moveDistance):
    # get new target pos
    tPos += sDirection*moveDistance

    return tPos

def get_matrix(obj):
    return pm.xform(obj,worldSpace =1,matrix =1,q=1)

def springAddWindObj():
    windCone = pm.cone(name=SM_windObjName)[0]
    windCone.setScale([5,5,5])
    pm.delete(windCone,constructionHistory=1 )
    # add wind attr
    pm.addAttr(windCone,longName='MaxForce',attributeType='float')
    pm.setAttr(windCone.name()+'.MaxForce',1,e=1,keyable=1)
    pm.addAttr(windCone,longName='MinForce',attributeType='float')
    pm.setAttr(windCone.name()+'.MinForce',0.5,e=1,keyable=1)
    pm.addAttr(windCone,longName='Frequency',attributeType='float')
    pm.setAttr(windCone.name()+'.Frequency',1,e=1,keyable=1)
    # pm.addAttr(windCone,longName='Wave',attributeType='float')
    # pm.setAttr(windCone.name()+'.Wave',0.5,e=1,keyable=1)

    setWireShading(windCone,False)

    pm.makeIdentity( apply=True )
    windCone.setRotation([0,0,90])


def springBindController():
    ctrlList = pm.ls(sl=1)
    pm.select( d=True )
    proxyJointLst = []
    for ctrl in ctrlList:
        # create proxy joint in ctrller world position
        ctrlPos = pm.xform(ctrl,worldSpace =1,rp=1,q=1)
        # print ctrlPos
        proxyJoint = pm.joint( 
                            name=ctrl.name()+SM_springProxySubFix,
                            position=ctrlPos
                            )
        pm.setAttr(proxyJoint.name()+'.radius',1.5)
        proxyJointLst.append(proxyJoint)
    for joint in proxyJointLst:
        #set joint oritation
        pm.joint(joint,edit=1,orientJoint ='xyz',zeroScaleOrient =True)
        # preRot = joint.getRotation()
        # preOrient = joint.getAttr('jointOrient')
        # joint.setAttr('jointOrient', [0,0,0])
        # joint.setRotation(preRot+preOrient)
        # joint.setAttr('rotateAxis', preOrient)
        springStraightBonePose(joint)


    if proxyJointLst:
        # parent root proxy joint to controller parent
        pm.parent(proxyJointLst[0],ctrlList[0].getParent())

    for joint in proxyJointLst:
        idx=proxyJointLst.index(joint)
        if idx+1<len(ctrlList):
            cns = pm.aimConstraint( ctrlList[idx+1], proxyJointLst[idx], aimVector = [1,0,0], upVector = [0,0,0], worldUpVector = [0,1,0], skip ='x' )
            pm.delete(cns)
        pm.parentConstraint( proxyJointLst[idx], ctrlList[idx], maintainOffset=True )


def springClearBind():
    proxyJointLst = pm.ls(sl=1)
    pm.select( d=True )
    ctrlList = []

    # get frame range
    if springActive_radioButton.getSelect():
        startFrame = int( pm.playbackOptions( q=1, minTime = 1 ) )
        endFrame = int( pm.playbackOptions( q=1, maxTime = 1 ) )
    else:
        startFrame = int( springFrom_lineEdit.getText() )
        endFrame = int( springEnd_lineEdit.getText() )

    for bone in proxyJointLst:
        ctrl = pm.ls(bone.name().split(SM_springProxySubFix)[0])[0]
        ctrlList.append(ctrl)
    for ctrl in ctrlList:
        pm.bakeResults( ctrl, t=(startFrame,endFrame))

    pm.delete(proxyJointLst)

def getCapsule(getAll):
    if getAll:
        nurbsTransLst = pm.ls(type='transform')
    else:
        nurbsTransLst = pm.ls(sl=1)
    
    nurbsSurfaceLst=[]
    for obj in nurbsTransLst:
        if obj.getShape():
            if pm.nodeType(obj.getShape()) == 'nurbsSurface':
                nurbsSurfaceLst.append(obj)

    cylinderLst = []
    for obj in nurbsTransLst:
        if 'ylinder' in obj.name() and SM_capsuleNameBase in obj.name():
            cylinderLst.append(obj)

    return cylinderLst

def preCheckCollision(objPos,objLength,capsuleLst):
    # pre check bone length compare with collision body radius
    # will improve performance if bone is far from capsule
    for obj in capsuleLst:
        objChildren = pm.listRelatives( obj, children=1, type='transform')
        p = objChildren[0].getTranslation(space='world')
        q = objChildren[1].getTranslation(space='world')
        r = obj.getAttr('scaleZ')*1

        boneToCapsuleDistance = dist_to_line(p,q,objPos)

        if boneToCapsuleDistance<objLength+r:  # means close enough to have a hit change
            return True

    return False

def checkCollision(cur_pos, pre_pos, capsuleLst, isRevert):
    # calculate collision with all the capsule in scene
    if isRevert:
        sa = cur_pos
        sb = pre_pos
    else:
        sb = cur_pos
        sa = pre_pos


    isHited = False
    closest_pt_dict = {}
    for obj in capsuleLst:
        objChildren = pm.listRelatives( obj, children=1, type='transform')
        p = objChildren[0].getTranslation(space='world')
        q = objChildren[1].getTranslation(space='world')
        r = obj.getAttr('scaleZ')*1

        hit, closest_pt, hitCylinder = segment_capsule_isect(sa, sb, p, q, r)


        if hit:
            isHited = True
            closest_pt_dict[obj.name()] = [obj,closest_pt]
            # drawDebug_box(closest_pt)

    if isHited:
        pt_length = 9999
        closest_pt = None
        col_obj = None
        for pt in closest_pt_dict.keys():
            lLength = (closest_pt_dict[pt][1]-pre_pos).length()
            if lLength < pt_length:
                pt_length = lLength
                closest_pt = closest_pt_dict[pt][1]
                col_obj = closest_pt_dict[pt][0]

        # return col pt and col_body speed
        return closest_pt, col_obj, hitCylinder
    else:
        return None, None, None


def setWireShading(obj,tmp):
    obj.getShape().overrideEnabled.set(True)
    obj.getShape().overrideShading.set(False)
    if tmp:
        obj.getShape().overrideDisplayType.set(1)

def addCapsuleSphereConstraint(sphereObj):
    # create a locator and make sphere follow it
    locator = pm.spaceLocator(name=sphereObj.name()+'_locator'+SM_capsuleNameBase)
    locator.setTranslation( sphereObj.getTranslation() )
    locator.setRotation( sphereObj.getRotation() )
    locator.getShape().setAttr('visibility',False)

    pm.parentConstraint( locator, sphereObj )

    return locator

def createCapsuleGeometry(size):
    #create geometry
    cylinder,cylinder_history = pm.cylinder( radius=size, sections=8, heightRatio=3 )
    pm.rename(cylinder.name(),cylinder.name()+SM_capsuleNameBase)
    
    sphereA,sphereA_history = pm.sphere( radius=size, endSweep=180, sections=4 )
    pm.rename(sphereA.name(),sphereA.name()+SM_capsuleNameBase)
    
    sphereB,sphereB_history = pm.sphere( radius=size, endSweep=180, sections=4 )
    pm.rename(sphereB.name(),sphereB.name()+SM_capsuleNameBase)
    
    # set to wireframe shader
    setWireShading(cylinder,False)
    setWireShading(sphereA,True)
    setWireShading(sphereB,True)

    # build a capsule with geometry
    cylinder.setAttr('rotateZ', 90)
    sphereA.setAttr('translateY', -1.5*size)
    sphereB.setAttr('rotateZ', 180)
    sphereB.setAttr('translateY', 1.5*size)

    # add constrain
    locatorA = addCapsuleSphereConstraint(sphereA)
    locatorB = addCapsuleSphereConstraint(sphereB)

    pm.parent(locatorA,cylinder)
    pm.parent(locatorB,cylinder)

    pm.parent(sphereA,cylinder)
    pm.parent(sphereB,cylinder)

    sphereA.setAttr('inheritsTransform',False)
    sphereB.setAttr('inheritsTransform',False)

    pm.connectAttr(cylinder.scaleY,(sphereA_history.name()+'.radius'))
    pm.connectAttr(cylinder.scaleY,(sphereB_history.name()+'.radius'))
    pm.connectAttr(cylinder.scaleY,cylinder.scaleZ)

    return cylinder


def springAddBody():
    # create capsule body for collision
    # place capsule at ori point of nothing selected in scene
    # place capsule match with object position and rotation if select scene object
    collisionBoneList = []
    objs = pm.ls(sl=1)
    for obj in objs:
        children = pm.listRelatives( obj, children  = 1)
        if children:    # only add capsule to the obj whitch has child
            collisionBoneList.append([obj,children[0]])

    if collisionBoneList:
        for couple in collisionBoneList:
            baseBone = couple[0]
            endBone = couple[1]
            capsule = createCapsuleGeometry(1)

            pm.parent(capsule,baseBone)
            # match capsule to bone
            endBoneTrans = endBone.getTranslation()
            capsule.setTranslation(endBoneTrans*0.5)
            capsule.setAttr('scaleX', endBoneTrans[0]/3)
            capsule.setAttr('scaleY', endBoneTrans[0]/3)
            cns = pm.aimConstraint( endBone, capsule, aimVector = [1,0,0] )
            pm.delete( cns )

    else:
        capsule = createCapsuleGeometry(1)
        capsule.setAttr('scaleX', 10)
        capsule.setAttr('scaleY', 10)
        pm.select(clear = 1)

def springRemoveBody(clear=False):
    cylinderLst = getCapsule(clear)

    for obj in cylinderLst:
        pm.delete(obj)

def springBindPose():
    pm.runtime.GoToBindPose()

def springStraightBonePose(bone):
    for obj in pm.ls(sl=1):
        bone.setRotation([0,0,0])
        bone.setAttr('rotateAxis', [0,0,0])
        bone.setAttr('jointOrient', [0,0,0])

def springMutipleChain(op=None):
    if pm.ls(sl=1, type = 'joint'):
        pickedBones = pm.ls(sl=1, type = 'joint')
    else:
        return False
    springApply_Button.setEnable(False)
    if op == 'apply':
        SM_printTextLable( SM_main_processLable, 'Calculating Bone Spring ... Cannot Stop ...' )
        springPrepare()

        # springApply(bone, pickedBones)
    for bone in pickedBones:
        if op == 'bindPose':
            pm.runtime.GoToBindPose()
        elif op == 'straight':
            springStraightBonePose(bone)

    pm.select(pickedBones)
    springApply_Button.setEnable(True)
    # SM_showSpam()





def get_trans(n):
    return dt.Vector( pm.xform(n, worldSpace = 1, translation = 1, query = 1) )

def get_rot(n):
    return pm.xform(n,q=1,worldSpace=1,rotation=1)

def get_node(name):
    a = pm.ls(name)
    if a:
        return a[0]
    else: return None

def aim_by_ratio(obj,prePos,curPos,ratio,upVector,preGrandPos=None,tension=0):

    lct = pm.spaceLocator()
    lct.setTranslation( curPos )

    lct_p = pm.spaceLocator()
    lct_p.setTranslation(prePos)

    if preGrandPos:
        lct_p_g = pm.spaceLocator()
        lct_p_g.setTranslation(preGrandPos)

        cns = pm.aimConstraint( 
                                lct, lct_p, lct_p_g, obj,
                                aimVector = [1,0,0],
                                upVector = [0,1,0],
                                worldUpVector = upVector
                                )
        cns.setAttr(lct+'W0', ratio)
        cns.setAttr(lct_p+'W1', 1-ratio)
        cns.setAttr(lct_p_g+'W2', (1-ratio)*tension)

    else:
        cns = pm.aimConstraint( 
                                lct, lct_p, obj,
                                aimVector = [1,0,0],
                                upVector = [0,1,0],
                                worldUpVector = upVector
                                )
        cns.setAttr(lct+'W0', ratio)
        cns.setAttr(lct_p+'W1', 1-ratio)

    pm.setKeyframe(obj, attribute = 'rotate')

    # pm.delete(cns)
    pm.delete(cns,lct,lct_p)
    if preGrandPos:
        pm.delete(lct_p_g)


def springPrepare():
    # prepare all information to call SpringMagicMaya function

    # get selection obj
    objs = pm.ls(sl=1)

    # check obj vaild
    for obj in objs:
        # has duplicate name obj
        nameCntErr = (len(pm.ls(obj.name()))>1)
        # is a duplicate obj
        nameVaildErr = (obj.name().find('|')>0)
        if nameCntErr or nameVaildErr:
            pm.warning( obj.name()+' has duplicate name objcet! Stopped!' )
            return
        objTrans = obj.getTranslation()
        if objTrans[0]<0 or abs(objTrans[1])>0.001 or abs(objTrans[2])>0.001:
            if obj.getParent():
                if obj.getParent() in objs:
                    pm.warning( obj.getParent().name()+"'s X axis not point to child! May get broken result!" )

    springRatio = 1-float(springSpring_lineEdit.getText())
    twistRatio = 1-float(springXspring_lineEdit.getText())
    isLoop = bool(springLoop_checkBox.getValue())
    isFastMove = springFastMove_checkBox.getValue()
    isCollision = springCollision_checkBox.getValue()
    if isCollision:
        subDiv = float(springSubDiv_lineEdit.getText())
    else:
        subDiv = 1

    # get frame range
    if springActive_radioButton.getSelect():
        startFrame = int( pm.playbackOptions( q=1, minTime = 1 ) )
        endFrame = int( pm.playbackOptions( q=1, maxTime = 1 ) )
    else:
        startFrame = int( springFrom_lineEdit.getText() )
        endFrame = int( springEnd_lineEdit.getText() )

    pm.currentTime( startFrame, edit=True )

    tension=float(springTension_lineEdit.getText())

    extend=float(springExtend_lineEdit.getText())

    wipeSubFrame = springClearSubFrame_checkBox.getValue()

    isWind=False
    windObj=None
    windMaxForce=windMinForce=windFreq=0
    if pm.ls(SM_windObjName):
        isWind = True
        windObj=pm.ls(SM_windObjName)[0]
        windMaxForce=windObj.getAttr('MaxForce')
        windMinForce=windObj.getAttr('MinForce')
        windFreq=windObj.getAttr('Frequency')
        # windWave=windObj.getAttr('Wave')

    calStartTime = datetime.datetime.now()
    SpringMagicMaya(
                        objs,
                        springRatio,
                        twistRatio,
                        tension,
                        extend,
                        subDiv,
                        startFrame,
                        endFrame,
                        isLoop,
                        isCollision,
                        isFastMove,
                        wipeSubFrame,
                        isWind,
                        windObj,
                        windMaxForce,
                        windMinForce,
                        windFreq
                    )
    calDeltaTime = (datetime.datetime.now() - calStartTime)
    SM_printTextLable( SM_main_processLable, "Spring Calculation Time: {0}s".format(calDeltaTime.seconds) )


def SpringMagicMaya(
                        objs,
                        ratio=0.3,
                        twistRatio=0.3,
                        tension=0.5,
                        extend=0.0,
                        subDiv=1.0,
                        startFrame=0,
                        endFrame=1,
                        isLoop=False,
                        isCollision=False,
                        isFastMove=False,
                        wipeSubFrame=True,
                        isWind=False,
                        windObj=None,
                        windMaxForce=0,
                        windMinForce=0,
                        windFreq=0,
                        windWave=0
                    ):
    # on each frame go through all objs and do:
    # 1. make a vectorA from current obj position to previouse child position
    # 2. make a vectorB from current obj position to current child position
    # 3. calculate the angle between two vectors
    # 4. rotate the obj towards vectorA base on spring value


    ratio /= subDiv
    twistRatio /= subDiv
    tension /= 1/(sigmoid(1-subDiv)+0.5)
    # extend /= subDiv
    # initial var
    isSeconendPath = False
    nullSubFix = '_SpringNull'
    pm.delete(pm.ls( '*'+nullSubFix+'*', recursive =1))
    # twistNullSubFix = '_SpringTwistNull'
    # loop frame
    obj_trans_dict = {} # use a dict to restore obj previous frame trans information

    capsuleLst = getCapsule(True) # get all capsule in scene
    boneNum = len(objs)*1.0

    i = 0.0
    SM_setProgressBar(SM_main_progressBar,0.0)

    while i < ((endFrame-startFrame)+(1/subDiv)):

        # print 'Frame',i

        pm.currentTime( startFrame+i, edit=True )
        # calculate obj
        for obj in objs:
            objIndex = objs.index(obj)
            if len(obj.listRelatives(children = True))>0 and (obj.getParent() is not None):     # skip end bone and root bone
                child = grandChild = None
                if obj.listRelatives(children = True,type='joint'):
                    child = obj.listRelatives(children = True,type='joint')[0]
                if child:

                    # grand child for tension
                    if child.listRelatives(children = True,type='transform'):
                        grandChild = child.listRelatives(children = True,type='transform')[0]


                    if i > 0 or isSeconendPath:     # only skip first frame of first calculation path

                        # pm.currentTime( startFrame+i, edit=True )  # goto current frame

                        # get previous frame position of obj and child
                        prev_obj_pos = obj_trans_dict[obj][0]
                        prev_child_pos = obj_trans_dict[obj][1]
                        prev_grandChild_pos = obj_trans_dict[obj][3]

                        hasChildCollide = obj_trans_dict[obj][4]
                        boneLength = obj_trans_dict[obj][5]
                        # get prev_rot for twist
                        prev_rot = obj_trans_dict[obj][2]

                        # get current frame position of obj and child
                        cur_obj_pos = get_trans(obj)

                        objNull = get_node(obj.name()+nullSubFix)
                        # print get_trans(objNull)
                        cur_child_pos = get_trans(objNull)
                        # get cur_rot for twist
                        cur_rot = get_rot(objNull)


                        # apply wind
                        if isWind:
                            windMaxForce=windObj.getAttr('MaxForce')
                            windMinForce=windObj.getAttr('MinForce')
                            windFreq=windObj.getAttr('Frequency')

                            midForce = (windMaxForce+windMinForce)/2

                            # waveOffset = (objIndex+1.0)/boneNum*2*math.pi*windWave
                            # # moveDistance /= subDiv
                            # # prev_child_pos = offsetPosByDirection(windObj,prev_child_pos,moveDistance)

                            # waveDirection = cur_child_pos-prev_child_pos
                            # waveDistance = waveOffset
                            # cur_child_pos = offsetPosByDirection(waveDirection,cur_child_pos,waveDistance)

                            # get source x-axis direction in world space
                            windDirection = pm.xform(windObj,worldSpace =1,matrix =1,q=1)[:3]
                            # sDirection = sObj.getMatrix()[0][:3]
                            windDirection = dt.Vector(windDirection[0],windDirection[1],windDirection[2]).normal()
                            windDistance = math.sin(i*windFreq)*(windMaxForce-windMinForce)+midForce

                            cur_child_pos = offsetPosByDirection(windDirection,cur_child_pos,windDistance)

                            # print prev_child_pos

                        # detect collision
                        col_pre = col_cur = None

                        if isCollision and capsuleLst:
                            if preCheckCollision(cur_obj_pos,boneLength,capsuleLst):
                                # check col from previous pos to cur pos
                                col_pre, col_body_pre, hitCylinder_pre = checkCollision(cur_child_pos, prev_child_pos, capsuleLst, True)
                                # check col from cur pos to previous pos

                                col_cur, col_body_cur, hitCylinder_cur = checkCollision(cur_child_pos, prev_child_pos, capsuleLst, False)

                                # if col_pre == none and col_cur == ture 
                                #   means previous pos is in side col body, move pre pos to col_cur
                                # if col_pre == ture and col_cur == none 
                                #   means cur pos is in side col body, move cur pos to col_pre
                                # if both none 
                                #   means no collision, do nothing
                                # if both true
                                #   means move path the col body or both pos are inside body, move cur pos to col_cur

                                # ratio = ori_ratio
                                # childDistance = distance(prev_child_pos,cur_child_pos)


                                if col_pre and (col_cur == None):
                                    cur_child_pos = col_pre

                                elif col_cur and (col_pre == None):
                                    prev_child_pos = col_cur

                                elif col_pre and col_cur:

                                    # move cur child pose to closest out point if both pre and cur pos are already inside of col body
                                    # if distance(col_pre, cur_child_pos) < distance(col_cur, cur_child_pos):
                                    midPoint = (prev_child_pos+cur_child_pos)/2
                                    if distance(col_pre, midPoint) < distance(col_cur, midPoint):
                                        cur_child_pos = col_pre
                                        if isFastMove:
                                            prev_child_pos = col_pre

                                    else:
                                        cur_child_pos = col_cur
                                        if isFastMove:
                                            prev_child_pos = col_cur

                                # # draw debug locator
                                # if col_pre and col_cur:
                                #     locator1 = pm.spaceLocator(name=obj.name()+'_col_pre_locator_'+str(i))
                                #     locator1.setTranslation( col_pre )
                                #     locator1 = pm.spaceLocator(name=obj.name()+'_col_cur_locator_'+str(i))
                                #     locator1.setTranslation( col_cur )


                        # calculate upvector by interpolation y axis for twist
                        prev_obj_yAxis = obj_trans_dict[obj][6]
                        cur_obj_yAxis = get_matrix(objNull)[4:7]
                        prev_upVector = dt.Vector(prev_obj_yAxis[0],prev_obj_yAxis[1],prev_obj_yAxis[2]).normal()
                        cur_upVector = dt.Vector(cur_obj_yAxis[0],cur_obj_yAxis[1],cur_obj_yAxis[2]).normal()

                        upVector = prev_upVector*(1-twistRatio)+cur_upVector*(twistRatio)


                        # apply aim constraint to do actual rotation
                        if tension>0 and prev_grandChild_pos and hasChildCollide:
                            aim_by_ratio(obj, prev_child_pos, cur_child_pos, ratio, upVector, prev_grandChild_pos, tension)
                        else:
                            aim_by_ratio(obj, prev_child_pos, cur_child_pos, ratio, upVector)
                        r = get_rot(obj)
                        upVector = get_matrix(obj)[4:7]

                        if extend != 0.0:
                            childT = child.getTranslation()
                            # get length between bone pos and previous child pos
                            x2 = (prev_child_pos-get_trans(obj)).length()
                            x3 = boneLength*(1-extend) + x2*extend
                            child.setTranslation([x3,childT[1],childT[2]])
                            pm.setKeyframe(child, attribute = 'tx')


                        # else:
                        #     child.setTranslation([boneLength,childT[1],childT[2]])



                        # restore for next frame
                        cur_obj_pos = get_trans(obj)
                        cur_child_pos = get_trans(child)
                        cur_grandChild_pos = False
                        if prev_grandChild_pos:
                            cur_grandChild_pos = get_trans(grandChild)
                        # change parent obj hasChildCollide value
                        if col_pre or col_cur:
                            hasChildCollide = True
                        else:
                            hasChildCollide = False
                        if obj.getParent() in obj_trans_dict.keys():
                            obj_trans_dict[obj.getParent()][4] = hasChildCollide
                        obj_trans_dict[obj] = [cur_obj_pos,cur_child_pos,r,cur_grandChild_pos,hasChildCollide,boneLength,upVector]


                    else:

                        # creat a null at child pos, then parent to obj parent for calculation
                        null = pm.spaceLocator(name=obj.name()+nullSubFix)
                        null.setTranslation( child.getTranslation(space='world') )
                        null.setRotation( child.getRotation(space='world') )
                        null.getShape().setAttr('visibility',False)
                        pm.parent(null, obj.getParent())

                        # remove exists keys
                        pm.cutKey( obj, time=(startFrame, endFrame+0.99999) )
                        pm.cutKey( child, time=(startFrame, endFrame+0.99999) )
                        
                        # set key
                        pm.setKeyframe(obj, attribute = 'rotate')
                        if extend != 0.0:
                            pm.setKeyframe(child, attribute = 'tx')
                        # get initial position of obj and child
                        prev_obj_pos = get_trans(obj)
                        prev_obj_yAxis = get_matrix(obj)[4:7]
                        prev_child_pos = get_trans(child)
                        boneLength = distance(prev_obj_pos,prev_child_pos)
                        prev_grandChild_pos = False
                        boneStartRotation = obj.getRotation()
                        lastShort = False

                        if grandChild:
                            prev_grandChild_pos = get_trans(grandChild)

                        # get prev_rot for twist
                        prev_rot = get_rot(obj)
                        # obj.GetVector(prev_rot, FBModelTransformationType.kModelRotation)

                        # restore obj trans information
                        obj_trans_dict[obj] = [prev_obj_pos, prev_child_pos, prev_rot, prev_grandChild_pos, False, boneLength,prev_obj_yAxis]

                        # print obj_trans_dict[obj]


        i += 1/subDiv

        jj=1.0
        kk = 0.0
        if isLoop:
            jj=2
        if isSeconendPath:
            kk = 50.0
        SM_setProgressBar(SM_main_progressBar,float(i)/jj/float(endFrame-startFrame+1)*100+kk)

        # print isLoop, startFrame+i+1, endFrame
        if isLoop and (startFrame+i > endFrame) and isSeconendPath == False: # at the end frame of first path
            i = 0   # back to first frame
            isSeconendPath = True   # mark seconed path calculation for loop

    # bake result on frame
    if wipeSubFrame:
        bakeAnim(objs, startFrame, endFrame)

    # remove all spring nulls, add recursive incase name spaces
    pm.delete(pm.ls( '*'+nullSubFix+'*', recursive =1))

    SM_setProgressBar(SM_main_progressBar,0.0)


def bakeAnim(objLst,startFrame,endFrame):
    pm.bakeResults(
                    objLst,
                    t=(startFrame,endFrame),
                    sampleBy =1.0,
                    disableImplicitControl=False,
                    preserveOutsideKeys=True,
                    sparseAnimCurveBake=False,
                    removeBakedAttributeFromLayer=False,
                    bakeOnOverrideLayer=False,
                    minimizeRotation=True,
                    shape=False,
                    simulation=False
                    )

def SM_limitTextEditValue(ui_object, minValue=0, maxValue=1, roundF = 2, defaultValue = 0):
    value = 0
    try:
        value = float(ui_object.getText())
    except:
        ui_object.setText(str(defaultValue))
        return
    if value < minValue:
        ui_object.setText(str(minValue))
    elif value > maxValue:
        ui_object.setText(str(maxValue))
    else:
        ui_object.setText(str(round(float(value),roundF)))

SM_boneTransformDict={}
def copyBonePose():
    global SM_boneTransformDict
    for obj in pm.ls(sl=1):
        SM_boneTransformDict[obj] = [obj.getTranslation(),obj.getRotation()]

def pasteBonePose():
    for obj in pm.ls(sl=1):
        if obj in SM_boneTransformDict.keys():
            print SM_boneTransformDict[obj][0]
            obj.setTranslation(SM_boneTransformDict[obj][0])
            obj.setRotation(SM_boneTransformDict[obj][1])


#############################################
# Initial Scripts
############################################## 


SM_language_list.setVisible(False)

# SM_showSpam()