// smooth scroll
$(document).ready(function(){
    $(".navbar .nav-link").on('click', function(event) {

        if (this.hash !== "") {

            event.preventDefault();

            var hash = this.hash;

            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 700, function(){
                window.location.hash = hash;
            });
        }
    });
});

new WOW().init();

function initMap() {
    var uluru = {lat: -4.0304546116356565, lng: -79.2000953489245};
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 17,
      center: uluru
    });
    var marker = new google.maps.Marker({
      position: uluru,
      map: map
    });
}

function actualizarHora() {
    var ahora = new Date();
    var hora = ahora.getHours().toString().padStart(2, '0');
    var minutos = ahora.getMinutes().toString().padStart(2, '0');
    var segundos = ahora.getSeconds().toString().padStart(2, '0');
    var horaActual = hora + ':' + minutos + ':' + segundos;
    document.getElementById('hora').textContent = horaActual;
}

setInterval(actualizarHora, 1000);
actualizarHora(); // Llamar inmediatamente para mostrar la hora sin esperar un segundo


// Cronometro
