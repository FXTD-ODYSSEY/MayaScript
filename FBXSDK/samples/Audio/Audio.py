"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.
 
"""
SAMPLE_FILENAME = "Audio.fbx"
import sys

def CreateScene(pSdkManager, pScene, pSampleFileName):

    # Create the Animation Stack
    lAnimStack = FbxAnimStack.Create(pScene, "AudioSample")

    # At least one animation layer is mandatory even if we don't have nodes animation.
    lAnimLayer = FbxAnimLayer.Create(pScene, "Base Layer")
    lAnimStack.AddMember(lAnimLayer)

    # Create 2 audio tracks (each track can contain [0..n] audio clips
    lAudioLayer1 = FbxAudioLayer.Create(pScene, "Audio Track 1")
    lAudioLayer1.Color.Set(FbxDouble3(1,0,0))

    lAudioLayer2 = FbxAudioLayer.Create(pScene, "Audio Track 2")
    lAudioLayer2.Color.Set(FbxDouble3(0,0,1))
    lAudioLayer2.Mute.Set(True) # let's mute the second audio track

    # add the audio tracks to the AnimStack
    lAnimStack.AddMember(lAudioLayer1)
    lAnimStack.AddMember(lAudioLayer2)

    # At this moment we should have 3 layers in the AnimStack.
    # The first one is "Base Layer" and the next ones are "Audio Track 1" and "Audio Track 2"
    if lAnimStack.GetMemberCount() != 3:
        return False

    if lAnimStack.GetMember(0) != lAnimLayer:
        return False

    if lAnimStack.GetMember(1) != lAudioLayer1:
        return False

    if lAnimStack.GetMember(2) != lAudioLayer2:
        return False

    # Create audio clip and put it in the audio tracks
    clip0 = FbxAudio.Create(pScene, "Clip0")

    # Fill clip0 with dummy values. 
    # Note that the FBX SDK does not evaluate audio data.
    time = FbxTime()
    time.SetSecondDouble(30.0)

    clip0.BitRate.Set(8)
    clip0.SampleRate.Set(96000)
    clip0.Channels.Set(2)
    clip0.Duration.Set(time)
    clip0.Volume().Set(0.5)
    clip0.SetFileName("/a/dummy/file/name.wav")
    clip0.SetClipIn(FbxTime())
    time.SetSecondDouble(3.33)
    clip0.SetClipOut(time)

    # The same audio clip can be used on different audio tracks
    lAudioLayer1.AddMember(clip0)
    lAudioLayer2.AddMember(clip0)

    # Create another audio clip that we will only attach to the track 1
    clip1 = FbxAudio.Create(pScene, "Clip1")
    clip1.SetFileName("/a/dummy/file/name.wav") # clips can reference the same audio file
    time.SetSecondDouble(40.0)
    clip1.SetClipIn(time)
    clip1.SetClipOut(time + clip0.Duration.Get())
    lAudioLayer1.AddMember(clip1)

    # clone clip0 and attach it to track 1 as well
    clip2 = clip0.Clone(FbxObject.eDeepClone, pScene)
    clip2.SetName("clone of clip0")
    clip2.SetFileName("/defining/a/second/audio/file.mp3")
    time.SetSecondDouble(120.0)
    clip2.SetClipIn(time)
    time.SetSecondDouble(time.GetSecondDouble() + 8.0)
    clip2.SetClipOut(time)
    lAudioLayer1.AddMember(clip2)
    return True

if __name__ == "__main__":
    try:
        import FbxCommon
        from fbx import *
    except ImportError:
        print("Error: module FbxCommon and/or fbx failed to import.\n")
        print("Copy the files located in the compatible sub-folder lib/python<version> into your python interpreter site-packages folder.")
        import platform
        if platform.system() == 'Windows' or platform.system() == 'Microsoft':
            print('For example: copy ..\\..\\lib\\Python27_x64\\* C:\\Python27\\Lib\\site-packages')
        elif platform.system() == 'Linux':
            print('For example: cp ../../lib/Python27_x64/* /usr/local/lib/python2.7/site-packages')
        elif platform.system() == 'Darwin':
            print('For example: cp ../../lib/Python27_x64/* /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
        sys.exit(1)
    
    # Prepare the FBX SDK.
    (lSdkManager, lScene) = FbxCommon.InitializeSdkObjects()
    
    # The example can take an output file name as an argument.
    lSampleFileName = ""
    if len(sys.argv) > 1:
        lSampleFileName = sys.argv[1]
    # A default output file name is given otherwise.
    else:
        lSampleFileName = SAMPLE_FILENAME

    # Create the scene.
    lResult = CreateScene(lSdkManager, lScene, lSampleFileName)

    if lResult == False:
        print("\n\nAn error occurred while creating the scene...\n")
        lSdkManager.Destroy()
        sys.exit(1)

    # Save the scene.
    lResult = FbxCommon.SaveScene(lSdkManager, lScene, lSampleFileName)

    if lResult == False:
        print("\n\nAn error occurred while saving the scene...\n")
        lSdkManager.Destroy()
        sys.exit(1)

    # Destroy all objects created by the FBX SDK.
    lSdkManager.Destroy()
   
    sys.exit(0)
