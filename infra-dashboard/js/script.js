jQuery(document).ready(function () {
	// If svg is not supported
	if (!Modernizr.svg) {
	  jQuery('img[src$=".svg"]').each(function() {
	      jQuery(this).attr('src', jQuery(this).attr('src').replace('.svg', '.png'));
	  });
	}
	// If media queries are not supported
	if(!Modernizr.mq('only all')) {
		jQuery('head').append('<link id="no-mq" rel="stylesheet" type="text/css">');
		jQuery("link#no-mq").attr("href", "/joomla/media/templates/highsoft_bootstrap/css/ie.css");
	}
	// Sidebar click animation
	jQuery('.nav-sidebar > li').click(function () {
		if (!jQuery(this).hasClass("active")) {
			jQuery('.nav-sidebar > li.active > div.active').removeClass('active');
			jQuery('.nav-sidebar > li.active > ul').slideUp("slow");
			jQuery('.nav-sidebar > li.active').removeClass('active');
			jQuery(this).addClass("active");
			jQuery('.nav-sidebar > li.active > ul').slideDown("slow");
			jQuery('.nav-sidebar > li.active > div').addClass('active');
		}
	});
	jQuery("#sidebar-toggle").click(function (e) {
		jQuery("#wrap").toggleClass("toggled");
	});	
});	