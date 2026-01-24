// arreglo de productos
const productos = [
    { id: 1, nombre: "Producto A", precio: 120, descripcion: "Descripcion A" },
    { id: 2, nombre: "Producto B", precio: 210, descripcion: "Descripcion B" },
    { id: 3, nombre: "Producto C", precio: 270, descripcion: "Descripcion C" }
];

// referencias al DOM
const ul = document.getElementById("listaProductos");
const btnAgregar = document.getElementById("btnAgregar");

// renderizar productos
function renderizarProductos() {
    ul.innerHTML = "";

    productos.forEach(producto => {
        const li = document.createElement("li");
        li.textContent = `${producto.nombre} - $${producto.precio} - ${producto.descripcion}`;
        ul.appendChild(li);
    });
}

// agregar producto
function agregarProducto() {
    const nuevoProducto = {
        id: productos.length + 1,
        nombre: "Producto Nuevo",
        precio: 50,
        descripcion: "Descripcion Nueva"
    };

    productos.push(nuevoProducto);
    renderizarProductos();
}

// eventos
btnAgregar.addEventListener("click", agregarProducto);

// render inicial
renderizarProductos();