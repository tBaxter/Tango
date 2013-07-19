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

**************************************************/(function(e){e.fn.extend({stickit:function(t){function c(){m=!0;v.addClass("collapsed");r.stickHeader&&p();l=r.header.outerHeight()}function h(){m=!1;v.removeClass("collapsed");r.stickHeader&&d();l=r.header.outerHeight()}function p(){r.header.css("position","fixed");a.css("margin-top",f)}function d(){r.header.css("position","static");a.css("margin-top",0)}function y(){o=S.scrollTop();if(r.collapseHeader){o>g&&m===!1&&c();o<g&&m===!0&&h()}n.each(function(){if(this.sticky.topOffset-l-30<o&&S.width()>=this.sticky.breakPoint){u=b(this);E(this,o,u)}else w(this)})}function b(e){return{lowerLimit:r.footer.offset().top+e.sticky.stickyHeight+l,upperLimit:e.sticky.topPos-l+30}}function w(t){e(t).css({position:"static",width:"auto"})}function E(t,n,r){r.lowerLimit<n?e(t).css({top:r.lowerLimit}):e(t).css({position:"fixed",top:r.upperLimit,width:t.sticky.parent.width()})}var n=e(this),r=e.extend({debug:"false",stickHeader:!0,collapseHeader:!0,header:e("#masthead"),footer:e("#footer"),content:e("content-main")},t),i=[];for(var s in r)r[s]||i.push(r[s]);if(i.length){console.warn(i);return!1}var o,u,a=r.header.next(),f=a.offset().top,l=r.header.outerHeight();if(r.collapseHeader||r.stickHeader){var v=e("body");if(r.collapseHeader)var m=v.hasClass("collapsed"),g=f*.6;else r.stickHeader&&p()}n.each(function(){var t=e(this).parent();t.css("position","relative");this.sticky={stickyHeight:e(this).outerHeight(!0),breakPoint:e(this).outerWidth(!0)+e(r.contentID).outerWidth(!0),topMargin:parseInt(e(this).css("margin-top"),10),topOffset:e(this).offset().top,topPos:e(this).position().top,parent:t}});var S=e(window);S.bind({scroll:y,resize:y()});e("#menu-trigger").click(function(e){e.preventDefault();if(m===!0){h();window.scrollTo(0,0)}else c()})}})})(jQuery);