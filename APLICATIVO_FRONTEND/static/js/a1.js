var botonMenu = document.getElementById("boton-menu");
if (botonMenu) {
    botonMenu.addEventListener("click", function () {
        document.getElementById("menu").classList.toggle("abierto");
    });
}

// los avisos se cierran al hacer click o a los 6 segundos
var avisos = document.querySelectorAll(".aviso");
for (var i = 0; i < avisos.length; i++) {
    avisos[i].addEventListener("click", function () {
        this.style.display = "none";
    });
    setTimeout(function (aviso) {
        aviso.style.display = "none";
    }, 6000, avisos[i]);
}

// pide confirmacion antes de enviar los formularios marcados con data-confirmar
var formularios = document.querySelectorAll("form[data-confirmar]");
for (var j = 0; j < formularios.length; j++) {
    formularios[j].addEventListener("submit", function (evento) {
        if (!confirm(this.getAttribute("data-confirmar"))) {
            evento.preventDefault();
        }
    });
}

// los selects marcados con data-autoenviar envian el formulario al cambiar
var selects = document.querySelectorAll("select[data-autoenviar]");
for (var k = 0; k < selects.length; k++) {
    selects[k].addEventListener("change", function () {
        this.form.submit();
    });
}

// en la compra, actualiza el total al cambiar la cantidad
var cantidad = document.getElementById("cantidad");
if (cantidad) {
    cantidad.addEventListener("input", function () {
        var precio = parseFloat(cantidad.getAttribute("data-precio"));
        var entradas = parseInt(cantidad.value);
        if (isNaN(entradas) || entradas < 1) {
            entradas = 1;
        }
        var total = precio * entradas;
        var texto = total.toLocaleString("es-AR", { maximumFractionDigits: 2 });
        document.getElementById("cant-texto").textContent = entradas;
        document.getElementById("total-texto").textContent = "$ " + texto;
        document.getElementById("total-final").textContent = "$ " + texto;
    });
}

// en el pago, cuenta regresiva hasta que vence el QR 
var cuenta = document.getElementById("cuenta");
if (cuenta) {
    var restantes = parseInt(cuenta.getAttribute("data-segundos"));
    var reloj = setInterval(function () {
        restantes = restantes - 1;
        if (restantes <= 0) {
            clearInterval(reloj);
            location.reload();
            return;
        }
        var minutos = Math.floor(restantes / 60);
        var segundos = restantes % 60;
        if (segundos < 10) {
            segundos = "0" + segundos;
        }
        cuenta.textContent = minutos + ":" + segundos;
    }, 1000);
}

var fechas = document.querySelectorAll('input[type="date"]');//solo ingresan la fecha por calendario
for (var i = 0; i < fechas.length; i++) {
    fechas[i].style.cursor = "pointer";
    fechas[i].onclick = function () {
        this.showPicker();
    };
    fechas[i].onkeydown = function () {
        return false;
    };
}
