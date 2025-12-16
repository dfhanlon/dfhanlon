var cbpAnimatedHeader = (function() {

	var docElem = document.documentElement,
		header = document.querySelector( '.navbar-fixed-top' ),
		didScroll = false,
		changeHeaderOn = 3;

	function init() {
		// Force shrink immediately on load
		if (header) {
			classie.add(header, 'navbar-shrink');
		}

		window.addEventListener( 'scroll', function() {
			if( !didScroll ) {
				didScroll = true;
				setTimeout( scrollPage, 250 );
			}
		}, false );
	}

	function scrollPage() {
		// Always keep navbar shrunk
		if (header) {
			classie.add(header, 'navbar-shrink');
		}
		didScroll = false;
	}

	function scrollY() {
		return window.pageYOffset || docElem.scrollTop;
	}

	init();

})();
