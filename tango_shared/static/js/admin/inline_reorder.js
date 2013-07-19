jQuery(function($) {
    // NOTE: THIS ONLY WORKS ON TABULAR INLINES.
    $('div.inline-related tbody tr').attr('title', 'Drag and drop to re-set order');
    $('div.inline-group').sortable({
        axis: 'y',
        opacity: 0.7,
        items: 'div.inline-related tbody tr',
        handle: 'td',
        update: function() {
            $(this).find('div.inline-related tbody tr').each(function(i) {
                // only set order if there is an item
                if ($(this).find('td.original input').val()) {
                    $(this).find('td.field-order input').val(i+1);
                }
            });
            $(this).find('div.inline-related tbody tr:odd').removeClass('row2').addClass('row1');
            $(this).find('div.inline-related tbody tr:even').removeClass('row1').addClass('row2');
        }
    });
    $('div.inline-related tr').css('cursor', 'move');
});