const formulario = document.getElementById("miFormulario");
const btnEnviar = document.getElementById("btnEnviar");

const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const password = document.getElementById("password");
const confirmar = document.getElementById("confirmar");
const edad = document.getElementById("edad");

function validarFormulario() {
  if (
    nombre.classList.contains("valido") &&
    correo.classList.contains("valido") &&
    password.classList.contains("valido") &&
    confirmar.classList.contains("valido") &&
    edad.classList.contains("valido")
  ) {
    btnEnviar.disabled = false;
  } else {
    btnEnviar.disabled = true;
  }
}

// Nombre
nombre.addEventListener("input", () => {
  if (nombre.value.length < 3) {
    errorNombre.textContent = "Mínimo 3 caracteres";
    nombre.className = "invalido";
  } else {
    errorNombre.textContent = "";
    nombre.className = "valido";
  }
  validarFormulario();
});

// Correo
correo.addEventListener("input", () => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(correo.value)) {
    errorCorreo.textContent = "Correo no válido";
    correo.className = "invalido";
  } else {
    errorCorreo.textContent = "";
    correo.className = "valido";
  }
  validarFormulario();
});

// Contraseña
password.addEventListener("input", () => {
  if (password.value.length < 8) {
    errorPassword.textContent = "Mínimo 8 caracteres";
    password.className = "invalido";
  } else {
    errorPassword.textContent = "";
    password.className = "valido";
  }
  validarFormulario();
});

// Confirmar contraseña
confirmar.addEventListener("input", () => {
  if (confirmar.value !== password.value) {
    errorConfirmar.textContent = "No coincide";
    confirmar.className = "invalido";
  } else {
    errorConfirmar.textContent = "";
    confirmar.className = "valido";
  }
  validarFormulario();
});

// Edad
edad.addEventListener("input", () => {
  if (edad.value < 18) {
    errorEdad.textContent = "Debe ser mayor de edad";
    edad.className = "invalido";
  } else {
    errorEdad.textContent = "";
    edad.className = "valido";
  }
  validarFormulario();
});

// Envío
formulario.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Formulario validado correctamente");
});