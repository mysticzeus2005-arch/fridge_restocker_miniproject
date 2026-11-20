const searchBox = document.getElementById('search');
const filterButtons = document.querySelectorAll('.filter');
const cards = document.querySelectorAll('.item-card');
const noResults = document.getElementById('noResults');
let filter = 'all';

function updateView(){
  const q = (searchBox?.value || '').toLowerCase().trim();
  let shown = 0;
  cards.forEach(card=>{
    const matchesSearch = card.dataset.name.includes(q);
    const status = card.dataset.stock;
    const matchesFilter = filter === 'all' || (filter === 'low' && (status === 'low' || status === 'out')) || (filter === 'out' && status === 'out');
    const visible = matchesSearch && matchesFilter;
    card.classList.toggle('hidden', !visible);
    if(visible) shown++;
  });
  noResults?.classList.toggle('hidden', shown !== 0 || cards.length === 0);
}
searchBox?.addEventListener('input', updateView);
filterButtons.forEach(btn=>btn.addEventListener('click',()=>{
  filter = btn.dataset.filter;
  filterButtons.forEach(b=>b.classList.toggle('active', b===btn));
  updateView();
}));
