$(document).ready(function() {
	// TODO - what about after christmas?
	$('#clock').countdown('2014/12/25', function(event) {
		$(this).html(event.strftime('%D days %H:%M:%S until Christmas'));
	})
	.on('finish.countdown', function(event) {
		$(this).html("IT'S CHRISTMASSS!!!");
	});
});
