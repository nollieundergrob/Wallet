// script.js

function toggleTheme() {
    const body = document.body;
    const html = document.documentElement;
    const isDark = body.classList.toggle('dark-theme');
  
    if (isDark) {
      html.style.setProperty('--bg-color', '#111827');
      html.style.setProperty('--text-color', '#f9fafb');
      html.style.setProperty('--header-bg', '#1f2937');
      html.style.setProperty('--card-bg', '#1f2937');
      html.style.setProperty('--card-text', '#f3f4f6');
      html.style.setProperty('--link-color', '#60a5fa');
      html.style.setProperty('--code-bg', '#1e293b');
    } else {
      html.style.setProperty('--bg-color', '#f9fafb');
      html.style.setProperty('--text-color', '#111827');
      html.style.setProperty('--header-bg', '#ffffff');
      html.style.setProperty('--card-bg', '#ffffff');
      html.style.setProperty('--card-text', '#1f2937');
      html.style.setProperty('--link-color', '#3b82f6');
      html.style.setProperty('--code-bg', '#f3f4f6');
    }
  
    // Animate theme transition
    html.classList.add('theme-transition');
    setTimeout(() => {
      html.classList.remove('theme-transition');
    }, 500);
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    const html = document.documentElement;
    const body = document.body;
    const allSections = document.querySelectorAll('main > section');
  
    // Fade in & slide-down animation
    allSections.forEach((section, index) => {
      section.style.opacity = '0';
      section.style.transform = 'translateY(-30px)';
      section.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
    });
  
    requestAnimationFrame(() => {
      allSections.forEach((section) => {
        section.style.opacity = '1';
        section.style.transform = 'translateY(0)';
      });
    });
  
    // Set initial theme based on system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      toggleTheme();
    }
  
    // Bind toggle to custom element
    const switcher = document.getElementById('dark-theme');
    if (switcher) {
      switcher.addEventListener('click', toggleTheme);
    }
  });