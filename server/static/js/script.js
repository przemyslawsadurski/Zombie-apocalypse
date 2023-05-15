console.log("Hello from js")

function showInterface(option) {
    var interfaces = document.getElementsByClassName("interface");
    for (var i = 0; i < interfaces.length; i++) {
      interfaces[i].style.display = "none";
    }
  
    var selectedInterface = document.getElementById(option + "-interface");
    if (selectedInterface) {
      selectedInterface.style.display = "block";
    }
  }