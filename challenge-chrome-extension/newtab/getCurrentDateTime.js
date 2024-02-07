const currentTimeElement = document.querySelector("#current-time");
const currentDayElement = document.querySelector("#current-day");

currentDayElement.textContent = "hello";

function updateCurrentTime() {
  const currentDateUTC = new Date();
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    hour12: false
  };
  const formattedDateTime = currentDateUTC.toLocaleDateString("en-US", options);
  const day = formattedDateTime.split("at")[0];
  const time = formattedDateTime.split("at")[1];

  currentDayElement.textContent = day;
  currentTimeElement.textContent = time;
}

updateCurrentTime();
setInterval(() => {
  updateCurrentTime();
}, 1000);
