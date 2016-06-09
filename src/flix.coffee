# /*
#  * This example program connects to already paired buttons and register event listeners on button events.
#  * Run the scanwizard.js program to add buttons.
#  */


fliclib = require("./fliclibNodeJs");
FlicClient = fliclib.FlicClient;
FlicConnectionChannel = fliclib.FlicConnectionChannel;
FlicScanner = fliclib.FlicScanner;

client = new FlicClient("localhost", 5551);

listenToButton(bdAddr) ->
	cc = new FlicConnectionChannel(bdAddr);
	client.addConnectionChannel(cc);
	cc.on "buttonUpOrDown", (clickType, wasQueued, timeDiff) ->
		console.log(bdAddr + " " + clickType + " " + (wasQueued ? "wasQueued" : "notQueued") + " " + timeDiff + " seconds ago");
	cc.on "connectionStatusChanged", (connectionStatus, disconnectReason) ->
		console.log(bdAddr + " " + connectionStatus + (connectionStatus == "Disconnected" ? " " + disconnectReason : ""));

client.once "ready", () ->
	console.log("Connected to daemon!");
	client.getInfo  (info) ->
		info.bdAddrOfVerifiedButtons.forEach (bdAddr) ->
			listenToButton(bdAddr);

client.on "bluetoothControllerStateChange", (state) ->
	console.log("Bluetooth controller state change: " + state);

client.on "newVerifiedButton", (bdAddr) ->
	console.log("A new button was added: " + bdAddr);
	listenToButton(bdAddr);

client.on "error", (error) ->
	console.log("Daemon connection error: " + error);

client.on "close", (hadError) ->
	console.log("Connection to daemon is now closed");
