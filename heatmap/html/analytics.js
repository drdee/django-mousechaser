var server = window.location.hostname + '/analytics/';

var coordinates = new Object();
var x = 0;
var startTime = new Date();
var divs = Array();

function convert_object_to_array(object) {
       var data = new String();
       for (i=0, len=object.length; i<len; i++){
       		//obj = $.param(object[i]);
       		for (key in object[i]) {
       			data += i + key + '=' + object[i][key] + ';'
       		}
			//console.log(obj);               
            //data[i] = obj;
       }
       return data;

}

function retrieve_document_properties() {
	width = $(document).width();
	height= $(document).height();
	return [width, height];
}

function add_postform(data, coordinates, delta_time, server) {
       var ifr = document.createElement('iframe');
       var frm = document.createElement('form');
       ifr.setAttribute("id", 'ifr_analytics');
       frm.setAttribute("action", server);
       frm.setAttribute("method", "POST");
       frm.setAttribute("id","analytics");
       var elem = document.createElement('input');
       elem.setAttribute("type", "textarea");


       frm.appendChild(elem);
       ifr.appendChild(frm);
       document.body.appendChild(ifr);
       //frm.submit();
       //console.log(data);
       //console.log($.param(coordinates));
       props = retrieve_document_properties();
       //width, height = retrieve_document_properties();
       width = props[0];
       height= props[1];
       //console.log(props);
       data = convert_object_to_array(data);
       data = data + $.param(coordinates) + ';';
       data = data + 'url=' + location.href + ';';
       data = data + 'time_spend=' + delta_time +';';
       data = data + 'doc_height=' + height + ';';
       data = data + 'doc_width=' + width + ';';
       
       $('#analytics').val(data);
       //form = $('#analytics');
       data = $('#analytics').val();
       console.log(data);
       $.ajax({
               type: 'POST',
               url: server,
               data : data,
               });
}

function retrieve_parent_element(elem) {
	parent = $(elem).closest('div');
	if (parent.length == 1) {
		return parent;
	} else {
		parent = $(elem).closest('p');
		if (parent.length ==1) {
			return parent;
		} else {
		parent = $(elem).closest('body');
		return parent;
		}
	}
}

$(document).ready(function(){

       $('div').mouseenter(function() {

               var currentTime = new Date();
               var currentId = $(this).attr("id");
               parent = retrieve_parent_element($(this));
               if (!(currentId in divs)) {
                       elem = new Object();
                       elem.id = currentId;
                       elem.time_entered = currentTime.getTime();
                       elem.height= parent.height();
                       elem.width = parent.width();
                       elem.x = parent.offset().left;
                       elem.y = parent.offset().top;
                       //console.log($(this).offset().left);
                       divs[currentId] = elem;
                       console.log(elem);
                       //divs.push(elem);
                       }
       });

       $('div').mouseleave(function() {
               var currentTime = new Date();
               var currentId = $(this).attr("id");
               if (currentId in divs) {
                       elem = divs[currentId];
                       elem.time_left = currentTime.getTime();

               }

       });
       
       $('body').mousemove(function(e){
               console.log('('+ e.pageX+','+ e.pageY+')');
               coordinates['x'+x] = e.pageX;
               coordinates['y'+x] = e.pageY;
               x++;
               $('#document').html('e.pageX = ' + e.pageX + ', e.pageY = ' + e.pageY);
       });

       $("#document").click(function() {
       //Uncomment this line for debug purposes, this will send the post form without leaving the page
       //$(window).unload(function() {
			   endTime = new Date();
			   delta_time = endTime.getTime() - startTime.getTime();
               add_postform(divs,coordinates, delta_time, server);
       });
});
