// JavaScript Document

if (app.documents.length == 0) {

alert ("You must have an open document to run this script.");

}

else {

var docRef = app.activeDocument

var saveOptions = new TargaSaveOptions();
saveOptions.alphaChannels = true;
saveOptions.resplution = TargaBitsPerPixels.TWENTYFOUR;

var saveName = docRef.fullName.toString();
saveName = saveName.replace('.psd','.tga')
activeDocument.saveAs(new File(saveName), saveOptions,true,Extension.LOWERCASE)

// alert("保存成功")

}