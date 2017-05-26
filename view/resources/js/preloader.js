
(function ($) {
 
    $.fn.preloader = function(msg) {
		
        this.append('<div id="preloader"><p><i class="fa fa-refresh fa-spin fa-3x fa-fw"></i></p> <p style="margin-top: 20px">' + msg + '</p></div>');	
		
		 	
		$( window ).resize(function() {
			$("#preloader").css('width', $(window).width());
			$("#preloader").css('height', $(window).height());			
		});		
					
        return this;
    };
 
     $.fn.removerPreloader = function() {
        this.find('#preloader').remove();
        return this;
	};
	
}(jQuery));
