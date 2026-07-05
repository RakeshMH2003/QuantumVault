// QuantumVault — Interactive JS

document.addEventListener('DOMContentLoaded', () => {
  initCopyButtons();
  initDropzones();
  initFormLoaders();
  initAlertDismiss();
  highlightActiveNav();
  initTiltCards();
  initTypewriter();
  initScrollReveal();
});

/* ── Copy QRC code ────────────────────────────────── */
function initCopyButtons() {
  document.querySelectorAll('.qrc-copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.dataset.code || btn.closest('.qrc-box').querySelector('.qrc-code').textContent.trim();
      navigator.clipboard.writeText(code).then(() => {
        const orig = btn.textContent;
        btn.textContent = '✓ Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
          btn.textContent = orig;
          btn.classList.remove('copied');
        }, 2500);
      });
    });
  });
}

/* ── Drag-and-drop file zone ──────────────────────── */
function initDropzones() {
  document.querySelectorAll('.dropzone').forEach(zone => {
    const input = zone.querySelector('input[type="file"]');
    const label = zone.querySelector('.dz-filename');

    zone.addEventListener('click', () => input.click());

    zone.addEventListener('dragover', e => {
      e.preventDefault();
      zone.classList.add('drag-over');
    });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', e => {
      e.preventDefault();
      zone.classList.remove('drag-over');
      if (e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        updateFilename(label, e.dataTransfer.files[0].name);
      }
    });

    input.addEventListener('change', () => {
      if (input.files.length && label) updateFilename(label, input.files[0].name);
    });
  });
}

function updateFilename(el, name) {
  if (el) {
    el.textContent = '📎 ' + name;
    el.style.color = 'var(--cyan)';
    el.style.fontWeight = '600';
  }
}

/* ── Button loading state ─────────────────────────── */
function initFormLoaders() {
  document.querySelectorAll('form[data-loading]').forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.classList.add('loading');
        btn.disabled = true;
      }
    });
  });
}

/* ── Auto-dismiss flash alerts ────────────────────── */
function initAlertDismiss() {
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .5s, transform .5s';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-6px)';
      setTimeout(() => el.remove(), 500);
    }, 5000);
  });
}

/* ── Highlight active nav link ────────────────────── */
function highlightActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });
}

/* ── Interactive Particle Canvas ──────────────────── */
function initParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width, height;
  const particles = [];
  
  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  for(let i=0; i<40; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 2,
      dx: (Math.random() - 0.5) * 0.5,
      dy: (Math.random() - 0.5) * 0.5,
      alpha: Math.random() * 0.5 + 0.1
    });
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0, 240, 255, ${p.alpha})`;
      ctx.fill();
      
      p.x += p.dx;
      p.y += p.dy;
      
      if(p.x < 0) p.x = width;
      if(p.x > width) p.x = 0;
      if(p.y < 0) p.y = height;
      if(p.y > height) p.y = 0;
    });
    requestAnimationFrame(draw);
  }
  draw();
}

/* ── 3D Tilt Effect on Cards ──────────────────────── */
function initTiltCards() {
  const cards = document.querySelectorAll('.card, .feature-card, .stat-card, .auth-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const rotateX = ((y - centerY) / centerY) * -5;
      const rotateY = ((x - centerX) / centerX) * 5;
      
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
    });
  });
}

/* ── Typewriter Effect ────────────────────────────── */
function initTypewriter() {
  const heroText = document.querySelector('.gradient-text');
  if(heroText && heroText.textContent.includes('Quantum-Resistant')) {
    const text = 'Quantum-Resistant';
    heroText.textContent = '';
    let i = 0;
    function type() {
      if(i < text.length) {
        heroText.textContent += text.charAt(i);
        i++;
        setTimeout(type, 80);
      }
    }
    setTimeout(type, 300);
  }
}

/* ── Custom Interactive Cursor ────────────────────── */
function initCustomCursor() {
  const cursor = document.createElement('div');
  cursor.classList.add('custom-cursor');
  document.body.appendChild(cursor);

  const cursorDot = document.createElement('div');
  cursorDot.classList.add('custom-cursor-dot');
  document.body.appendChild(cursorDot);

  document.addEventListener('mousemove', e => {
    // Smooth trailing for outer ring
    requestAnimationFrame(() => {
      cursor.style.left = e.clientX + 'px';
      cursor.style.top = e.clientY + 'px';
    });
    // Instant for inner dot
    cursorDot.style.left = e.clientX + 'px';
    cursorDot.style.top = e.clientY + 'px';
  });

  // Expand cursor on clickable elements
  const clickables = document.querySelectorAll('a, button, input, textarea, .dropzone, .qrc-copy-btn, .nav-user');
  clickables.forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursor.classList.add('hover');
    });
    el.addEventListener('mouseleave', () => {
      cursor.classList.remove('hover');
    });
  });
}

/* ── Scroll Reveal Intersection Observer ──────────── */
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
      }
    });
  }, { threshold: 0.1 });

  // Apply to all cards and feature cards by default
  document.querySelectorAll('.card, .feature-card, .stat-card, .auth-card').forEach(el => {
    el.classList.add('scroll-reveal');
    observer.observe(el);
  });
}
