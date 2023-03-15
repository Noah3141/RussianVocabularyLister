const toggleLinkButton = document.getElementById("wiki-button");
const wikiLinks = document.querySelectorAll(".wiki-link-RU");
const LangDisp = document.querySelector(".button-row div")

toggleLinkButton.addEventListener("click", function() {
  wikiLinks.forEach(link => {
    if (link.classList.contains("wiki-link-RU")) {
      link.classList.remove("wiki-link-RU");
      link.classList.add("wiki-link-EN");
      var this_link = link.getAttribute("href")
      this_link = this_link.replace("//ru.","//en.")
      link.href = this_link
      LangDisp.textContent = "EN"
    } else if (link.classList.contains("wiki-link-EN")) {
      link.classList.remove("wiki-link-EN");
      link.classList.add("wiki-link-RU");
      var this_link = link.getAttribute("href")
      this_link = this_link.replace("//en.","//ru.")
      link.href = this_link
      LangDisp.textContent = "RU"
    }
  });
});

const list = document.querySelectorAll(".update-entry")
for (let i = 1; i < list.length; i++) {
    var currentButtonId = "update-entry-" + (i);


    // Get a reference to the update button element
    const updateButton = document.getElementById(currentButtonId);

    // Attach a click event listener to the update button
    updateButton.addEventListener('click', function(event) {

      // Get the value of the button (which is the data we want to send)
      const data = updateButton.value;

      const input_tag = document.getElementById("input_text");
      const input_text = input_tag.value; 
  
      // Send an AJAX request to the server
      fetch('/flag-word', {
        method: 'POST',
        body: JSON.stringify({ value: data, input_text: input_text }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (response.ok) {
          console.log('Flagged word successfully');
        } else {
          console.error('Failed to flag word');
        }
      })
      .catch(error => {
        console.error(error);
      });
      
      // Prevent the default form submission behavior
      event.preventDefault();
    });
}