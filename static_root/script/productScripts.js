tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#EF4444',
                'primary-dark': '#1E293B',
                accent: '#F59E0B',
                muted: '#64748B'
            },
            fontFamily: {
                'sans': ['Inter', 'system-ui', 'sans-serif']
            }
        }
    }
};

let searchTerm = '';
let selectedBrands = [];
let wishlist = [];
let currentProductId = null;

const searchInput = document.getElementById('searchInput');
const productsGrid = document.getElementById('productsGrid');
const productCount = document.getElementById('productCount');
const appliedFilters = document.getElementById('appliedFilters');
const filterTags = document.getElementById('filterTags');
const noResults = document.getElementById('noResults');
const clearAllFilters = document.getElementById('clearAllFilters');
const resetFiltersBtn = document.getElementById('resetFiltersBtn');
const filterButton = document.getElementById('filterButton');
const filterModalOverlay = document.getElementById('filterModalOverlay');
const filterModal = document.getElementById('filterModal');
const closeFilterModal = document.getElementById('closeFilterModal');
const applyMobileFilters = document.getElementById('applyMobileFilters');
const clearMobileFilters = document.getElementById('clearMobileFilters');
const activeFiltersCount = document.getElementById('activeFiltersCount');
const orderModal = document.getElementById('orderModal');
const orderForm = document.getElementById('orderForm');
const modalProductName = document.getElementById('modalProductName');
const modalPrice = document.getElementById('modalPrice');
const modalQuantity = document.getElementById('modalQuantity');

function goToSlide(event, productId, slideIndex) {
    event.stopPropagation();
    const slides = document.querySelectorAll(`[data-product="${productId}"][data-slide]`);
    const indicators = document.querySelector(`[data-product="${productId}"][data-slide="${slideIndex}"]`).parentElement.querySelectorAll('.indicator');
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    slides[slideIndex].classList.add('active');
    indicators[slideIndex].classList.add('active');
}

function autoSlideProducts() {
    [1, 2, 3, 4, 5, 6].forEach(productId => {
        const slides = document.querySelectorAll(`[data-product="${productId}"][data-slide]`);
        const indicators = document.querySelectorAll(`[data-product="${productId}"]`).length > 0 ?
            document.querySelector(`[data-product="${productId}"]`).parentElement.querySelectorAll('.indicator') : [];
        if (slides.length > 0) {
            const currentActive = Array.from(slides).findIndex(slide => slide.classList.contains('active'));
            const nextSlide = (currentActive + 1) % slides.length;
            slides.forEach(slide => slide.classList.remove('active'));
            indicators.forEach(indicator => indicator.classList.remove('active'));
            slides[nextSlide].classList.add('active');
            if (indicators[nextSlide]) indicators[nextSlide].classList.add('active');
        }
    });
}

setInterval(autoSlideProducts, 3000);

function filterProducts() {
    const productCards = document.querySelectorAll('.product-card');
    let visibleCount = 0;
    productCards.forEach(card => {
        const name = card.dataset.name.toLowerCase();
        const brand = card.dataset.brand;
        const matchesSearch = name.includes(searchTerm.toLowerCase()) ||
            brand.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesBrand = selectedBrands.length === 0 || selectedBrands.includes(brand);
        if (matchesSearch && matchesBrand) {
            card.classList.remove('hidden');
            visibleCount++;
        } else {
            card.classList.add('hidden');
        }
    });
    return visibleCount;
}

function renderProducts() {
    const visibleCount = filterProducts();
    productCount.textContent = `Найдено товаров: ${visibleCount}`;
    noResults.classList.toggle('hidden', visibleCount > 0);
    appliedFilters.classList.toggle('hidden', !searchTerm && selectedBrands.length === 0);
    activeFiltersCount.classList.toggle('hidden', !searchTerm && selectedBrands.length === 0);
    activeFiltersCount.textContent = (searchTerm ? 1 : 0) + selectedBrands.length;
}

function createFilterTag(text, onRemove) {
    const tag = document.createElement('span');
    tag.className = 'inline-flex items-center bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded-full font-medium';
    tag.innerHTML = `
                ${text}
                <button class="ml-1 focus:outline-none">
                    <svg class="w-3 h-3 text-gray-500 hover:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            `;
    tag.querySelector('button').addEventListener('click', () => {
        onRemove();
        renderProducts();
    });
    return tag;
}

function updateAppliedFilters() {
    filterTags.innerHTML = '';
    if (searchTerm) {
        filterTags.appendChild(createFilterTag(searchTerm, () => {
            searchTerm = '';
            searchInput.value = '';
            updateAppliedFilters();
        }));
    }
    selectedBrands.forEach(brand => {
        filterTags.appendChild(createFilterTag(brand, () => {
            selectedBrands = selectedBrands.filter(b => b !== brand);
            updateBrandCheckboxes();
            updateAppliedFilters();
        }));
    });
    renderProducts();
}

function updateBrandCheckboxes() {
    document.querySelectorAll('.filter-checkbox, .mobile-filter-checkbox').forEach(checkbox => {
        const isChecked = selectedBrands.includes(checkbox.dataset.brand);
        checkbox.checked = isChecked;
        const label = checkbox.nextElementSibling;
        const icon = label.querySelector('svg');
        if (isChecked) {
            label.classList.add('bg-primary', 'border-primary');
            label.classList.remove('border-gray-300');
            icon.classList.remove('hidden');
        } else {
            label.classList.remove('bg-primary', 'border-primary');
            label.classList.add('border-gray-300');
            icon.classList.add('hidden');
        }
    });
}

function toggleWishlist(productId) {
    if (wishlist.includes(productId)) {
        wishlist = wishlist.filter(id => id !== productId);
        document.querySelector(`[data-product-id="${productId}"] .heart-icon`).classList.remove('active');
    } else {
        wishlist.push(productId);
        document.querySelector(`[data-product-id="${productId}"] .heart-icon`).classList.add('active');
    }
}

function openOrderModal(productId) {
    currentProductId = productId;
    const card = document.querySelector(`[data-product-id="${productId}"]`);
    const name = card.dataset.name;
    const price = card.querySelector('.text-primary').textContent;
    modalProductName.textContent = name;
    modalPrice.textContent = price;
    modalQuantity.textContent = '1';
    orderModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    orderForm.reset();
}

function closeOrderModal() {
    orderModal.classList.add('hidden');
    document.body.style.overflow = '';
    currentProductId = null;
}

function clearAllFiltersFunc() {
    searchTerm = '';
    selectedBrands = [];
    searchInput.value = '';
    updateBrandCheckboxes();
    updateAppliedFilters();
    renderProducts();
}

function openFilterModal() {
    filterModalOverlay.classList.add('active');
    filterModal.classList.add('active');
    document.body.style.overflow = 'hidden';
    document.querySelectorAll('.mobile-filter-checkbox').forEach(checkbox => {
        const isChecked = selectedBrands.includes(checkbox.dataset.brand);
        checkbox.checked = isChecked;
        const label = checkbox.nextElementSibling;
        const icon = label.querySelector('svg');
        if (isChecked) {
            label.classList.add('bg-primary', 'border-primary');
            label.classList.remove('border-gray-300');
            icon.classList.remove('hidden');
        } else {
            label.classList.remove('bg-primary', 'border-primary');
            label.classList.add('border-gray-300');
            icon.classList.add('hidden');
        }
    });
}

function closeFilterModalFunc() {
    filterModalOverlay.classList.remove('active');
    filterModal.classList.remove('active');
    document.body.style.overflow = '';
}

function applyFiltersFromModal() {
    const tempSelectedBrands = [];
    document.querySelectorAll('.mobile-filter-checkbox:checked').forEach(checkbox => {
        tempSelectedBrands.push(checkbox.dataset.brand);
    });
    selectedBrands = tempSelectedBrands;
    updateBrandCheckboxes();
    updateAppliedFilters();
    renderProducts();
    closeFilterModalFunc();
}

function clearMobileFiltersFunc() {
    document.querySelectorAll('.mobile-filter-checkbox').forEach(checkbox => {
        checkbox.checked = false;
        const label = checkbox.nextElementSibling;
        const icon = label.querySelector('svg');
        label.classList.remove('bg-primary', 'border-primary');
        label.classList.add('border-gray-300');
        icon.classList.add('hidden');
    });
}

searchInput.addEventListener('input', (e) => {
    searchTerm = e.target.value;
    updateAppliedFilters();
    renderProducts();
});

document.addEventListener('change', (e) => {
    if (e.target.classList.contains('filter-checkbox')) {
        const brand = e.target.dataset.brand;
        if (e.target.checked) {
            selectedBrands.push(brand);
        } else {
            selectedBrands = selectedBrands.filter(b => b !== brand);
        }
        updateBrandCheckboxes();
        updateAppliedFilters();
        renderProducts();
    }
});

filterButton.addEventListener('click', openFilterModal);
closeFilterModal.addEventListener('click', closeFilterModalFunc);
filterModalOverlay.addEventListener('click', (e) => {
    if (e.target === filterModalOverlay) closeFilterModalFunc();
});
applyMobileFilters.addEventListener('click', applyFiltersFromModal);
clearMobileFilters.addEventListener('click', clearMobileFiltersFunc);
clearAllFilters.addEventListener('click', clearAllFiltersFunc);
resetFiltersBtn.addEventListener('click', clearAllFiltersFunc);

orderForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const fullName = orderForm.fullName.value;
    const phone = orderForm.contactPhone.value;
    const email = orderForm.email.value;
    const additionalInfo = orderForm.additionalInfo.value;
    const productName = modalProductName.textContent;
    const price = modalPrice.textContent;
    const quantity = modalQuantity.textContent;

    if (!phone.match(/\+998[0-9]{9}/)) {
        alert('Пожалуйста, введите номер телефона в формате +998XXXXXXXXX');
        return;
    }

    alert(`Заказ оформлен!\nТовар: ${productName}\nКоличество: ${quantity}\nЦена: ${price}\nИмя: ${fullName}\nТелефон: ${phone}\nEmail: ${email}\nДополнительно: ${additionalInfo || 'Нет'}`);
    closeOrderModal();
});

updateBrandCheckboxes();
renderProducts();




let basket = {};

function toggleBasket(productId) {
    const card = document.querySelector(`.product-card[data-product-id="${productId}"]`);
    const basketBtn = card.querySelector('.basket-btn');
    const basketCounter = card.querySelector('.basket-counter');

    if (!basket[productId]) {
        basket[productId] = 1;
        basketBtn.classList.add('hidden');
        basketCounter.classList.remove('hidden');
        updateBasketCount(productId);
    } else {
        delete basket[productId];
        basketBtn.classList.remove('hidden');
        basketCounter.classList.add('hidden');
    }
}

function updateBasket(productId, change) {
    if (!basket[productId]) basket[productId] = 0;
    basket[productId] = Math.max(0, basket[productId] + change);

    const card = document.querySelector(`.product-card[data-product-id="${productId}"]`);
    const basketBtn = card.querySelector('.basket-btn');
    const basketCounter = card.querySelector('.basket-counter');

    if (basket[productId] === 0) {
        delete basket[productId];
        basketBtn.classList.remove('hidden');
        basketCounter.classList.add('hidden');
    } else {
        basketBtn.classList.add('hidden');
        basketCounter.classList.remove('hidden');
        updateBasketCount(productId);
    }
}

function updateBasketCount(productId) {
    const card = document.querySelector(`.product-card[data-product-id="${productId}"]`);
    const countElement = card.querySelector('.basket-count');
    countElement.textContent = basket[productId];
}