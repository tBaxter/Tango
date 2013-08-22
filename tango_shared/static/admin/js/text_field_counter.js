
django.jQuery(document).ready(function() {
    django.jQuery('textarea[data-counter="needs_counter"]').each(function() {
        console.log('found textarea')
        var max = 140;
        var c = django.jQuery("<span class='counter'></span>");
        var field = django.jQuery(this);
        field.after(c);
        c.after('  characters remaining');
        c.css("margin-left","10px");
        c.css("padding", "0 3px 0 3px");
        c.css("border", "1px solid #ccc");

        function get_remaining() {
            var cur = field.attr('value').length;
            var remaining = max - cur;
            c.text(remaining.toString());

            if(remaining <= 10) {
                c.css("background","#F4F379");
            } else {
                c.css("background","none");
            }
        }
        get_remaining();
        
        field.keyup(function() {
            get_remaining();
        });
        django.jQuery("#id_link").change(function() {
            if (this.value.length > 0) {
                c.text(c.text() - this.value.length);
            }
        });
    });
});
