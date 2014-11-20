
var protocol_type
var port_number
var status = false



function startSerial() {
	port_number = $('select#port_no option:selected').val();
	$.get("/get_serial/"+port_number+"/");
	timeLoop1();
} 

function update1() {
 $.get("/post_serial/",function(data) {
	 $("#serial_print").html('<a>' + data + '</a>');
   });
}

function timeLoop1(){
	a = setTimeout(function() {
		timeLoop1($('select#frequency option:selected').val())
	}, 500*$('select#frequency option:selected').val());
	port_number = $('select#port_no option:selected').val();
	update1();
}



function startRecv() {
	$.get("/get_data/"+protocol_type+"/");
	timeLoop2();
}

function update2() {
 $.getJSON("/post_data/",function(data) {
	$.each(data, function(){
		 $("#recv_data").html('<h3>' + data.data + '</h3>');
		 $("#source_addr").html('<h3>' + data.ip + ' port:' + data.port + '</h3>');
		 $("#dest_addr").html('<h3>' + 'bbbb::0212:4b00:0205:f000 port:5678' + '</h3>');
		 $("#via_router").html('<h3>' + 'tun0 router: aaaa::0212:4b00:0205:f358' +'</br>'
				+'tun1 router: aaaa::0212:4b00:0205:f4ec' + '</h3>');
		 });
   });
}

function timeLoop2(){
	b = setTimeout(function() {
		timeLoop2($('select#frequency option:selected').val())
	}, 1000*$('select#frequency option:selected').val());
	update2();
}



function startPing() {
	ping_dest = $('select#ping_dest option:selected').val();
	$.get("/get_ping/"+ping_dest+"/");
	timeLoop3();
} 

function update3() {
 $.get("/post_ping/",function(data) {
	 $("#icmpv6").html('<a>' + data + '</a>');
   });
}

function timeLoop3(){
	c = setTimeout(function() {
		timeLoop3($('select#frequency option:selected').val())
	}, 1000*$('select#frequency option:selected').val());
	update3();
}








function setType(type){
	protocol_type = type;
}

function clear(){
	$("#serial_print").html('<a>' + 'Serial print' + '</a>');
}
