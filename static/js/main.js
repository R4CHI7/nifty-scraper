function getLocalTime(value1) {
  var date = new Date(value1 * 1000);
  document.write(date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'}));
}
