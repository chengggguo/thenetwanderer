/*web socket*/
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);


/* text to svg*/
var fs = require('fs');
var svgpath = require('svgpath');
const svgcode = require("svgcode");
const TextToSVG = require('text-to-svg');

/*svg reotation*/
const textToSVG = TextToSVG.loadSync('./fonts/simplex.ttf');
const attributes = {fill: 'none', stroke: 'black'};
const options = {x: 0, y: 0, fontSize: 72, anchor: 'top', attributes: attributes};

/*arduino serail port(gbrl)*/
const SerialPort = require('serialport')
const port = new SerialPort('/dev/ttyUSB0', { baudRate: 115200 })
var Readline = SerialPort.parsers.Readline

/*line by line gcode sender*/
var LineByLineReader = require('line-by-line')
var serialState = new Boolean() //checking the grbl feedback
var parser = port.pipe(new Readline({delimiter:'\n'}))



/*communication with the arduino(grbl)*/
port.on('open',function(){
  console.log('waiting for serial port connection')
});

/*feedback from arduino(grbl)*/
parser.on('data', line => {
  console.log(line)
})


/*communication with the client (error page of the browser)*/

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});
 
io.on('connection', function(socket){
  console.log('a user connected');
  /*combine the scroe and name from game*/
  var score;
  var ipAdd = "192.222.919"; //need to be replaced
  socket.on('score', function(data){
    score = data.toString();
  });
  socket.on('user', function(data){
    console.log("CNC printing: ");
    console.log("NAME: ", data);
    var totalData =  ipAdd + " " + data + " " +score;
    console.log(totalData);



  /*get the data from error page*/
  socket.on('cnc', function(data){
  	console.log("CNC printing: ");
  	console.log(data);
  	// console.log(data.ip);
  	// console.log(data.name);
  	// console.log(data.score);
  	socket.emit('status', "P");//P for printing, F for finished

    /*transform text to svg image*/
  	const svgData = textToSVG.getD(totalData, options);

    /*rotate the svg image and save*/
  	var transformed = svgpath(svgData).rotate(90, 0, 0).scale(-0.06, 0.06).translate(0,0).toString();
  	var path = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\"><path fill= \"none\" stroke=\"black\" stroke-width=\"0\" d=\"" + transformed + "\"/></svg>";
	//console.log(path);
	fs.writeFile("./test.svg", path, function(){
  		console.log("SVG Saved");
  		const gcode = svgcode()
			.loadFile(__dirname + "/test.svg")
			.generateGcode();

    /*conver the svg to gcode file and save*/
		var gcodeData = gcode.gCode;
		var gcodeString = "G1 F3000\nG1 X0 Y0\nM3 S1000\n";
		var zVal = -1;
		for(var i=0; i<gcodeData.length; i++){
			/*UNCOMMENT TO CHANGE THE VALUE OF Z*/
			var g = gcodeData[i].includes("G1");
			var n = gcodeData[i].includes("Z");
			var substring = "";
			var splitSubs;
			if(g && n){
				splitSubs = gcodeData[i].split("Z");
				//console.log(splitSubs[1]);
				gcodeString += splitSubs[0] + "Z" + zVal + "\n";
			}else{
				gcodeString += gcodeData[i]+"\n";
			}
			//gcodeString += gcodeData[i]+"\n"; //COMMENT WHEN CHANGING VALUE OF Z
		}

		//console.log(gcodeString);
		fs.writeFile("./test.nc", gcodeString, function(){
  			console.log("GCODE Saved");
  		});
  	});
    port.write('GO X0 Y0\n')
    setTimeout(GcodeSender,2000)// sending commands to CNC after got the gcode file

  	//Test for a timeout to send data to the browser after 10 secs
  	// setTimeout(function(){
  	// 	socket.emit('status', "F");
  	// },10000);
  
  });

  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
});


/*checking the state of grbl, if true (get 'ok')then send another land of gcode*/
function SerialState(){
  parser.on('data', line => {
    if(line.includes('ok')){
      serialState = true
    }else{
      serialState = false
    }   
  })

  return serialState
}

/*grbl configuration*/
function config(){
  port.write('$G\n[G0 G54 G17 G21 G90 G94 M0 M5 M9 T0 F0.SO.]\n$$\n$0=10 (step pulse, usec)\n$1=25 (step idle delay, msec)\n$2=0 (step port invert mask:00000000)\n$3=0 (dir port invert mask:00000110)\n$4=0 (step enable invert, bool)\n$5=0 (limit pins invert, bool)\n$6=0 (probe pin invert, bool)\n$10=3 (status report mask:00000011)\n$11=0.020 (junction deviation, mm)\n$12=0.002 (arc tolerance, mm)\n$13=0 (report inches, bool)\n$20=0 (soft limits, bool)\n$21=0 (hard limits, bool)\n$22=0 (homing cycle, bool)\n$23=1 (homing dir invert mask:00000001)\n$24=50.000 (homing feed, mm/min)\n$25=635.000 (homing seek, mm/min)\n$26=250 (homing debounce, msec)\n$27=1.000 (homing pull-off, mm)\n$100=314.961 (x, step/mm)\n$101=314.961 (y, step/mm)\n$102=314.961 (z, step/mm)\n$110=635.000 (x max rate, mm/min)\n$111=635.000 (y max rate, mm/min)\n$112=635.000 (z max rate, mm/min)\n$120=50.000 (x accel, mm/sec^2)\n$121=50.000 (y accel, mm/sec^2)\n$122=50.000 (z accel, mm/sec^2)\n$130=225.000 (x max travel, mm)\n$131=125.000 (y max travel, mm)\n$132=170.000 (z max travel, mm)\n', function(err) {
    if (err) {
      return console.log('Error on write: ', err.message)
    }
    console.log('grbl configuration done')
  })
}


/*gcode sender*/
function GcodeSender(){
  console.log('in GcodeSender now')
  var lr = new LineByLineReader('test.nc', {skipEmptyLines: true}),
    row = 0
  lr.on('error', function(err){
    throw err
  })

  lr.on('open', function(){
    console.log('gcode file is opened')
  })

  lr.on('line',function(line){
    console.log(line)
    port.write(line + '\n')
    lr.pause()

    SerialState()
    if (serialState){
      setTimeout(function(){
        lr.resume()
      },150)
    }
  });

  lr.on('end',function(){
    console.log('gcode file all line sent')
    socket.emit('status',"F")
    console.log('sever sent F')
  })
}


setTimeout(config,2000)

/*the server keep listening*/
http.listen(3000, function(){
  console.log('listening on *:3000');
});