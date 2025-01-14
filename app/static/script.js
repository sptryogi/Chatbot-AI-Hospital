// Handle search schedule
document.getElementById("searchForm").onsubmit = async (e) => {
  e.preventDefault();
  const doctor = document.getElementById("doctor").value;
  const specialty = document.getElementById("specialty").value;

  const response = await fetch(`/search_schedule?doctor=${doctor}&specialty=${specialty}`);
  const results = await response.json();
  document.getElementById("searchResults").innerHTML = results.map(r =>
    `<p>${r.doctor} (${r.specialty}): ${r.days}, ${r.times}</p>`
  ).join("");
};

// Handle booking
document.getElementById("bookingForm").onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  const response = await fetch('/book_appointment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  document.getElementById("bookingResponse").innerHTML = `<p>${result.message}</p>`;
};

// Load booking history
async function loadBookingHistory() {
    const response = await fetch('/booking_history');
    const data = await response.json();
  
    const bookingHistoryTableBody = document.getElementById("bookingHistoryTable").querySelector("tbody");
    bookingHistoryTableBody.innerHTML = ""; // Clear existing rows
  
    data.bookings.forEach(booking => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${booking.doctor}</td>
        <td>${booking.date}</td>
        <td>${booking.time}</td>
        <td>${booking.patient_name}</td>
      `;
      bookingHistoryTableBody.appendChild(row);
    });
  }
  
  // Handle booking form submission
  document.getElementById("bookingForm").onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
  
    const response = await fetch('/book_appointment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  
    const result = await response.json();
    document.getElementById("bookingResponse").innerHTML = `<p>${result.message}</p>`;
    loadBookingHistory(); // Reload booking history
  };
  
  // Load booking history on page load
  document.addEventListener("DOMContentLoaded", loadBookingHistory);

// Handle chatbot
document.getElementById("chatForm").onsubmit = async (e) => {
    e.preventDefault();
    const question = document.getElementById("chatInput").value;
  
    const response = await fetch('/ask_bot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    const result = await response.json();
    document.getElementById("chatResponse").innerHTML = `<p>${result.response}</p>`;
  };
  

// Handle health tips
document.getElementById("tipsForm").onsubmit = async (e) => {
  e.preventDefault();
  const query = document.getElementById("tipsQuery").value;

  const response = await fetch(`/get_health_tips?query=${query}`);
  const results = await response.json();
  document.getElementById("tipsResults").innerHTML = results.tips.map(t =>
    `<p>${t}</p>`
  ).join("");
};
