// === GLOBAL CART HANDLER ===
let cart = [];

// Load cart from localStorage once when page starts
function loadCart() {
  const stored = localStorage.getItem('cart');
  cart = stored ? JSON.parse(stored) : [];
}
loadCart();
window.addEventListener('storage', loadCart);

// Add to cart (with toast)
// function addToCart(name, price) {
//   if (!Array.isArray(cart)) cart = [];
//   const existing = cart.find(item => item.name === name);
//   if (existing) {
//     existing.quantity++;
//   } else {
//     cart.push({ name, price, quantity: 1 });
//   }
//   localStorage.setItem('cart', JSON.stringify(cart));
//   showToast(`${name} added to cart!`);
// }

function addToCart(id, name, price) {
  console.log("Adding:", id, name, price);
  if (!Array.isArray(cart)) cart = [];

  const existing = cart.find(item => item.id === id);
  if (existing) {
    existing.quantity++;
  } else {
    cart.push({ id: id, name: name, price: price, quantity: 1 });
  }

  console.log("Cart after add:", cart);
  localStorage.setItem('cart', JSON.stringify(cart));
  showToast(`${name} added to cart!`);
  updateCartCount();
}

// === DISPLAY CART ITEMS ===
function displayCart() {
  const container = document.getElementById('cart-items');
  if (!container) return;

  const stored = localStorage.getItem('cart');
  if (!stored) {
    document.getElementById('subtotal').textContent = '$0.00';
    document.getElementById('total').textContent = '$0.00';
    return;
  }

  cart = JSON.parse(stored);
  container.innerHTML = '';
  let subtotal = 0;

  cart.forEach((item, index) => {
    const price = parseFloat(item.price); // ✅ ensure number
    subtotal += price * item.quantity;
    container.innerHTML += `
      <div class="cart-item">
        <span>${item.name} ($${price.toFixed(2)}) × ${item.quantity}</span>
        <button onclick="removeFromCart(${index})">Remove</button>
      </div>`;
  });

  const delivery = subtotal > 0 ? 2.0 : 0.0;
  const total = subtotal + delivery;

  document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
  document.getElementById('delivery').textContent = `$${delivery.toFixed(2)}`;
  document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}


// === ESTIMATED DELIVERY TIME ===
function showDeliveryTime() {
  const eta = document.getElementById('eta');
  if (!eta) return;
  const min = 20 + Math.floor(Math.random() * 15); // random 20–35 min
  eta.textContent = `${min} min`;
}
showDeliveryTime();


function removeFromCart(index) {
  cart.splice(index, 1);
  localStorage.setItem('cart', JSON.stringify(cart));
  displayCart();
  updateCartCount(); // ✅ refresh navbar count
}

document.getElementById('checkout-btn')?.addEventListener('click', () => {
  const payment = document.querySelector('input[name="payment"]:checked')?.value || 'Cash';
  const eta = document.getElementById('eta')?.textContent || '30 min';
  localStorage.setItem('eta', eta);

  if (cart.length === 0) return alert('Your cart is empty!');
  alert(`Order placed successfully! Payment: ${payment}`);

  // clear cart + redirect
  localStorage.removeItem('cart');
  window.location.href = '/thankyou';
});

// === NAVBAR TOGGLE ===
function toggleNav() {
  const nav = document.getElementById('navbar');
  nav.classList.toggle('active');
}

// === SEARCH & FILTER ===
function applyFilter() {
  const search = document.getElementById('searchInput').value.toLowerCase();
  const category = document.getElementById('categoryFilter').value;
  const cards = document.querySelectorAll('.food-card');

  cards.forEach(card => {
    const name = card.dataset.name.toLowerCase();
    const cat = card.dataset.category;
    const matchSearch = name.includes(search);
    const matchCategory = category === "All" || cat === category;
    card.style.display = (matchSearch && matchCategory) ? "block" : "none";
  });
}

// === TOAST NOTIFICATION ===
function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2000);
}


// === LAYOUT SWITCHER WITH ANIMATION ===
function setLayout(type) {
  const container = document.getElementById('menuContainer');
  const cards = container.querySelectorAll('.food-card');

  // Fade-out animation
  cards.forEach(c => c.classList.add('fade-out'));

  setTimeout(() => {
    // Reset existing layout classes
    container.classList.remove('grid4', 'grid6');
    cards.forEach(c => c.classList.remove('list-view'));

    // Apply new layout
    if (type === 'grid4') {
      container.classList.add('grid4');
    } else if (type === 'grid6') {
      container.classList.add('grid6');
    } else if (type === 'list') {
      container.style.display = 'flex';
      container.style.flexDirection = 'column';
      cards.forEach(c => c.classList.add('list-view'));
    }

    if (type !== 'list') {
      container.style.display = 'grid';
      container.style.flexDirection = '';
    }

    // Fade-in animation
    setTimeout(() => {
      cards.forEach(c => c.classList.remove('fade-out'));
      cards.forEach(c => c.classList.add('fade-in'));
      setTimeout(() => cards.forEach(c => c.classList.remove('fade-in')), 400);
    }, 100);
  }, 200);
}

function sortMenu() {
  const sortType = document.getElementById('sortFilter').value;
  const container = document.getElementById('menuContainer');
  const cards = Array.from(container.querySelectorAll('.food-card'));

  cards.sort((a, b) => {
    const priceA = parseFloat(a.querySelector('p').innerText.replace('$',''));
    const priceB = parseFloat(b.querySelector('p').innerText.replace('$',''));
    const nameA = a.dataset.name.toLowerCase();
    const nameB = b.dataset.name.toLowerCase();

    if (sortType === 'price-low') return priceA - priceB;
    if (sortType === 'price-high') return priceB - priceA;
    if (sortType === 'name') return nameA.localeCompare(nameB);
    return 0;
  });

  container.innerHTML = '';
  cards.forEach(c => container.appendChild(c));
}

// === DARK MODE TOGGLE ===
function toggleTheme() {
  const body = document.body;
  const btn = document.getElementById('themeButton');
  body.classList.toggle('dark');
  
  // Save preference
  const mode = body.classList.contains('dark') ? 'dark' : 'light';
  localStorage.setItem('theme', mode);
  
  // Change icon
  btn.textContent = body.classList.contains('dark') ? '☀️' : '🌙';
}

// Apply saved theme on load
window.addEventListener('load', () => {
  const savedTheme = localStorage.getItem('theme');
  const body = document.body;
  const btn = document.getElementById('themeButton');
  if (savedTheme === 'dark') {
    body.classList.add('dark');
    if (btn) btn.textContent = '☀️';
  }
});

// === CART COUNT BADGE ===
function updateCartCount() {
  const badge = document.getElementById('cartCount') || document.getElementById('cart-count');
  if (!badge) return;
  const stored = localStorage.getItem('cart');
  const items = stored ? JSON.parse(stored) : [];
  const count = items.reduce((sum, i) => sum + i.quantity, 0);
  badge.textContent = count;
}

updateCartCount();
window.addEventListener('storage', updateCartCount);