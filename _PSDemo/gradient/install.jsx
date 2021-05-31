//@include "ActionFileFromXML.jsx" 

function delete_action(action){
    var idDlt = charIDToTypeID("Dlt ");
    var desc231 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    var ref59 = new ActionReference();
    var idASet = charIDToTypeID("ASet");
    ref59.putName(idASet, action);
    desc231.putReference(idnull, ref59);
    try {
        executeAction(idDlt, desc231, DialogModes.NO);
    } catch (error) {
        return false
    }
    return true
}

function install() {
    __file__ = File($.fileName)
    temp_folder = Folder.temp.fsName
    // temp_folder = __file__.parent.fsName

    xml = __file__.fsName.replace(".jsx", ".xml")

    // NOTE read 
    var xml_file = new File(xml);
    xml_file.encoding = "UTF8";
    xml_file.open("r");
    content = xml_file.read()

    // NOTE replace __cwd__ to current working directory
    var res = ""
    lines = content.split("\n")
    for (i in lines) {
        line = lines[i]
        if (typeof line == "string") {
            res += line.replace("__cwd__", __file__.parent.fsName) + "\n";
        }
    }
    xml_file.close()

    // NOTE create a new xml file
    var xml = temp_folder + "/atn.xml";
    var atn_xml = new File(xml);
    atn_xml.encoding = "UTF8";
    atn_xml.open("w");
    atn_xml.write(res)
    atn_xml.close()

    var atn = temp_folder + "/atn.atn";

    // NOTE generate atn file
    opt = { source: xml, outf: atn }
    ActionFileXmlUI.prototype.process(opt)

    // NOTE delete previous install file
    delete_action("魔方 PS 动作库")
    
    // https://community.adobe.com/t5/photoshop/load-action-in-photoshop-using-javascript-refreshes-photoshop-please-guide/td-p/10107938
    app.load(new File(atn))
    alert("安装成功 - 打开动作可以找到 PS 动作库")
}

install()