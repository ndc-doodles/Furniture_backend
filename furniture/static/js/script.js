document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.getElementById('navbar');
  const brand = document.getElementById('brand');
  const navLinks = document.getElementById('navLinks');
  const menuBtn = document.getElementById('menuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  const closeBtn = document.getElementById('closeBtn');

  // Scroll navbar color change
  if (navbar) {
    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY > 10;
      navbar.classList.toggle('backdrop-blur', scrolled);
      navbar.classList.toggle('bg-white/70', scrolled);
      navbar.classList.toggle('shadow-md', scrolled);

      if (brand) brand.classList.toggle('text-black', scrolled);
      if (brand) brand.classList.toggle('text-white', !scrolled);

      if (navLinks) navLinks.classList.toggle('text-black', scrolled);
      if (navLinks) navLinks.classList.toggle('text-white', !scrolled);

      if (menuBtn) menuBtn.classList.toggle('text-black', scrolled);
      if (menuBtn) menuBtn.classList.toggle('text-white', !scrolled);
    });
  }

  // Toggle mobile menu
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      mobileMenu.classList.toggle('hidden');
    });
  }

  // Close via close button
  if (closeBtn && mobileMenu) {
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      mobileMenu.classList.add('hidden');
    });
  }

  // Close on outside click
  if (mobileMenu && menuBtn) {
    document.addEventListener('click', (e) => {
      if (!mobileMenu.contains(e.target) && !menuBtn.contains(e.target)) {
        mobileMenu.classList.add('hidden');
      }
    });
  }
});










 document.addEventListener("DOMContentLoaded", function () {
  const thumbnailContainer = document.getElementById("thumbnailContainer");
  const scrollLeft = document.getElementById("scrollLeft");
  const scrollRight = document.getElementById("scrollRight");
  const thumbnails = document.querySelectorAll(".thumbnail");
  const mainImage = document.getElementById("mainImage");

  const imageModal = document.getElementById("imageModal");
  const modalImage = document.getElementById("modalImage");
  const closeModal = document.getElementById("closeModal");
  const modalPrev = document.getElementById("modalPrev");
  const modalNext = document.getElementById("modalNext");

  let currentIndex = 0;

  if (scrollLeft && scrollRight && thumbnailContainer) {
    scrollLeft.addEventListener("click", () => {
      thumbnailContainer.scrollBy({ left: -150, behavior: "smooth" });
    });

    scrollRight.addEventListener("click", () => {
      thumbnailContainer.scrollBy({ left: 150, behavior: "smooth" });
    });
  }

  if (thumbnails && mainImage) {
    thumbnails.forEach((thumb, index) => {
      thumb.addEventListener("click", () => {
        mainImage.src = thumb.src;
        currentIndex = index;
      });
    });

    mainImage.addEventListener("click", () => {
      if (modalImage && imageModal) {
        modalImage.src = mainImage.src;
        imageModal.classList.remove("hidden");
        imageModal.classList.add("flex");

        thumbnails.forEach((thumb, index) => {
          if (thumb.src === mainImage.src) {
            currentIndex = index;
          }
        });
      }
    });
  }

  if (closeModal && imageModal) {
    closeModal.addEventListener("click", () => {
      imageModal.classList.add("hidden");
      imageModal.classList.remove("flex");
    });

    imageModal.addEventListener("click", (e) => {
      if (e.target === imageModal) {
        imageModal.classList.add("hidden");
        imageModal.classList.remove("flex");
      }
    });
  }

  if (modalPrev && modalNext && modalImage && thumbnails.length > 0) {
    modalPrev.addEventListener("click", () => {
      currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
      modalImage.src = thumbnails[currentIndex].src;
    });

    modalNext.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % thumbnails.length;
      modalImage.src = thumbnails[currentIndex].src;
    });
  }
});









// function openEnquiryModal(name, material, price, color, quantity) {
//   document.getElementById('productName').value = name;
//   document.getElementById('productMaterial').value = material;
//   document.getElementById('productPrice').value = price;
//   document.getElementById('productColor').value = color;
//   document.getElementById('productQuantity').value = quantity || 1;
//   document.getElementById('enquiryModal').classList.remove('hidden');
// }

// function closeEnquiryModal() {
//   document.getElementById('enquiryModal').classList.add('hidden');
// }









   const container = document.getElementById('cardContainer');
  const scrollLeftBtn = document.getElementById('scrollLeft');
  const scrollRightBtn = document.getElementById('scrollRight');

  scrollLeftBtn.addEventListener('click', () => {
    container.scrollBy({ left: -container.clientWidth, behavior: 'smooth' });
  });

  scrollRightBtn.addEventListener('click', () => {
    container.scrollBy({ left: container.clientWidth, behavior: 'smooth' });
  });

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.product-image').forEach(img => {
    const originalSrc = img.getAttribute('src');
    const hoverSrc = img.getAttribute('data-hover');

    img.addEventListener('mouseenter', () => {
      img.style.transition = 'opacity 0.3s ease'; // smooth fade
      img.style.opacity = '0';
      setTimeout(() => {
        img.setAttribute('src', hoverSrc);
        img.style.opacity = '1';
      }, 150);
    });

    img.addEventListener('mouseleave', () => {
      img.style.opacity = '0';
      setTimeout(() => {
        img.setAttribute('src', originalSrc);
        img.style.opacity = '1';
      }, 150);
    });
  });
});







// function openShareModal(event) {
//     event.preventDefault(); // prevent link click
//     event.stopPropagation(); // stop event bubbling
//     document.getElementById('shareModal').classList.remove('hidden');
//   }

//   function closeShareModal() {
//     document.getElementById('shareModal').classList.add('hidden');
//   }

//   // Optional: Close modal when clicking outside
//   window.addEventListener('click', function (e) {
//     const modal = document.getElementById('shareModal');
//     if (e.target === modal) {
//       modal.classList.add('hidden');
//     }
//   });





 
document.addEventListener('DOMContentLoaded', () => {
  // Paths to images (relative to the HTML file, NOT the JS file)
  const images = [
    './static/images/headerbg2.png',
    './static/images/about1.jpg',
    './static/images/about2.jpg'
  ];

  const bg1 = document.getElementById('bg1');
  const bg2 = document.getElementById('bg2');

  if (!bg1 || !bg2) {
    console.error('Background elements not found. Make sure #bg1 and #bg2 exist in HTML.');
    return;
  }

  // Preload all images before starting slideshow
  const preload = (src) => new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve();
    img.onerror = () => resolve(); // even if it fails, skip
    img.src = src;
  });

  Promise.all(images.map(preload)).then(() => {
    let index = 0;
    let showingBg1 = true;

    // Initialize first background
    bg1.style.backgroundImage = `url('${images[0]}')`;
    bg1.style.opacity = '1';
    bg2.style.opacity = '0';

    setInterval(() => {
      index = (index + 1) % images.length;

      if (showingBg1) {
        bg2.style.backgroundImage = `url('${images[index]}')`;
        bg2.style.opacity = '1';
        bg1.style.opacity = '0';
      } else {
        bg1.style.backgroundImage = `url('${images[index]}')`;
        bg1.style.opacity = '1';
        bg2.style.opacity = '0';
      }

      showingBg1 = !showingBg1;
    }, 4000); // 4 seconds between changes
  });
});




