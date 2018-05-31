// For debugging
slate.bind("r:alt,ctrl,shift", function(win) {
    win.doOperation(slate.operation("relaunch"));
});

var maximize = slate.operation("move", {
  "x" : "screenOriginX",
  "y" : "screenOriginY",
  "width" : "screenSizeX",
  "height" : "screenSizeY"
});

// Common operations
function setupCommon() {
  var grow = slate.operation("move", {
    "x": "max({0, windowTopLeftX - windowSizeX * 0.5 * 0.2})",
    "y": "max({0, windowTopLeftY - windowSizeY * 0.5 * 0.1})",
    "width": "min({screenSizeX, windowSizeX * (1 + 0.2)})",
    "height": "min({screenSizeY, windowSizeY * (1 + 0.1)})"
  });
  var shrink = slate.operation("move", {
    "x": "windowTopLeftX + windowSizeX * 0.5 * 0.2",
    "y": "windowTopLeftY + windowSizeY * 0.5 * 0.1",
    "width": "windowSizeX * (1 - 0.2)",
    "height": "windowSizeY * (1 - 0.1)"
  });
  var pushRight = slate.operation("push", {
    "direction" : "right",
    "style" : "bar-resize:screenSizeX/2"
  });
  var pushLeft = slate.operation("push", {
    "direction" : "left",
    "style" : "bar-resize:screenSizeX/2"
  });
  var allOps = slate.operation("chain", {
    "operations": [maximize, pushRight, pushLeft]
  })
  var moveCenter = slate.operation("move", {
    "x": "screenOriginX + screenSizeX * 0.1",
    "y": "screenOriginY + screenSizeY * 0.05",
    "width": "screenSizeX * 0.8",
    "height": "screenSizeY * 0.9"
  });

  // Bindings
  slate.bind("right:alt,ctrl", function(win) {
    win && win.doOperation(pushRight);
  });
  slate.bind("left:alt,ctrl", function(win) {
    win && win.doOperation(pushLeft);
  });
  slate.bind("up:alt", function(win) {
    win && win.doOperation(allOps);
  });
  slate.bind("=:alt,ctrl", function(win) {
    win && win.doOperation(grow);
  });
  slate.bind("-:alt,ctrl", function(win) {
    win && win.doOperation(shrink);
  });
  slate.bind("o:alt,ctrl", function(win) {
    if (win) {
      var appName = win.app().name();
      win.doOperation("hide", {
        "app": "all-but:'" + appName + "'"
      });
      win.doOperation(moveCenter);
    }
  });
}

function createLayout(name, pushRight, pushLeft, moveTopLeft, moveMiddle, moveMini) {
  // Layout params
  var getBrowserParams = function(regex) {
    return {
      "operations": [function(win) {
        var title = win.title();
        if (title && title.match(regex)) {
          win.doOperation(moveMiddle);
        } else {
          win.doOperation(moveTopLeft);
        }
      }],
      "ignore-fail": true,
      "repeat": true
    }
  };

  var getParams = function(op) {
    return {
      "operations": [op],
      "ignore-fail": true,
      "repeat": true
    };
  };

  return slate.layout(name, {
    "Google Chrome": getBrowserParams(/^Developer\sTools\s-\s.+$/),
    "Firefox": getBrowserParams(/^Firebug\s-\s.+$/),
    "Safari": getBrowserParams(/^Web\sInspector\s-\s.+$/),
    "iTerm2": getParams(pushLeft),
    "Sublime Text": getParams(pushRight),
    "Code": getParams(maximize),
    "MacVim": getParams(pushRight),
    "Quip": getParams(moveMini)
  });
}

function setupBig() {
  // Operations
  var pushRight = slate.operation("push", {
    "direction" : "right",
    "style" : "bar-resize:screenSizeX*2/3"
  });
  var pushLeft = slate.operation("push", {
    "direction" : "left",
    "style" : "bar-resize:screenSizeX/3"
  });
  var moveTopLeft = slate.operation("corner", {
    "direction" : "top-left",
    "width" : "screenSizeX/3",
    "height" : "screenSizeY*0.8"
  });
  var moveMiddle = slate.operation("move", {
    "x": "screenOriginX + screenSizeX/3",
    "y": "screenOriginY",
    "width" : "screenSizeX/3",
    "height" : "screenSizeY*0.8"
  });
  var moveMini = slate.operation("move", {
    "x": "screenOriginX + screenSizeX/3",
    "y": "screenOriginX + screenSizeY/2",
    "width" : "screenSizeX/2",
    "height" : "screenSizeY/2"
  });

  var layoutBig = createLayout("big", pushRight, pushLeft, moveTopLeft, moveMiddle, moveMini);

  slate.bind("1:cmd,ctrl", function(win) {
    win.doOperation(slate.operation("layout", {"name": layoutBig}));
  });
}

function setupSmall() {
  // Operations
  var pushRight = slate.operation("push", {
    "direction" : "right",
    "style" : "bar-resize:screenSizeX/2"
  });
  var pushLeft = slate.operation("push", {
    "direction" : "left",
    "style" : "bar-resize:screenSizeX/2"
  });
  var moveTopLeft = slate.operation("corner", {
    "direction" : "top-left",
    "width" : "screenSizeX/2",
    "height" : "screenSizeY*0.8"
  });
  var moveMini = slate.operation("move", {
    "x": "screenOriginX + screenSizeX/4",
    "y": "screenOriginX + screenSizeY/2",
    "width" : "screenSizeX/2",
    "height" : "screenSizeY/2"
  });
  var layoutSmall = createLayout("small", pushRight, pushLeft, moveTopLeft, pushRight, moveMini);

  slate.bind("2:cmd,ctrl", function(win) {
    win.doOperation(slate.operation("layout", {"name": layoutSmall}));
  });
  slate.bind("1:alt", function(win) {
    win.doOperation(pushLeft);
  });
  slate.bind("2:alt", function(win) {
    win.doOperation(pushRight);
  });
}

slate.log("Setting up...");
setupBig();
setupSmall();
setupCommon();
slate.log("Done");
