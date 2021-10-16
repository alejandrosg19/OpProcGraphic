let left = 3;
let right = 1;

document.addEventListener('DOMContentLoaded', () => {

    const info_pages = document.querySelectorAll('.info-page');
    info_pages.forEach((elemento)=>{
        elemento.style.width = `calc( 100% / ${info_pages.length})`
    })
    const slider = document.querySelector('.slider');

    slider_pages = info_pages.length;
    left = slider_pages;
    slider.style.width = `${slider_pages}00%`;
    
    
    document.querySelector(".btn-left").onclick = () =>{
        selected =  document.querySelector(".slider");
        if(left < slider_pages && left > 0){
            selected.style.marginLeft = `${(selected.style.marginLeft == "0%" || selected.style.marginLeft == "" ? 0 : parseInt(selected.style.marginLeft)) + 100}%`;
            left++;
            right--;
        }       
    }

    document.querySelector(".btn-right").onclick = () =>{
        selected =  document.querySelector(".slider");
        if(right < slider_pages && right > 0){
            selected.style.marginLeft =  `${(selected.style.marginLeft == "" ? 0 : parseInt(selected.style.marginLeft)) - 100}%`;
            left--;
            right++;
        }
    }

    /** FASE 1*/
    const tables_fase1 = document.querySelectorAll(".table-fase1");
    const carrousel_fase1 = document.querySelector(".cc-fase1");
    const puntos_fase1 = document.querySelectorAll(".punto-fase1");
    activeCarrousel(carrousel_fase1, puntos_fase1, tables_fase1);

    /** FASE 2*/
    const tables_fase2 = document.querySelectorAll(".table-fase2");
    const carrousel_fase2 = document.querySelector(".cc-fase2");
    const puntos_fase2 = document.querySelectorAll(".punto-fase2");
    activeCarrousel(carrousel_fase2, puntos_fase2, tables_fase2);
   
});


const activeCarrousel = (carrousel, puntos, tables)=>{
    // Adaptación de width del carrousel con todas las tablas
    carrousel.style.width = 100 * tables.length + '%';

    // Adaptación de cada tabla segun el total de las tablas
    tables.forEach((table, index) =>{
        tables[index].style.width = `calc( (100% / ${tables.length}) - 4em)`
    })
    
    //Adecuación de evento para cada punto cambiando el porcentaje de translateX del carrousel
    puntos[0].classList.add('activo')
    puntos.forEach( (punto, position)=>{
        puntos[position].addEventListener("click", ()=>{
            calcWidth = position * (-100/tables.length) // 50 equivale al porcentaje que moveremos de translate X 
            carrousel.style.transform = `translateX(${ calcWidth }%)`;

            puntos.forEach( (punto, position) => {
                puntos[position].classList.remove('activo');
            })

            puntos[position].classList.add('activo');
        })
    })
}