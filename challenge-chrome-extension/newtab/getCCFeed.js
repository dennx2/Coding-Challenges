// Parse the feed to get challenge list
// https://codingchallenges.substack.com/feed

function getCCFeed() {
  const challengeList = document.querySelector("#challenge-list");

  const url = "https://codingchallenges.substack.com/feed";
  fetch(url)
    .then(res => res.text())
    .then(xmlString => {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlString, "text/xml");
      const items = xmlDoc.getElementsByTagName("item");

      function stringToNode(htmlString) {
        const tempContainer = document.createElement("p");
        htmlString = htmlString.trim();
        tempContainer.innerHTML = htmlString;
        return tempContainer.firstChild();
      }

      for (let i = 0; i < 4; i++) {
        const title = items[i].getElementsByTagName("title");
        console.log(title);
        challengeList.appendChild(
          stringToNode(`
            <p>${title}</p>
        `)
        );
      }
    })
    .catch(error => console.error(error));
}

getCCFeed();
