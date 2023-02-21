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