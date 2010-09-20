var re = new RegExp('\/[\d]*\/');
$(document).ready(function(){
	id = location.href.search(re);
	domain = window.location.hostname;
	//console.log(id);
	
	$.ajax({
		url: domain + '/analytics/page/' + id + '/',
		dataType: 'json',
		success: function(data) {
			$('body').css('background-image', 'url(domain + '/analytics/html/images/' + data[0].fields.file + '-full.png)');
			$('body').css('background-repeat', 'no-repeat');
			}
	});
	
	$.ajax({
		url: domain + '/analytics/elements/' + id + '/',
		dataType: 'json',
		success: function(data) {
			$.each(data, function(pk, elem){
				console.log(pk, elem);
				$('<div id="' + pk + '"></div>').appendTo('body');
				$('#' + pk).css('position', 'absolute');
				$('#' + pk).css('height', elem.fields.height);
				$('#' + pk).css('width', elem.fields.width);
				$('#' + pk).css('top', elem.fields.y);
				$('#' + pk).css('left', elem.fields.x);
				$('#' + pk).css('border-style', 'solid');
				$('<p>'+ elem.fields.time + '</p>').appendTo('#' + pk);
				//console.log(elem.fields.height);
				});
			}
		});
});