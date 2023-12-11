(function () {
  // Tu código JavaScript aquí

  function createInterface() {
    /*const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href="../css/chatbot.css";
    console.log(link);
    document.head.appendChild(link);*/

    const interfaz2 = document.createElement("div");
    interfaz2.textContent = "Hola, mundo";
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(interfaz2, s);
  }

  // La función que crea la interfaz
  createInterface();
})();