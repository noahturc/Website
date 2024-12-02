/*  This works fine but it doesn't make the arrows disappear if on first or last slide.

let slideIndex = 0;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    let slides = document.getElementsByClassName("slide");
    if (slides.length === 0) return;

    if (n >= slides.length) { slideIndex = 0; }
    if (n < 0) { slideIndex = slides.length - 1; }

    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove('active');
    }

    slides[slideIndex].classList.add('active');
}


*/



let slideIndex = 0;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex + n);
}

function showSlides(n) {
    let slides = document.getElementsByClassName("slide");
    let prev = document.querySelector('.prev');
    let next = document.querySelector('.next');

    if (slides.length === 0) return;

    // Enforce bounds without looping
    if (n >= slides.length) {
        slideIndex = slides.length - 1;
    } else if (n <= 0) {
        slideIndex = 0;
    } else {
        slideIndex = n;
    }

    // Hide or show arrows based on the current slide
    if (slideIndex === 0) {
        prev.style.display = 'none';
    } else {
        prev.style.display = 'block';
    }

    if (slideIndex === slides.length - 1) {
        next.style.display = 'none';
    } else {
        next.style.display = 'block';
    }

    // Hide all slides
    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove('active');
    }

    // Show the current slide
    slides[slideIndex].classList.add('active');
}



// you can now use right and left arrow keys to navigate slides
document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
        event.preventDefault(); // Prevent default action
        plusSlides(-1);
    } else if (event.key === 'ArrowRight') {
        event.preventDefault(); // Prevent default action
        plusSlides(1);
    }
});


