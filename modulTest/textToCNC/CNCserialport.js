const SerialPort = require('serialport')
var Readline = SerialPort.parsers.Readline

var port = new SerialPort('/dev/ttyUSB0',{baudrate:115200})

var parser = new Readline()
port.pipe(parser)

parser.on('data',function(data)){
	if(data == 'ok'){
		console.log(data)
	}
}

port.on('open',function(){
	console.log('waiting for arduino')
})