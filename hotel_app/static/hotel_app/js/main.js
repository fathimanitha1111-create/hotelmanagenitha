/**
 * The Grand Azure - Hotel & Resort Interactive Scripts
 */

document.addEventListener('DOMContentLoaded', function () {
  // Initialize Bootstrap Tooltips & Popovers
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Set minimum date for all check-in date inputs to today
  const today = new Date().toISOString().split('T')[0];
  const checkInInputs = document.querySelectorAll('input[type="date"][name="check_in"], #search_check_in, #booking_check_in, #calc_check_in');
  const checkOutInputs = document.querySelectorAll('input[type="date"][name="check_out"], #search_check_out, #booking_check_out, #calc_check_out');

  checkInInputs.forEach(input => {
    input.min = today;
    if (!input.value) {
      input.value = today;
    }
    input.addEventListener('change', function () {
      updateCheckOutMin(input);
      recalculateLivePricing();
    });
  });

  function updateCheckOutMin(checkInInput) {
    if (!checkInInput.value) return;
    const nextDay = new Date(checkInInput.value);
    nextDay.setDate(nextDay.getDate() + 1);
    const minCheckOutStr = nextDay.toISOString().split('T')[0];

    checkOutInputs.forEach(outInput => {
      outInput.min = minCheckOutStr;
      if (!outInput.value || outInput.value <= checkInInput.value) {
        outInput.value = minCheckOutStr;
      }
    });
  }

  // Trigger once on load
  if (checkInInputs.length > 0 && checkInInputs[0].value) {
    updateCheckOutMin(checkInInputs[0]);
  }

  checkOutInputs.forEach(input => {
    input.addEventListener('change', function () {
      recalculateLivePricing();
    });
  });

  // Live Price Calculation in Room Detail & Booking Pages
  function recalculateLivePricing() {
    const checkInEl = document.querySelector('#booking_check_in') || document.querySelector('#calc_check_in');
    const checkOutEl = document.querySelector('#booking_check_out') || document.querySelector('#calc_check_out');
    const pricePerNightEl = document.querySelector('#room_base_price');
    const nightsCountEl = document.querySelector('#calc_nights');
    const subtotalEl = document.querySelector('#calc_subtotal');
    const taxServiceEl = document.querySelector('#calc_tax');
    const grandTotalEl = document.querySelector('#calc_total');

    if (!checkInEl || !checkOutEl || !pricePerNightEl) return;

    const checkInVal = new Date(checkInEl.value);
    const checkOutVal = new Date(checkOutEl.value);

    if (isNaN(checkInVal.getTime()) || isNaN(checkOutVal.getTime())) return;

    const diffTime = checkOutVal.getTime() - checkInVal.getTime();
    let nights = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (nights < 1) nights = 1;

    const nightlyRate = parseFloat(pricePerNightEl.dataset.price || pricePerNightEl.textContent.replace(/[^0-9.]/g, '')) || 0;
    const subtotal = nightlyRate * nights;
    const taxService = subtotal * 0.10; // 10% taxes and resort fees
    const grandTotal = subtotal + taxService;

    if (nightsCountEl) nightsCountEl.textContent = nights + (nights === 1 ? ' Night' : ' Nights');
    if (subtotalEl) subtotalEl.textContent = '$' + subtotal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    if (taxServiceEl) taxServiceEl.textContent = '$' + taxService.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    if (grandTotalEl) grandTotalEl.textContent = '$' + grandTotal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  // Initial calculation on load
  recalculateLivePricing();

  // Quick Book Modal Population
  const quickBookModalEl = document.getElementById('quickBookModal');
  if (quickBookModalEl) {
    quickBookModalEl.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      if (!button) return;

      const roomId = button.getAttribute('data-room-id');
      const roomTitle = button.getAttribute('data-room-title');
      const roomPrice = button.getAttribute('data-room-price');
      const roomImage = button.getAttribute('data-room-image');

      const modalTitleEl = quickBookModalEl.querySelector('#modalRoomTitle');
      const modalPriceEl = quickBookModalEl.querySelector('#modalRoomPrice');
      const modalRoomIdInput = quickBookModalEl.querySelector('#modalRoomId');
      const modalImgEl = quickBookModalEl.querySelector('#modalRoomImg');
      const modalLinkEl = quickBookModalEl.querySelector('#modalRoomLink');

      if (modalTitleEl) modalTitleEl.textContent = roomTitle;
      if (modalPriceEl) modalPriceEl.textContent = '$' + roomPrice + ' / night';
      if (modalRoomIdInput) modalRoomIdInput.value = roomId;
      if (modalImgEl && roomImage) modalImgEl.src = roomImage;
      if (modalLinkEl) {
        const roomSlug = button.getAttribute('data-room-slug');
        if (roomSlug) modalLinkEl.href = '/rooms/' + roomSlug + '/book/';
      }
    });
  }

  // Copy Booking Reference Code Helper
  const copyBtn = document.getElementById('copyBookingCodeBtn');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      const code = this.getAttribute('data-code');
      if (code) {
        navigator.clipboard.writeText(code).then(() => {
          const originalText = copyBtn.innerHTML;
          copyBtn.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i> Copied!';
          setTimeout(() => {
            copyBtn.innerHTML = originalText;
          }, 2500);
        });
      }
    });
  }

  // Auto-dismiss Django success messages after 5 seconds
  const autoAlerts = document.querySelectorAll('.alert-dismissible');
  autoAlerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 6000);
  });
});

// Print Receipt function
function printReceipt() {
  window.print();
}
