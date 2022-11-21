/*--------------------------------------------------------------
# select2 customization
--------------------------------------------------------------*/

$(".select2-trips").select2({
  width: 'resolve'
  }
)

$('select').select2({
  minimumResultsForSearch: 4 
});

$(".select").each(function() {
$(this).siblings(".select2-trips").css('border', '5px solid red');
});

