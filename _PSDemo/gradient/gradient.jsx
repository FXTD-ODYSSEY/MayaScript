
function getSelectedLayers() {
    // NOTE https://stackoverflow.com/questions/27255364
    var idGrp = stringIDToTypeID("groupLayersEvent");
    var descGrp = new ActionDescriptor();
    var refGrp = new ActionReference();
    refGrp.putEnumerated(charIDToTypeID("Lyr "), charIDToTypeID("Ordn"), charIDToTypeID("Trgt"));
    descGrp.putReference(charIDToTypeID("null"), refGrp);
    executeAction(idGrp, descGrp, DialogModes.ALL);
    var resultLayers = new Array();
    for (var ix = 0; ix < app.activeDocument.activeLayer.layers.length; ix++) { resultLayers.push(app.activeDocument.activeLayer.layers[ix]) }
    var id8 = charIDToTypeID("slct");
    var desc5 = new ActionDescriptor();
    var id9 = charIDToTypeID("null");
    var ref2 = new ActionReference();
    var id10 = charIDToTypeID("HstS");
    var id11 = charIDToTypeID("Ordn");
    var id12 = charIDToTypeID("Prvs");
    ref2.putEnumerated(id10, id11, id12);
    desc5.putReference(id9, ref2);
    executeAction(id8, desc5, DialogModes.NO);
    return resultLayers;
}

function clear_select() {
    // NOTE clear select regin
    var idsetd = charIDToTypeID("setd");
    var desc259 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    var ref63 = new ActionReference();
    var idChnl = charIDToTypeID("Chnl");
    var idfsel = charIDToTypeID("fsel");
    ref63.putProperty(idChnl, idfsel);
    desc259.putReference(idnull, ref63);
    var idT = charIDToTypeID("T   ");
    var idOrdn = charIDToTypeID("Ordn");
    var idNone = charIDToTypeID("None");
    desc259.putEnumerated(idT, idOrdn, idNone);
    executeAction(idsetd, desc259, DialogModes.NO);
}

function placeFile(placeFile) {
    clear_select()

    // NOTE https://community.adobe.com/t5/photoshop/photoshop-scripts-for-image-layers-javascript/td-p/9903887?page=1
    var desc21 = new ActionDescriptor();

    desc21.putPath(charIDToTypeID('null'), new File(placeFile));

    desc21.putEnumerated(charIDToTypeID('FTcs'), charIDToTypeID('QCSt'), charIDToTypeID('Qcsa'));

    var desc22 = new ActionDescriptor();

    desc22.putUnitDouble(charIDToTypeID('Hrzn'), charIDToTypeID('#Rlt'), 0.000000);

    desc22.putUnitDouble(charIDToTypeID('Vrtc'), charIDToTypeID('#Rlt'), 0.000000);

    desc21.putObject(charIDToTypeID('Ofst'), charIDToTypeID('Ofst'), desc22);

    executeAction(charIDToTypeID('Plc '), desc21, DialogModes.NO);

};

function main() {

    var __file__ = File($.fileName).fsName
    var docRef = app.activeDocument;
    var layers = getSelectedLayers();

    temp_folder = Folder.temp.fsName

    artLayers_visible = []
    layerSets_visible = []
    for (var i = 0; i < docRef.artLayers.length; i++) {
        layer = docRef.artLayers[i]
        artLayers_visible.push(layer.visible)
        layer.visible = false

    }
    for (var i = 0; i < docRef.layerSets.length; i++) {
        sets = docRef.layerSets[i]
        layerSets_visible.push(sets.visible)
        sets.visible = false
    }

    for (var i = 0; i < layers.length; i++) {
        layer = layers[i]
        layer.visible = true;
        var saveOptions = new PNGSaveOptions();
        var idx = i + 1
        var output = temp_folder + "\\input_" + idx + ".png"
        activeDocument.saveAs(new File(output), saveOptions, true, Extension.LOWERCASE)
        layer.visible = false;
    }


    for (var i = 0; i < artLayers_visible.length; i++)
        docRef.artLayers[i].visible = artLayers_visible[i]
    for (var i = 0; i < layerSets_visible.length; i++)
        docRef.layerSets[i].visible = layerSets_visible[i]


    bat_path = __file__.replace(".jsx", ".bat")
    // app.system(bat_path + " & pause")
    app.system('"' + bat_path + '"')

    // NOTE place layer
    output_image = temp_folder + "\\output.png"
    placeFile(output_image)
}

main()
