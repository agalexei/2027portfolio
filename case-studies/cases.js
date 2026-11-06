const cards = document.querySelectorAll('.case-card');

for (const card of cards) {
  card.addEventListener('click', (event) => {
    if (event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    document.querySelector('.case-card.is-opening')?.classList.remove('is-opening');
    card.classList.add('is-opening');
  });
}

window.addEventListener('pageshow', () => {
  document.querySelector('.case-card.is-opening')?.classList.remove('is-opening');
});
