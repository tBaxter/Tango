var screenWidth    = $(document).width();
var previous       = '#gallery_info .prev';
var next           = '#gallery_info .next';
var caption_hold   = $('#caption_hold');
var gallery_thumbs = $('#gallery_thumbs li');

// helper function to load in images as needed
// by default, only the first image is loaded.
// This uploads the next img in the gallery, too.
function load_img(next) {
  if ($(next).find('img').length === 0) {
    //console.log('loading img into next figure: '+ $(next).attr('id'))
    $(next).prepend('<img alt="" src="' + $(next).attr('data-load-on-demand') + '">');
  }
}

function slide_callback(next) {
  //console.log('slide_callback running')
  //console.log(next)
  next_sibling = $(next).next();
  load_img(next);
  load_img(next_sibling);

  caption = $(next).find('.caption').html();
  if ($(caption_hold).html() != caption) {
    $(caption_hold).html(caption);
  }
  idx = $(next).attr('id').replace('image_','');
  $('#gallery_index').html(idx);
  $(gallery_thumbs).removeClass('current');
  $(gallery_thumbs).eq(idx).addClass('current');
  if (idx > 1) {
    // recalculate height for new image
    //console.log(idx)
    height =  $('#image_'+idx).height();
    $('#gallery_slides').height(height+20);
    //console.log('new height....' + height)
    
    // and update analytics
    if (typeof(_gaq) != 'undefined'){
      _gaq.push(['_trackPageview']);
    }
  }
}

// check for initial hash and set starting index (idx) accordingly
if (window.location.hash && (window.location.hash.indexOf("slide-") != -1)) {
  var idx = $(window.location.hash.replace('slide-','image_')).index();
  $('#gallery_index').html(idx+1);
} else {
  var idx = 0;
}

function gallerize() {
  if ($('#gallery_slides > figure').size() > 1) {

    $('#gallery_slides > figure').each(function() {
      $(this).attr('title','Click or swipe for next photo');
    });

    // callback doesn't run on init, so we're going to init...
    slide_callback($('#gallery_slides > figure').eq(idx));
    // then decrement idx, since we just effectively increased it.
    idx = idx - 1;

    // browser supports css transitions. Use swipe.js
    if ( Modernizr.csstransitions  ) {
      //console.log('using swipe')
      var swipe_slider = new Swipe(document.getElementById('gallery_slides_hold'), {
        startSlide: idx,
        speed:      400,
        callback:   function(event, index, elem) {
          next_slide = ($('#gallery_slides > figure').eq(index));
          //console.log('got next slide')
          slide_callback(next_slide);
        }
      });
      $('#gallery_info .next').click(function() {
        swipe_slider.next();
        gallery_thumbs.next();
      });
      $('#gallery_info .prev').click(function() {
        swipe_slider.prev();
        gallery_thumbs.prev();
      });
    } else { // browser can't use swipe.js. Fall back on cycle.
      //console.log('using cycle')
      $('#gallery_slides').cycle({
        speed:              100,
        pause:              1,
        nowrap:             1,
        timeout:            0,
        startingSlide:      idx,
        slideResize:        0,
        fx:                 'scrollHorz',
        activePagerClass:   'current',
        prev:               previous,
        next:               next,
        pager:              'ul#gallery_thumbs',
        pagerAnchorBuilder: function(idx, slide) {return 'ul#gallery_thumbs li:eq(' + idx + ') ';},
        before:             function(curr,next,opts) {slide_callback(next);}
      });
    }
    // cycle on image click
    $('#gallery_slides > figure').click(function(e) {
      if (swipe_slider) {
        swipe_slider.next();
        gallery_thumbs.next();
      } else {
        $('#gallery_info .next').click();
      }
    });
    // cycle on key (arrow) press
    $(document).keydown(function(e){
      if(e.which == 37){
        if (swipe_slider) {
          swipe_slider.prev();
          gallery_thumbs.prev();
        } else {
          $('#gallery_info .prev').click();
        }
      }
      else if(e.which == 39){
        if (swipe_slider) {
          swipe_slider.next();
          gallery_thumbs.next();
        } else {
          $('#gallery_info .next').click();
        }
      }
    });
  }
}

/* below 1000, we're not showing thumbs, as defined in css media query */
if (Modernizr.touch === false && screenWidth > 780) {
  $('*[data-deferred-thumbs]').prepend(function(index){
      var hash = $(this).attr('data-deferred-thumbs');
       return '<img alt="" src="' + hash + '">';
  });
  // Help the thumby nav rotate
  /*
  $('#gallery_thumbs').jcarousel({
    scroll              : 1,
    visible             : 12,
    animation           : 200,
    itemFirstInCallback : function(carousel, item, idx, state) {
      // It is not smart re-running this selector every time.
      $('#gallery_thumbs li').removeClass('current');
      $(item).addClass('current'); 
      //console.log('Item #' + idx + ' is now the first item')
      },
    setupCallback       : function() {
      $('#gallery_thumbs_hold').show();
    }
  });
  gallery_thumbs = $('#gallery_thumbs').data('jcarousel');
  */
}
gallerize()