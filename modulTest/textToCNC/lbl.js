const SerialPort = require('serialport')
const port = new SerialPort('/dev/ttyUSB0', { baudRate: 115200 })
var Readline = SerialPort.parsers.Readline

var serialState = new Boolean()

var parser = port.pipe(new Readline({delimiter:'\n'}))


port.on('open',function(){
	console.log('waiting for serial port connection')
});

/*feedback from grbl*/
parser.on('data', line => {
	console.log(line)
})




var LineByLineReader = require('line-by-line')
var	lr = new LineByLineReader('test.nc', {skipEmptyLines: true }),
	row = 0

lr.on('error', function (err) {
	throw err
})

lr.on('open', function() {
	// Do something, like initialise progress bar etc.
})

lr.on('line', function (line) {
	console.log(++row + ": " + line);
//	port.write(line + '\n')
})

lr.on('end', function () {
	console.log("Ok we're done - exiting now.");
})