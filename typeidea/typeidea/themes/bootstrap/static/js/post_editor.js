$(document).ready(function($){
	var $content_md = $('.form-row.field-content_ck');
	var $content_ck = $('.form-row.field-content_md');
	var $is_md = $('input[name = is_md]');

	var switch_editor = function(is_md){
		if(is_md){
			$content_md.attr('style', 'display:none');
			$content_ck.attr('style', 'display:block');
		} else {
			$content_md.attr('style', 'display:block');
			$content_ck.attr('style', 'display:none');
		}
	}

	$is_md.on('click', function(){
		switch_editor($(this).is(':checked'));
	});

	switch_editor($is_md.is(':checked'));
});
