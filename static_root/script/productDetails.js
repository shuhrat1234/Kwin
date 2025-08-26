tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: "#EF4444",
        "primary-dark": "#1E293B",
        accent: "#F59E0B",
        muted: "#64748B",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      animation: {
        float: "float 6s ease-in-out infinite",
        glow: "glow 2s ease-in-out infinite alternate",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
    },
  },
};
// Function to switch the main image when a thumbnail is clicked
function goToSlide(productId, slideIndex, event) {
  event.stopPropagation(); // Prevent event bubbling

  try {
    const thumbnails = document.querySelectorAll(
      `.thumbnail-btn[data-product="${productId}"]`
    );

    if (!thumbnails.length) {
      console.warn(`No thumbnails found for product ID: ${productId}`);
      return;
    }

    // Reset all thumbnails
    thumbnails.forEach((thumb) => {
      thumb.classList.remove("border-primary");
      thumb.classList.add("border-gray-300");
    });

    // Highlight the selected thumbnail
    const targetThumb = document.querySelector(
      `.thumbnail-btn[data-product="${productId}"][data-slide="${slideIndex}"]`
    );
    if (!targetThumb) {
      console.warn(`Thumbnail not found for slide index: ${slideIndex}`);
      return;
    }

    targetThumb.classList.remove("border-gray-300");
    targetThumb.classList.add("border-primary");

    // Update the main image
    const mainImage = document.getElementById(`mainImage-${productId}`);
    const thumbImg = targetThumb.querySelector("img");
    if (mainImage && thumbImg) {
      mainImage.src = thumbImg.src;
      mainImage.alt = thumbImg.alt;
    } else {
      console.warn(
        `Main image or thumbnail image not found for product ID: ${productId}`
      );
    }
  } catch (error) {
    console.error("Error in goToSlide:", error);
  }
}

// Attach event listeners to thumbnail buttons
try {
  const thumbnailButtons = document.querySelectorAll(".thumbnail-btn");
  if (!thumbnailButtons.length) {
    console.warn("No thumbnail buttons found in the DOM");
  }
  thumbnailButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      const productId = button.getAttribute("data-product");
      const slideIndex = button.getAttribute("data-slide");
      if (productId && slideIndex) {
        goToSlide(productId, slideIndex, event);
      } else {
        console.warn(
          "Missing data-product or data-slide attribute on thumbnail button"
        );
      }
    });
  });
} catch (error) {
  console.error("Error attaching thumbnail event listeners:", error);
}

// Expose goToSlide to global scope
window.goToSlide = goToSlide;

// Quantity controls
let quantity = 0;
const quantityDisplay = document.getElementById("quantity") || null;
const modalQuantity = document.getElementById("modalQuantity") || null;

function updateQuantityDisplay() {
  if (quantityDisplay) quantityDisplay.textContent = quantity;
  if (modalQuantity) modalQuantity.textContent = quantity;
}

window.increaseQuantity = () => {
console.log("ishladi");

  quantity++;
  updateQuantityDisplay();
};

window.decreaseQuantity = () => {
  if (quantity > 0) {
    quantity--;
    updateQuantityDisplay();
  }
};

// Modal controls
window.openOrderModal = () => {
  const orderModal = document.getElementById("orderModal");
  if (orderModal) {
    orderModal.classList.remove("hidden");
  } else {
    console.warn("Order modal not found");
  }
};

window.closeOrderModal = () => {
  const orderModal = document.getElementById("orderModal");
  if (orderModal) {
    orderModal.classList.add("hidden");
  } else {
    console.warn("Order modal not found");
  }
};
