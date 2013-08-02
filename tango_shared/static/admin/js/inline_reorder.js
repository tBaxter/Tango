(function($) {
  $(document).ready(function() {
    // NOTE: THIS ONLY WORKS ON TABULAR INLINES.
    $objectRows = $('div.inline-related tbody tr');
    $objectRows
      .attr('title', 'Drag and drop to re-set order')
      .css('cursor', 'move');
    $('div.inline-group').sortable({
      axis: 'y',
      opacity: 0.7,
      items: 'div.inline-related tbody tr',
      handle: 'td',
      update: function() {
        $('div.inline-related tbody tr').each(function(i) {
            $this = $(this);
            // only set order if there is an item
            if ($this.find('td.original input:first').val()) {
                $this.find('td.field-order input').val(i + 1);
            }
        });
        $('div.inline-related tbody tr:odd').removeClass('row2').addClass('row1');
        $('div.inline-related tbody tr:even').removeClass('row1').addClass('row2');
      }
    });
  });
})(django.jQuery);