
<script src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script>
  function build_map() {
    var map_canvas = document.getElementById("map_canvas");
    if (!map_canvas) {
      return false
    }
    var map   = new google.maps.Map(map_canvas, mapOptions);    
    var styles = [{
      stylers: [
        { hue: "#ee6633" },
        { saturation: -80 }
      ]
    }];
    var iw = new google.maps.InfoWindow(); // global infowindow
    var markersArray = [];
    var mapOptions = { // Defaults
          zoom: 7,
          center: new google.maps.LatLng(39.0997265, -94.5785667),
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          minZoom: 2,
          maxZoom: 18,
          styles: styles
    };

    // mapping functions
    function clearOverlays() {
      if (markersArray) {
        for (i in markersArray) {
          markersArray[i].setMap(null);
        }
      }
    }

    function create_markers() {
      clearOverlays()
      var bounds = new google.maps.LatLngBounds(); 
      var cards = $('.vevent');
      
      $(cards).each(function() {
        geocode = $(this).attr('data-geocode');
        if (geocode != "None") {
          geocode = geocode.split(',');
          myLatLng = new google.maps.LatLng(geocode[0], geocode[1].replace(' ',''));
          marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: $(this).find('strong').attr('data-date')
          });
          markersArray.push(marker);

          info = '<strong>' + $(this).find('.summary').html() +'</strong><br> ' + 
              $(this).find('.event_times').text() +'<br>' +
              $(this).find('.org').html() + '<br>' + $(this).find('.adr').html();
          iw_string = info;
          createInfoWindow(marker, iw_string)
          bounds.extend(myLatLng);
          map.fitBounds(bounds);
          // control zoom levels not too far in, not too far out.
          zoomChangeBoundsListener = google.maps.event.addListener(map, 'bounds_changed', function(event) {
            //console.log('zoom '+ this.getZoom())
            if (this.getZoom() > 17){
              this.setZoom(this.getZoom() - 2);
              google.maps.event.clearListeners(map, 'bounds_changed');
            }
            //console.log('newzoom '+ this.getZoom())
          });
        }
      });
      function createInfoWindow(marker, content) {
        google.maps.event.addListener(marker, 'click', function(){
          iw.setContent(content);
          iw.open(map, marker);
        });
      } // end info window creation
    } // end create markers
    create_markers();
  }
  build_map();
</script> 
