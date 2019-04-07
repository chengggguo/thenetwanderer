/*web socket*/
var express = require('express')
var app = express()
var http = require('http').Server(app)
var io = require('socket.io')(http)
let async = require('async')


/* text to svg*/
var fs = require('fs')
var svgpath = require('svgpath')
const svgcode = require("svgcode")
const TextToSVG = require('text-to-svg')

/*svg reotation*/
const textToSVG = TextToSVG.loadSync('./fonts/simplex.ttf')
const attributes = {fill: 'none', stroke: 'black'}
const options = {x: 0, y: 0, fontSize: 72, anchor: 'top', attributes: attributes};

/*moving the default position*/
var counter = 0

/*arduino serail port(gbrl)*/
const SerialPort = require('serialport')
const port = new SerialPort('/dev/ttyUSB0', { baudRate: 115200 })
var Readline = SerialPort.parsers.Readline

/*line by line gcode sender*/
var LineByLineReader = require('line-by-line')
var serialState = new Boolean() //checking the grbl feedback
var parser = port.pipe(new Readline({delimiter:'\n'}))

// import parallel from './internal/parallel'
// import eachOfSeries from './eachOfSeries'

/*communication with the arduino(grbl)*/
port.on('open',function(){
  console.log('waiting for serial port connection')
});

/*feedback from arduino(grbl)*/
parser.on('data', line => {
  console.log(line)
})


/*communication with the client (error page of the browser)*/
app.use(express.static('./'))
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html')
})
 
io.on('connection', function(socket){
  console.log('a user connected')
  /*combine the scroe and name from game*/
  var score;
  var ipAdd = "1"; //need to be replaced
  socket.on('score', function(data){
    score = data.toString()
  });
  socket.on('user', function(data){
    console.log("CNC will print: ")
    console.log("NAME: ", data)
    var totalData =  ipAdd + " " + data + " " +score;
    console.log(totalData);



  /*get the data from error page*/
  // socket.on('cnc', function(data){
  // 	console.log("CNC printing: ");
  // 	console.log(data);
  	// console.log(data.ip);
  	// console.log(data.name);
  	// console.log(data.score);
  	socket.emit('status', "P");//P for printing, F for finished

    /*transform text to svg image*/
  	const svgData = textToSVG.getD(totalData, options);

    /*rotate the svg image and save*/
  	var transformed = svgpath(svgData).rotate(270, 0, 0).scale(-0.06, 0.06).translate(0,0).toString();
  	var path = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\"><path fill= \"none\" stroke=\"black\" stroke-width=\"0\" d=\"" + transformed + "\"/></svg>";
	//console.log(path);
	fs.writeFile("./test.svg", path, function(){
  	console.log("SVG Saved");
  	const gcode = svgcode()
		.loadFile(__dirname + "/test.svg")
		.generateGcode();

    /*conver the svg to gcode file and save*/
		var gcodeData = gcode.gCode;
    var newStart = counter*10
    console.log('newStart' + newStart)
		var gcodeString = "G1 F300\nG21\nM3 S1000\n";
		var zVal = -1;
    var gcodeEnding = "M3 0\nG0 X" + newStart +" " +"Y0 Z0\n"
		for(var i=0; i<gcodeData.length; i++){
			/*UNCOMMENT TO CHANGE THE VALUE OF Z*/
			var g = gcodeData[i].includes("G1");
			var n = gcodeData[i].includes("Z");
      var gStart = gcodeData[i].includes("G9")
			var substring = "";
			var splitSubs;
      if(g && n){
        splitSubs = gcodeData[i].split("Z");
        //console.log(splitSubs[1]);
        gcodeString += splitSubs[0] + "Z" + zVal + "\n";
      }else if(gStart){
        splitSubs = gcodeData[i].split("9")
        gcodeString+= splitSubs[0]+ "92 X0 Y0 Z0" + "\n"

      }else{
        gcodeString += gcodeData[i]+"\n";
      }
			//gcodeString += gcodeData[i]+"\n"; //COMMENT WHEN CHANGING VALUE OF Z
		}
    gcodeString = gcodeString + gcodeEnding;



		//console.log(gcodeString);
		fs.writeFile("./test.nc", gcodeString, function(){
  			console.log("GCODE Saved");
  		});
  	});
    //port.write('GO X0 Y0\n')
    // port.write('G0 F3000\NG0 X-320 Y0\N')///
    // console.log('set starting position')
    // sleep.sleep(5)
    // console.log('starting send code')///
    // GcodeSender()
    setTimeout(GcodeSender,2000)
    // console.log('code sent')///
    // port.write('$H\n')///
    // sleep.sleep(10)///

    // socket.emit('status','F')
    counter += 1
    setTimeout(function(){ 
      socket.emit('status','F')

    },20000)

    // async.auto({
    //   sendGcode: function(){
    //     GcodeSender()
    //     console.log('gcode sent done')
    //   },
    //   sendF: ['sendGcode',function(){
    //     socket.emit('status','F')
    //     console.log('F sent')
    //   }]

    // })


  });


  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
});


setTimeout(ConfigSender,2000)

/*the server keep listening*/
http.listen(3000, function(){
  console.log('listening on *:3000');
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
      },300)
    }
  });

  lr.on('end',function(){
    port.write("$H\n\r")
    console.log('gcode file all line sent')
  })
  return ('finish')
}

/*grbl configuration*/
function ConfigSender(){
  console.log('configing the GRBL now')
  var lr = new LineByLineReader('GrblConfig.txt', {skipEmptyLines: true}),
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
      },50)
    }
  });

  lr.on('end',function(){
    console.log('config done')
  })
  return ('finish')
}

