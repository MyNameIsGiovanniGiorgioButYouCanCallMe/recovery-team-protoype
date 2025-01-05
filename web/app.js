function toggleRelay() {
   fetch('/toggle').then(response => response.text()).then(console.log);
}