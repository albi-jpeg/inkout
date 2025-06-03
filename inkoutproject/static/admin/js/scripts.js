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
})

// Desplazar los artistas hacia abajo
document.addEventListener("DOMContentLoaded", function () {
  let arts = document.querySelectorAll('.art');
  let triggerPoint = window.innerHeight / 1.2;

  window.addEventListener('scroll', function () {
    arts.forEach((art, index) => {
      let artTop = art.getBoundingClientRect().top;
      if (artTop < triggerPoint) {
        setTimeout(() => {
          art.classList.add('visible');
        }, index * 100);
      }
    });
  });
});


document.addEventListener('DOMContentLoaded', function () {
  let btn1 = document.getElementById('btn1');
  let btn2 = document.getElementById('btn2');
  let div1 = document.getElementById('div1');
  let div2 = document.getElementById('div2');

  if (btn1 && div1 && div2) {
    btn1.addEventListener('click', function () {
      div1.classList.remove('d-none');
      div1.classList.add('d-flex');
      div2.classList.add('d-none');
      div2.classList.remove('d-flex');
    });
  }

  if (btn2 && div2 && div1) {
    btn2.addEventListener('click', function () {
      div2.classList.remove('d-none');
      div2.classList.add('d-flex');
      div1.classList.add('d-none');
      div1.classList.remove('d-flex');
    });
  }
});


// Deslizar las columnas hacia dentro
let columnsSection = document.getElementById('columns-section');
let leftColumn = document.querySelector('.left-column');
let rightColumn = document.querySelector('.right-column');

window.addEventListener('scroll', function () {
  let rect = columnsSection.getBoundingClientRect();

  // Verifica si la sección está en la vista
  if (rect.top < window.innerHeight && rect.bottom > 0) {
    leftColumn.classList.add('visible');
    rightColumn.classList.add('visible');
  }
});

// Función para alternar visibilidad de las citas
function toggleCitas(divId) {
  var div = document.getElementById(divId);
  if (window.getComputedStyle(div).display === "none") {
    div.style.display = "block";
  } else {
    div.style.display = "none";
  }
}

// Función para alternar visibilidad de los mensajes
function toggleMensajes(divId) {
  var div = document.getElementById(divId);
  if (window.getComputedStyle(div).display === "none") {
    div.style.display = "block";
  } else {
    div.style.display = "none";
  }
}

