(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (mainEl, el, all = false) => {
    el = el.trim()
    if (all) {
      return [...mainEl.querySelectorAll(el)]
    } else {
      return mainEl.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(document, el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  const getServiceBoxEl = (e) => {
    let mainBox = e.target.parentElement.parentElement.parentElement;
    if (mainBox) {
      let serviceName = select(mainBox, '.service-name'),
      serviceId = select(mainBox, 'input[name="service_id"]'),
      serviceDuration = select(mainBox, '.service-duration'),
      servicePrice = select(mainBox, '.service-price'),
      serviceDurationUnit = select(mainBox, '.service-duration-unit'),
      serviceSlot = select(mainBox, '.service-slot');
      return { serviceName, serviceId, serviceDuration, servicePrice, serviceDurationUnit, serviceSlot }
    }
    return {}
  }

  const getRegisterServicePackEl = () => {
    let registerModal = select(document, '#register-service-pack');
    if (registerModal) {
      let serviceName = select(registerModal, '.service-name'),
      serviceId = select(registerModal, 'input[name="service_id"]'),
      serviceSlot = select(registerModal, '.description-slot'),
      serviceDuration = select(registerModal, '.description-duration'),
      serviceTotal = select(registerModal, '.service-total');
      return { registerModal, serviceName, serviceId, serviceSlot, serviceDuration, serviceTotal }
      }
    return {}
  }

  /**
   * Easy open modal register service
   */
  on('click', '.btn-register-now', function (e) {
    let serviceBoxEl = getServiceBoxEl(e),
    registerServicePackEl = getRegisterServicePackEl(),
    duration = 0,
    slot = 0;
    if (serviceBoxEl && registerServicePackEl) {
      if (registerServicePackEl.serviceName && serviceBoxEl.serviceName) {
        registerServicePackEl.serviceName.textContent = serviceBoxEl.serviceName.textContent;
      }
      if (registerServicePackEl.serviceId && serviceBoxEl.serviceId) {
        registerServicePackEl.serviceId.value = serviceBoxEl.serviceId.value;
      }
      if (registerServicePackEl.serviceDuration && serviceBoxEl.serviceDuration) {
        duration = parseInt(serviceBoxEl.serviceDuration.textContent);
        registerServicePackEl.serviceDuration.textContent = serviceBoxEl.serviceDuration.textContent;
      } else {
        if (registerServicePackEl.serviceDuration && !serviceBoxEl.serviceDuration) {
          duration = 1;
          registerServicePackEl.serviceDuration.textContent = 1;
        }
      }
      if (registerServicePackEl.serviceSlot && serviceBoxEl.serviceSlot) {
        slot = parseInt(serviceBoxEl.serviceSlot.textContent);
        registerServicePackEl.serviceSlot.textContent = serviceBoxEl.serviceSlot.textContent;
      } else {
        if (registerServicePackEl.serviceSlot && !serviceBoxEl.serviceSlot) {
          slot = 1;
          registerServicePackEl.serviceSlot.textContent = 1;
        }
      }
      if (registerServicePackEl.serviceTotal) {
        registerServicePackEl.serviceTotal.textContent = serviceBoxEl.servicePrice.textContent;
      }
      const registerServicePackModal = new bootstrap.Modal(registerServicePackEl.registerModal);
      registerServicePackModal.show();
    }
  }, true);

  on('click', '.face-box', function(e) {
    let imageIdEl = e.target;
    if (!imageIdEl.hasAttribute('id')) { imageIdEl = e.target.parentElement }
    const imageId = imageIdEl.getAttribute('id');
    const uploadImageEl = select(document, '#upload-face-modal');
    const uploadBtnEl = select(uploadImageEl, '.btn-upload-image');
    uploadBtnEl.setAttribute('id', imageId);
    const uploadImageModal = new bootstrap.Modal(uploadImageEl);
    uploadImageModal.show();
  }, true)

  const generateElement = (name, attributes) => {
    const el = document.createElement(name);
    for (const attribute of attributes) {
      for (const key in attribute) {
        el.setAttribute(key, attribute[key]);
      }
    }
    return el;
  }

  on('click', '#register-service-pack .clear-face-box', function(e) {
    console.log(e);
  })

  on('click', '.btn-upload-image', function(e) {
    const btnID = e.target.getAttribute('id');
    const uploadContent = e.target.parentElement.parentElement;
    const uploadFaceFormEl = select(uploadContent, '.upload-face-form');
    const inputUploadImageEl = select(uploadContent, 'input[name="face_image_single"]');
    const inputUploadImageNameEl = select(uploadContent, 'input[name="face_image_name_single"]');
    const inputUploadImageName = inputUploadImageNameEl.value;
    const [inputUploadImage] = inputUploadImageEl.files;
    const suffixImage = inputUploadImage.type.replace('image/', '');
    if (inputUploadImage && inputUploadImageName) {
        const imageBoxFaceEl = select(document, `#register-service-pack #${btnID}`);
        const addLineEl = select(imageBoxFaceEl, '.ri-image-add-line');
        let inputFileFaceEl = generateElement('input', [{'name': 'face_image[]', 'type': 'file', 'class': 'd-none'}]);
        const tempFile = new File([inputUploadImage], `${inputUploadImageName}.${suffixImage}`, {
            type: inputUploadImage.type,
            lastModified: new Date(),
        }, 'utf-8');
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(tempFile);
        inputFileFaceEl.files = dataTransfer.files;
        let imageFaceEl = generateElement('input', [{'type': 'image', 'width': 130, 'height': 150, 'src': URL.createObjectURL(inputUploadImage), 'alt': 'Image Face', 'class': 'rounded-3'}]);
        let closeEl = generateElement('i', [{'class': 'clear-face-box ri-close-circle-fill position-absolute top-0 start-100 translate-middle pe-auto fs-4', 'style': 'color: #ef6603'}]);
        imageBoxFaceEl.removeChild(addLineEl);
        imageBoxFaceEl.appendChild(inputFileFaceEl);
        imageBoxFaceEl.appendChild(imageFaceEl);
        imageBoxFaceEl.appendChild(closeEl);
        imageBoxFaceEl.classList.add('disabled');

        const uploadImageEl = select(document, '#upload-face-modal');
        const uploadImageModal = bootstrap.Modal.getInstance(uploadImageEl);
        uploadFaceFormEl.reset();
        uploadImageModal.hide();
    }
  })

  on('input', '#register-service-pack input[name="service_quantity"]', function (e) {
    let qtyEl = select(document, '#register-service-pack input[name="service_quantity"]'),
        descriptionSlot = select(document, '.description-slot'),
        descriptionDuration = select(document, '.description-duration'),
        totalEl = select(document, '#register-service-pack .service-total'),
        total = 0;
    if (qtyEl && descriptionSlot ) {
      descriptionSlot.textContent = parseInt(descriptionSlot.textContent) * parseInt(qtyEl.value);
    }
    if (qtyEl && descriptionDuration) {
      descriptionDuration.textContent = parseInt(descriptionDuration.textContent) * parseInt(qtyEl.value);
    }
    totalEl.textContent = new Intl.NumberFormat().format(total);
  })

  /**
   * Easy on scroll event listener
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener);
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select(document, '#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200;
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(document, navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select(document, '#header')
    let offset = header.offsetHeight

    let elementPos = select(document, el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select(document, '#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select(document, '.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select(document, '#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select(document, '#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(document, this.hash)) {
      e.preventDefault()

      let navbar = select(document, '#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select(document, '.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(document, window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });
})()
