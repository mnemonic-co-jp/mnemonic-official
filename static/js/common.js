$(function() {

	function resizeWindow() {
		var topnavHeight = $('#subnav').height();
		var viewportHeight = 'innerHeight' in window ? window.innerHeight : document.documentElement.offsetHeight;
		var containerHeight = String(viewportHeight - topnavHeight - 100) + 'px';
		$('#container').css({
			minHeight: containerHeight,
			height: containerHeight
		});
	}
	resizeWindow();

	$(window).resize(resizeWindow);

});