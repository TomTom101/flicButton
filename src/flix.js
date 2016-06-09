var FlicClient, FlicConnectionChannel, FlicScanner, client, fliclib, listenToButton;

fliclib = require("./fliclibNodeJs");

FlicClient = fliclib.FlicClient;

FlicConnectionChannel = fliclib.FlicConnectionChannel;

FlicScanner = fliclib.FlicScanner;

client = new FlicClient("localhost", 5551);

listenToButton = function(bdAddr) {
  var cc;
  cc = new FlicConnectionChannel(bdAddr);
  client.addConnectionChannel(cc);
  cc.on("buttonUpOrDown", function(clickType, wasQueued, timeDiff) {
    return console.log(bdAddr + " " + clickType + " " + (wasQueued != null ? wasQueued : {
      "wasQueued": "notQueued"
    }) + " " + timeDiff + " seconds ago");
  });
  return cc.on("connectionStatusChanged", function(connectionStatus, disconnectReason) {
    var ref;
    return console.log(bdAddr + " " + connectionStatus + ((ref = connectionStatus === "Disconnected") != null ? ref : " " + {
      disconnectReason: ""
    }));
  });
};

client.once("ready", function() {
  console.log("Connected to daemon!");
  return client.getInfo(function(info) {
    return info.bdAddrOfVerifiedButtons.forEach(function(bdAddr) {
      return listenToButton(bdAddr);
    });
  });
});

client.on("bluetoothControllerStateChange", function(state) {
  return console.log("Bluetooth controller state change: " + state);
});

client.on("newVerifiedButton", function(bdAddr) {
  console.log("A new button was added: " + bdAddr);
  return listenToButton(bdAddr);
});

client.on("error", function(error) {
  return console.log("Daemon connection error: " + error);
});

client.on("close", function(hadError) {
  return console.log("Connection to daemon is now closed");
});
