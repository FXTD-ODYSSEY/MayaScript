var docRef = app.activeDocument;
var dlg = new Window('dialog', 'My first script!',[100,100,480,250]);
dlg.btnPnl = dlg.add('panel', [25,15,365,125], 'Hello world!');
dlg.btnPnl.testBtn = dlg.btnPnl.add('button', [15,30,305,50], 'Finished', {name:'ok'});
dlg.btnPnl.testBtn.onClick = dobuild;
dlg.show();
function dobuild() {
    alert("Congratulations - it all worked!");
    dlg.close();
}