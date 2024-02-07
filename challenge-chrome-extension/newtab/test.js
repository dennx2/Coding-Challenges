const currentDate = new Date();
const options = {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
  hour: "numeric",
  minute: "numeric",
  hour12: false
};
const formattedDateTime = currentDate.toLocaleDateString("en-US", options);
console.log(formattedDateTime.split("at"));
