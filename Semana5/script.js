// Obtener elementos por ID (DOM)
const inputUrl = document.getElementById("urlImagen");
const btnAgregar = document.getElementById("btnAgregar");
const btnEliminar = document.getElementById("btnEliminar");
const galeria = document.getElementById("galeria");

let imagenSeleccionada = null;

// Evento click para agregar imagen
btnAgregar.addEventListener("click", () => {
    const url = inputUrl.value;

    if (url === "") {
        alert("Ingrese una URL de imagen");
        return;
    }

    const img = document.createElement("img");
    img.src = url;
    img.onerror = () => {
    alert("La URL no es una imagen válida");
    img.remove();
    };
    // Evento click para seleccionar imagen
    img.addEventListener("click", () => {

        if (imagenSeleccionada) {
            imagenSeleccionada.classList.remove("seleccionada");
        }

        img.classList.add("seleccionada");
        imagenSeleccionada = img;
    });

    galeria.appendChild(img);
    inputUrl.value = "";
});

// Evento click para eliminar imagen seleccionada
btnEliminar.addEventListener("click", () => {

    if (imagenSeleccionada) {
        galeria.removeChild(imagenSeleccionada);
        imagenSeleccionada = null;
    } else {
        alert("No hay imagen seleccionada");
    }

});

// Evento keydown (tecla Delete)
document.addEventListener("keydown", (evento) => {
    if (evento.key === "Delete" && imagenSeleccionada) {
        galeria.removeChild(imagenSeleccionada);
        imagenSeleccionada = null;
    }
});