/* Peta lokalizasaun MDI + rota (Leaflet). Data husi atributu data-* iha #mdiLeafletMap. */
window.MDI = window.MDI || {};
window.MDI.initHomeMap = function(){
  var mapEl = document.getElementById('mdiLeafletMap');
  if (!mapEl || typeof L === 'undefined') return;

  var lat = parseFloat(mapEl.getAttribute('data-lat'));
  var lng = parseFloat(mapEl.getAttribute('data-lng'));
  var placeName = mapEl.getAttribute('data-name') || 'Mata Dalan Institute';
  var placeAddress = mapEl.getAttribute('data-address') || '';

  var map = L.map('mdiLeafletMap', { scrollWheelZoom: false }).setView([lat, lng], 15);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
  }).addTo(map);

  L.control.scale({ imperial: false }).addTo(map);

  var mdiIcon = L.divIcon({
    className: 'mdi-map-pin',
    html: '<i class="bi bi-geo-alt-fill"></i>',
    iconSize: [34, 34],
    iconAnchor: [17, 32],
    popupAnchor: [0, -30]
  });

  var destMarker = L.marker([lat, lng], { icon: mdiIcon }).addTo(map);
  destMarker.bindPopup('<strong>' + placeName + '</strong><br>' + placeAddress).openPopup();

  // Klik di peta manapun bebas re-enable scroll zoom, atu UX diak liu iha desktop
  map.on('focus', function(){ map.scrollWheelZoom.enable(); });
  map.on('blur', function(){ map.scrollWheelZoom.disable(); });

  var routeBtn = document.getElementById('mdiRouteBtn');
  var statusEl = document.getElementById('mdiRouteStatus');
  var routingControl = null;

  function showStatus(msg){
    if (!statusEl) return;
    statusEl.style.display = 'block';
    statusEl.textContent = msg;
  }

  if (routeBtn) {
    routeBtn.addEventListener('click', function(){
      if (!navigator.geolocation) {
        showStatus('Jeolokalizasaun la suporta iha navegador ida-ne\'e.');
        return;
      }
      routeBtn.disabled = true;
      var originalHtml = routeBtn.innerHTML;
      routeBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Buka lokalizasaun...';

      navigator.geolocation.getCurrentPosition(function(pos){
        var userLat = pos.coords.latitude;
        var userLng = pos.coords.longitude;

        if (routingControl) { map.removeControl(routingControl); }

        window.MDI.loadRouting().then(function(){
        routingControl = L.Routing.control({
          waypoints: [
            L.latLng(userLat, userLng),
            L.latLng(lat, lng)
          ],
          routeWhileDragging: false,
          addWaypoints: false,
          draggableWaypoints: false,
          fitSelectedRoutes: true,
          show: true,
          lineOptions: {
            styles: [{ color: '#A11D26', weight: 5, opacity: 0.85 }]
          },
          createMarker: function(i, wp) {
            if (i === 0) {
              return L.marker(wp.latLng, {
                icon: L.divIcon({
                  className: 'mdi-map-pin mdi-map-pin-user',
                  html: '<i class="bi bi-person-fill"></i>',
                  iconSize: [30, 30], iconAnchor: [15, 28]
                })
              }).bindPopup('Ita nia lokalizasaun');
            }
            return destMarker;
          }
        }).addTo(map);
        });

        routeBtn.innerHTML = originalHtml;
        routeBtn.disabled = false;
        showStatus('');
        statusEl.style.display = 'none';
      }, function(err){
        routeBtn.innerHTML = originalHtml;
        routeBtn.disabled = false;
        showStatus('La bele hetan ita nia lokalizasaun. Favor lisensa asesu jeolokalizasaun iha browser.');
      }, { enableHighAccuracy: true, timeout: 10000 });
    });
  }
};
