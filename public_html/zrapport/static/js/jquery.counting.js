(function($) {
	$.fn.counting = function(form, url) {
		return this.each(function() {
			$this = $(this);
			
			$this.change(function() {
				$.get(url + $this.find("option:selected").attr("value"), {}, function(result) {
					$(form).find(".counting").replaceWith(result);
				});
			});
		});
	};
})(jQuery);
