// https://www.davidebarranca.com/2012/10/scriptui-window-in-photoshop-palette-vs-dialog/

var isDone, s2t, waitForRedraw, win, windowResource;

// Shortcut function
s2t = function (stringID) {
    return app.stringIDToTypeID(stringID);
};

waitForRedraw = function () {
    var d;
    d = new ActionDescriptor();
    d.putEnumerated(s2t('state'), s2t('state'), s2t('redrawComplete'));
    return executeAction(s2t('wait'), d, DialogModes.NO);
};

//sentinel variable
isDone = false;

// palette same as before
var windowResource = "palette {  \
    orientation: 'column', \
    alignChildren: ['fill', 'top'],  \
    preferredSize:[300, 130], \
    text: 'ScriptUI Window - palette',  \
    margins:15, \
    \
    sliderPanel: Panel { \
      orientation: 'row', \
      alignChildren: 'right', \
      margins:15, \
      text: ' PANEL ', \
      st: StaticText { text: 'Value:' }, \
      sl: Slider { minvalue: 1, maxvalue: 100, value: 30, size:[220,20] }, \
      te: EditText { text: '30', characters: 5, justify: 'left'} \
    }, \
    \
    bottomGroup: Group{ \
      cd: Checkbox { text:'Checkbox value', value: true }, \
      cancelButton: Button { text: 'Cancel', properties:{name:'cancel'}, size: [120,24], alignment:['right', 'center'] }, \
      applyButton: Button { text: 'Apply', properties:{name:'ok'}, size: [120,24], alignment:['right', 'center'] }, \
    }\
    }";


win = new Window('window',"good",undefined,{resizeable:true,closeButton:true});
win = new Window(windowResource);

// don't forget this one!
win.onClose = function () {
    return isDone = true;
};

win.show();


while (isDone === false) {
    // waitForRedraw()
    app.refresh(); // or, alternatively, waitForRedraw();
}