// static/js/habitaciones.js

let currentIndex = 0; // Índice de la imagen actual
const images = document.querySelectorAll('.carrusel-imagenes img');

function showImage(index) {
    images.forEach((img, i) => {
        img.classList.remove('active'); // Elimina la clase 'active' de todas las imágenes
        if (i === index) {
            img.classList.add('active'); // Agrega la clase 'active' a la imagen actual
        }
    });
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length; // Incrementa el índice y vuelve al inicio si es necesario
    showImage(currentIndex); // Muestra la imagen correspondiente
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length; // Decrementa el índice y vuelve al final si es necesario
    showImage(currentIndex); // Muestra la imagen correspondiente
}

// Inicializa mostrando la primera imagen
showImage(currentIndex);