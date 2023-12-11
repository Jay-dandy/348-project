document.addEventListener("DOMContentLoaded", function() {
  // Document ready function can be expanded as needed
  console.log("Document ready!");

  // Example: Close flash messages after a delay
  setTimeout(function() {
    $('.alert').fadeOut('slow');
  }, 3000); // messages will fade out after 3 seconds
  
  // Example of adding an event listener to a button if needed
  const updateButtons = document.querySelectorAll('.update-btn');
  updateButtons.forEach(function(btn) {
    btn.addEventListener('click', function(event) {
      alert("Update button clicked!");
    });
  });
});
