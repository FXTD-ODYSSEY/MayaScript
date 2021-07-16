"""

 Copyright (C) 2001 - 2010 Autodesk, Inc. and/or its licensors.
 All Rights Reserved.

 The coded instructions, statements, computer programs, and/or related material 
 (collectively the "Data") in these files contain unpublished information 
 proprietary to Autodesk, Inc. and/or its licensors, which is protected by 
 Canada and United States of America federal copyright law and by international 
 treaties. 
 
 The Data may not be disclosed or distributed to third parties, in whole or in
 part, without the prior written consent of Autodesk, Inc. ("Autodesk").

 THE DATA IS PROVIDED "AS IS" AND WITHOUT WARRANTY.
 ALL WARRANTIES ARE EXPRESSLY EXCLUDED AND DISCLAIMED. AUTODESK MAKES NO
 WARRANTY OF ANY KIND WITH RESPECT TO THE DATA, EXPRESS, IMPLIED OR ARISING
 BY CUSTOM OR TRADE USAGE, AND DISCLAIMS ANY IMPLIED WARRANTIES OF TITLE, 
 NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE OR USE. 
 WITHOUT LIMITING THE FOREGOING, AUTODESK DOES NOT WARRANT THAT THE OPERATION
 OF THE DATA WILL BE UNINTERRUPTED OR ERROR FREE. 
 
 IN NO EVENT SHALL AUTODESK, ITS AFFILIATES, PARENT COMPANIES, LICENSORS
 OR SUPPLIERS ("AUTODESK GROUP") BE LIABLE FOR ANY LOSSES, DAMAGES OR EXPENSES
 OF ANY KIND (INCLUDING WITHOUT LIMITATION PUNITIVE OR MULTIPLE DAMAGES OR OTHER
 SPECIAL, DIRECT, INDIRECT, EXEMPLARY, INCIDENTAL, LOSS OF PROFITS, REVENUE
 OR DATA, COST OF COVER OR CONSEQUENTIAL LOSSES OR DAMAGES OF ANY KIND),
 HOWEVER CAUSED, AND REGARDLESS OF THE THEORY OF LIABILITY, WHETHER DERIVED
 FROM CONTRACT, TORT (INCLUDING, BUT NOT LIMITED TO, NEGLIGENCE), OR OTHERWISE,
 ARISING OUT OF OR RELATING TO THE DATA OR ITS USE OR ANY OTHER PERFORMANCE,
 WHETHER OR NOT AUTODESK HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH LOSS
 OR DAMAGE. 
 
"""

def DisplayString(pHeader, pValue="" , pSuffix=""):
    lString = pHeader
    lString += str(pValue)
    lString += pSuffix
    print(lString)

def DisplayBool(pHeader, pValue, pSuffix=""):
    lString = pHeader
    if pValue:
        lString += "true"
    else:
        lString += "false"
    lString += pSuffix
    print(lString)

def DisplayInt(pHeader, pValue, pSuffix=""):
    lString = pHeader
    lString += str(pValue)
    lString += pSuffix
    print(lString)

def DisplayDouble(pHeader, pValue, pSuffix=""):
    print("%s%f%s" % (pHeader, pValue, pSuffix))

def Display2DVector(pHeader, pValue, pSuffix=""):
    print("%s%f, %f%s" % (pHeader, pValue[0], pValue[1], pSuffix))

def Display3DVector(pHeader, pValue, pSuffix=""):
    print("%s%f, %f, %f%s" % (pHeader, pValue[0], pValue[1], pValue[2], pSuffix))

def Display4DVector(pHeader, pValue, pSuffix=""):
    print("%s%f, %f, %f, %f%s" % (pHeader, pValue[0], pValue[1], pValue[2], pValue[3], pSuffix))

def DisplayColor(pHeader, pValue, pSuffix=""):
    print("%s%f (red), %f (green), %f (blue)%s" % (pHeader, pValue.mRed, pValue.mGreen, pValue.mBlue, pSuffix))

