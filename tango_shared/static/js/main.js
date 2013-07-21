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

var small_screen = false;
if (document.width < 800 ){
  small_screen = true;
}

/*************
// Simple trigger handling.
// Takes hash from trigger link and toggles the object.
// Example: <a href="#foo" class='trigger'>
// would automatically hide the #foo element, then toggle it onclick.
// Also allows child selectors:
//    <a href="#foo>ul" class="trigger">
//    <a href="#foo>.bar" class="trigger">
// Note that the child selector does not have to be a direct descendant.
// It will toggle any matching children of the main selector.
********************************/
$('a.trigger').each(function(){
  var hash = this.hash;
  // check for child selector. Wait, what?
  if (hash.split(">").length > 1) {
    if (document.width > 1000 ){
      hash = hash.split(">")[0] + ' ' + hash.split(">")[1];
    } else {
      hash = hash.split(">")[0];
    }
  }
  $(hash).hide();
  $(this).click(function(e) {
    e.preventDefault();
    $(hash).toggle();
    $(this).toggleClass('activated');
  });
});

// Simple URL jumpbox
$('.url_selector').change(function() {
  window.location = $(this).val();
});


// pickadate.js
$( '.datepicker' ).pickadate({
    format: 'dddd, dd mmm, yyyy',
    format_submit: 'yyyy-mm-dd'
});


// Allows deferred loading of images.
// Parent element must have data-deferred-load=" <src>"
function load_images() {
  $('*[data-deferred-load]').prepend(function() {
    var hash = $(this).attr('data-deferred-load');
    if (small_screen) {
      hash = hash.replace('540x540','360x360');
    }
    var img = document.createElement('img');
      img.src = hash;
     return img;
  });
}
load_images();





/* tabs can be used two ways:
  With inside navigation:
    container.tabs
      ul
      tab block
      tab block
  or with remote navigation
    ul.remote_tabs_tabbed.nav(anywhere on the page
    container.tabs
      tab block
      tab block
  
  within ul, a.active denotes active tab.
  If no active tab is set, the first will be the default.

  A tab block can be any block level element other than a UL, so div, article, section, etc will all work.
  UL is reserved for nav. If you need a UL, wrap it.

  tabit respects page hash, so foo.com/#bar
  will go to the #bar tab
  
  You must set the container class to .tabs.
  When tabs are activated, it will be given the class .tabbed,
  so you can style it appropriately and only style blocks that have been tabbed.
  
  And remember to call tabit()
 */
function tabit() {
  $('.tabs').each(function() {
    var tabbed       = $(this),
        active       = '';

    tabbed.addClass('tabbed');
    tabbed.sections  = $(this).find('> *').not('ul');
    tabbed.nav       = tabbed.find('> ul');
    var nav_height   = tabbed.nav.height();

    if (tabbed.nav.length === 0) {
        tabbed.nav= $('.remote_tabs_nav');
        nav_height = 0;
      }
    if (!tabbed.nav) {
        //console.log('could not find tab nav!');
        return;
      }
    //tabbed.sections.hide(); // Should be done in css, but fallback for safety.
    tabbed.navitems = tabbed.nav.find('li');
    
    if (window.location.hash) {
        active = window.location.hash.replace('-view','');
        if (tabbed.nav) {
          tabbed.navitems.removeClass('active');
          tabbed.nav.find('a[href='+active+']').parent().addClass('active');
        }
      } else { // no hash available. check if one was pre-defined.
        active = tabbed.nav.find('li.active a').hash;
        if (!active) { // or set it to first item
          active = tabbed.navitems.eq(0).addClass('active').find('a').get(0).hash;
        }
      }
    $(active).addClass('activeTab');
    
    tabbed.nav.find('a:not(.no-tab)').click(function(e) {
      e.preventDefault();
      var target          = this.hash,
          tabbed_sections = $(target).parent().find('> *').not('ul');

      window.location.hash = target + '-view';
      var parent = $(this).parent();
      parent.addClass('active');
      var navitems = parent.parent().find('li');
      $(navitems).not(parent).removeClass('active');
      $(target).addClass('activeTab');
      // ensure the container height will be at least the target height...
      // it'll make the css much easier
      tabbed.css('min-height', $(target).height() + nav_height + 'px');
      tabbed_sections.not(target).removeClass('activeTab');
    });
  });
}
tabit();


var $top_assets = $('#top_assets');


if ($top_assets.length > 0) {
  // functions specific to pages with top assets.
  // note this is after the tabit() call, so it calculates
  // based on tabbed top asset height, not default.
  
  // create preview tooltips in story detail top assets
  $top_assets.find('.tabbed ul li a:not(.no-tab)').each(function() {
    var img = $(this.hash).find('img').eq(0);
    var preview = '<span class="preview"><img src="'+ $(img).attr('src') + '"></span>';
    if ($(img).size() === 0) {
      img = $(this.hash).first('object');
      preview = '<span class="preview">Video</span>';
    }
    $(this).append(preview);
  });
  $top_assets.find('.tabbed ul li').hover(function() {
    $(this).find('.preview').toggle();
  });
    // sets top margin for more assets to ensure it's pushed below top assets
  $(document).ready(function() {
  });
}
