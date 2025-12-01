document.addEventListener('DOMContentLoaded', () => {
    console.log('%c Django Blog Loaded Successfully!',
        'color: #4b7bec; font-size: 16px; font-weight: bold;');

    // Smooth fade-in animation for content
    const content = document.querySelector('.content');
    content.style.opacity = 0;
    setTimeout(() => {
        content.style.transition = "opacity 0.6s ease-in";
        content.style.opacity = 1;
    }, 150);
});
