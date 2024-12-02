document.addEventListener("DOMContentLoaded", () => {
    // Animate the underline on load for the "About Me" section
    const aboutUnderline = document.getElementById("about-underline");
    aboutUnderline.classList.add("active");
  
    // Add scroll listener for "My Projects" underline
    const projectsUnderline = document.getElementById("projects-underline");
    window.addEventListener("scroll", () => {
      const projectsSection = document.getElementById("projects");
      const sectionTop = projectsSection.getBoundingClientRect().top;
  
      if (sectionTop < window.innerHeight / 1.5) {
        projectsUnderline.classList.add("active");
      }
    });

    // Add scroll listener for "Contact" underline
    const contactUnderline = document.getElementById("contact-underline");
    window.addEventListener("scroll", () => {
        const contactSection = document.getElementById("contact");
        const sectionTop = contactSection.getBoundingClientRect().top;
    
        if (sectionTop < window.innerHeight / 1.5) {
        contactUnderline.classList.add("active");
        }
    });

  });
  



  
  document.addEventListener("DOMContentLoaded", () => {
    const boxes = document.querySelectorAll(".project-box");
  
    const slideInOnScroll = () => {
      boxes.forEach((box) => {
        const boxTop = box.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
  
        // Check if the box is within the viewport
        if (boxTop < windowHeight * 0.8) {
          box.classList.add("slide-in");
        }
      });
    };
  
    // Run function on scroll
    window.addEventListener("scroll", slideInOnScroll);
  
    // Trigger on load to account for already visible elements
    slideInOnScroll();
  });
