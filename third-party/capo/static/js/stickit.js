/***********************************************
* Stickit allows for multiple sticky elements,
* allows them be combined with a sticky header,
* allows for expanding/collapsing header navigation,
* and prevents overflow of the sticky element to the
* header or footer.
*
* The sticky sidebar functionality is heavily based on
* stickymojo.js: http://mojotech.github.com/stickymojo/
* If that's all you need, then it's probably better.
*
* If using a collapsing header,
* hide/show content in the nav based on body.collapsed
*
* Initialization:
* Pass a class name for the elements you want to be sticky,
* along with some variables:
*
* $(window).load(function() {
    $('.sticky').stickit({
    content: '#content-main', // your main content wrapper (not the sidebar)
    footer:  '#footer',
    header:  '#header'
  });
});

* additional settings:
* - stickHeader: false      (if header should not stick)
* - collapseHeader: false   (no collapsing will be done)

* Relies on getYOffset from main.js.
if not in place, add this:

// Reliably get window position.
function getYOffset() {
  var pageY;
  if(typeof(window.pageYOffset) === 'number') {
     pageY=window.pageYOffset;
  }
  else {
     pageY=document.documentElement.scrollTop;
  }
  return pageY;
}

**************************************************/

(function($) {
  $.fn.extend({
    stickit: function(options) {
      var $stickyElements = $(this);
      var settings = $.extend({
        //'debug': 'false',
        'stickHeader': true,
        'collapseHeader': true,
        'header':  '#masthead',
        'footer':  '#footer',
        'content': '#content-main'
      }, options);

      var errors = [];
      for (var key in settings) {
        if (!settings[key]) {
          errors.push(settings[key]);
        }
      }
      if (errors.length) {
        console.warn(errors);
        return false;
      }
      // we're going to compute the content top position
      // based on the first element AFTER the header,
      // in case there is any margin/padding oddness.
      var winPos;
      var limits;
      var $win = $(window);
      var $body = $('body');
      var $header = $(settings.header);
      var $footer = $(settings.footer);
      var $content = $(settings.content);
      var $firstContent = $header.next();
      var contentOffset = $firstContent.offset().top;
      var headerHeight = $header.outerHeight();

      // if we're sticking the header.
      function calcContentTop() {
        headerHeight = $header.outerHeight();
        if (settings.stickHeader) {
          $header.css('position', 'fixed');
          $firstContent.css('margin-top', Math.max(contentOffset, headerHeight));
        }
      }

      // if we're collapsing the header.
      if (settings.collapseHeader) {
        var collapsed = $body.hasClass('collapsed');
      }

      // Header helpers
      function collapseHeader() {
        $body.addClass('collapsed');
        collapsed = true;
        calcContentTop();
      }
      function unCollapseHeader() {
        $body.removeClass('collapsed');
        collapsed = false;
        calcContentTop();
      }

      // Build sticky elements
      $stickyElements.each(function() {
        var $thisParent = $(this).parent();
        $thisParent.css('position', 'relative');
        this.sticky = {
          'stickyHeight': $(this).outerHeight(true),
          'breakPoint': $(this).outerWidth(true) + $content.outerWidth(true),
          'topOffset': $(this).offset().top, // measured from window top...
          'topPos': $(this).position().top,  // measured from parent.
          'parent': $thisParent
        };
      });

      // on scroll, does anything need to change?
      function checkForChanges() {
        winPos = getYOffset();
        if (settings.collapseHeader) {
          // collapse when offset is 2/3 of height.
          // In other words, if the full header is 300px
          // you want to collapse when the offset is 200px.
          if (collapsed === false && winPos > (contentOffset / 3)) {
            collapseHeader();
          }
          if (collapsed === true && winPos < (contentOffset / 8)) {
            unCollapseHeader();
          }
        }

        // if we're in position to have sticky sidebar elements...
        if (winPos === 0 || winPos > contentOffset) {
          $stickyElements.each(function() {
            if (this.sticky.topOffset - headerHeight < winPos && $win.width() >= this.sticky.breakPoint) {
              limits = calculateLimits(this);
              setFixedSidebar(this, winPos, limits);
            } else {
              setStaticSidebar(this);
            }
          });
        }
      }

      //  Calculates the limits top and bottom limits for the sidebar
      function calculateLimits(elem) {
        return {
          lowerLimit: ($footer.offset().top + elem.sticky.stickyHeight) + headerHeight,
          upperLimit: elem.sticky.topPos - headerHeight // offset in parent - header height
        };
      }
      // sets sidebar to a static positioned element
      function setStaticSidebar(elem) {
        $(elem).css({
          'position': 'static',
          'width': 'auto'
        });
      }
      // Sets sidebar to fixed position
      function setFixedSidebar(elem, winPos, limits) {
        if (limits.lowerLimit < winPos) {
          // avoid overlap with footer
          $(elem).css({
          top: limits.lowerLimit
          });
        } else { // normal fixed sidebar
          $(elem).css({
            position: 'fixed',
            top: limits.upperLimit,
            width: elem.sticky.parent.width()
          });
        }
      }

      // Listen for window scroll and check for changes.
      $win.bind({
        'scroll': checkForChanges,
        'resize': checkForChanges()
      });

      // nav menu trigger expand/collapse
      $('#menu-trigger').click(function(e) {
        e.preventDefault();
        if (collapsed === true) {
          window.scrollTo(0, 0);
          unCollapseHeader();
        } else {
          collapseHeader();
          window.scrollTo(0, headerHeight-30);
        }
        $firstContent.css('margin-top', headerHeight);
      });
    }
  });
})(jQuery);
