function mostrarAlerta() {
    alert("Esta es una alerta personalizada usando JavaScript");
}

function validarFormulario(event) {
    event.preventDefault();

    let nombre = document.getElementById("nombre").value;
    let correo = document.getElementById("correo").value;
    let mensaje = document.getElementById("mensaje").value;

    if (nombre === "" || correo === "" || mensaje === "") {
        document.getElementById("error").textContent =
            "Todos los campos son obligatorios";
    } else {
        alert("Formulario enviado correctamente");
        document.getElementById("error").textContent = "";
    }
}