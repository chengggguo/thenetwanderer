const SerialPort = require('serialport');
const Readline = require('@serialport/parser-readline');
const port = new SerialPort('/dev/ttyUSB0', { baudRate: 115200 });

const parser = new Readline();
port.pipe(parser);

port.on('open',function(){
	console.log('waiting for serial port connection');
//	port.write('G1 F1000\NG1 X0 Y0\NG21\NG90\Nm3 s1000\n');
});



//parser.on('data', line => console.log(`> ${line}`));
parser.on('data', line => {

	console.log(`> ${line}`);
	if({line} == 'ok'){
		stopS();
	}


});

function config(){
	port.write('$G\n[G0 G54 G17 G21 G90 G94 M0 M5 M9 T0 F0.SO.]\n$$\n$0=10 (step pulse, usec)\n$1=25 (step idle delay, msec)\n$2=0 (step port invert mask:00000000)\n$3=6 (dir port invert mask:00000110)\n$4=0 (step enable invert, bool)\n$5=0 (limit pins invert, bool)\n$6=0 (probe pin invert, bool)\n$10=3 (status report mask:00000011)\n$11=0.020 (junction deviation, mm)\n$12=0.002 (arc tolerance, mm)\n$13=0 (report inches, bool)\n$20=0 (soft limits, bool)\n$21=0 (hard limits, bool)\n$22=0 (homing cycle, bool)\n$23=1 (homing dir invert mask:00000001)\n$24=50.000 (homing feed, mm/min)\n$25=635.000 (homing seek, mm/min)\n$26=250 (homing debounce, msec)\n$27=1.000 (homing pull-off, mm)\n$100=314.961 (x, step/mm)\n$101=314.961 (y, step/mm)\n$102=314.961 (z, step/mm)\n$110=635.000 (x max rate, mm/min)\n$111=635.000 (y max rate, mm/min)\n$112=635.000 (z max rate, mm/min)\n$120=50.000 (x accel, mm/sec^2)\n$121=50.000 (y accel, mm/sec^2)\n$122=50.000 (z accel, mm/sec^2)\n$130=225.000 (x max travel, mm)\n$131=125.000 (y max travel, mm)\n$132=170.000 (z max travel, mm)\n', function(err) {
	  if (err) {
	    return console.log('Error on write: ', err.message);
	  }
	  console.log('message written');
	});
};

function sendCode(){
	console.log('spindle on')
	port.write('m3 s1000\n')
};

function sendCode2(){
	console.log('spindle end')
	port.write('m3 0\n')
};

function stopS(){
	setTimeout(sendCode2,3000);
	

};


function sendCode3(){
//	console.log('spindle on');
	sendCode();
	port.on('data',stopS);
	// port.on('ok',function(){
	// 	setTimeout(sendCode2,3000)
	// });
};;

// port.on('state',function(){
// 	console.log('reading serialport');
// 	port.on('data',function(data){
// 		if (data == 'ok'){
// 			console.log('sending spindle end command')
// 			setTimeout(sendCode2,3000);			
// 		};

// 	});
// });

setTimeout(config,2000);
//setInterval(stateCheck,5);
setTimeout(sendCode3,3000);
//setTimeout(sendCode2,10000);