let headerNav = document.querySelector('nav');

// Cuando deslizas hacia abajo, el nav se vuelve opaco
window.addEventListener('scroll', () => {
  if (window.scrollY > 0) {
    headerNav.classList.add('scrolled');
  } else {
    headerNav.classList.remove('scrolled');
  }

  // Mostrar el botón "subir" si se ha desplazado más de 200px
  let subir = document.querySelector('.subir');
  if (window.scrollY > 200) {
    subir.style.display = 'block';
  } else {
    subir.style.display = 'none';
  }

  // Desplazar los artistas hacia abajo
  let arts = document.querySelectorAll('.art');
  let triggerPoint = window.innerHeight / 1.2; // Punto de activación

  arts.forEach((art, index) => {
    let artTop = art.getBoundingClientRect().top;

    if (artTop < triggerPoint) {
      setTimeout(() => {
        art.style.display = 'block'; // Mostrar el div
        art.style.transform = 'translateY(0)'; // Restablecer la posición
        art.style.opacity = '1'; // Hacerlo visible
      }, index * 100); // Retraso basado en el índice
    }
  });
});

// Manejo de botones que muestran cosas dependiendo de cuál se pulse
document.addEventListener('DOMContentLoaded', function() {
  let btn1 = document.getElementById('btn1');
  let btn2 = document.getElementById('btn2');
  let div1 = document.getElementById('div1');
  let div2 = document.getElementById('div2');

  btn1.addEventListener('click', function() {
    div1.style.display = 'block'; // Muestra div1
    div2.style.display = 'none'; // Oculta div2
    // Aumenta el margen inferior del main
    let mainElement = document.querySelector('main');
    mainElement.style.marginBottom = '700px'; // Cambia el valor según sea necesario
  });

  btn2.addEventListener('click', function() {
    div2.style.display = 'block'; // Muestra div2
    div1.style.display = 'none'; // Oculta div1
    // Aumenta el margen inferior del main
    let mainElement = document.querySelector('main');
    mainElement.style.marginBottom = '700px'; // Cambia el valor según sea necesario
  });
});

 // Deslizar las columnas hacia dentro
 let columnsSection = document.getElementById('columns-section');
 let leftColumn = document.querySelector('.left-column');
 let rightColumn = document.querySelector('.right-column');

 window.addEventListener('scroll', function() {
   let rect = columnsSection.getBoundingClientRect();
   
   // Verifica si la sección está en la vista
   if (rect.top < window.innerHeight && rect.bottom > 0) {
     leftColumn.classList.add('visible');
     rightColumn.classList.add('visible');
   }
 });