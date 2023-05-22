document.addEventListener('DOMContentLoaded', function() {
  var interfaceElements = document.getElementsByClassName('interface');

  for (var i = 0; i < interfaceElements.length; i++) {
    interfaceElements[i].addEventListener('click', function() {
      var interfaceId = this.getAttribute('data-interface-id');
      showInterface(interfaceId);
    });
  }
});

function showInterface(interfaceId) {
  var interfaceDivs = document.getElementsByClassName('interface-pop');

  for (var i = 0; i < interfaceDivs.length; i++) {
    interfaceDivs[i].style.display = 'none';
  }

  var selectedInterface = document.getElementById(interfaceId);

  if (selectedInterface) {
    selectedInterface.style.display = 'block';
  }
}
function validateForm() {
  console.log("czy to sie odpala?")
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var confirmPassword = document.getElementById("confirm-password").value;
  var email = document.getElementById("email").value;

  var emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address");
    return false;
  }

  var passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
  if (!passwordRegex.test(password)) {
    alert("Password must contain at least 8 characters, including letters and numbers");
    return false;
  }

  var usernameRegex = /^[a-zA-Z0-9]+$/;
  if (!usernameRegex.test(username)) {
    alert("Username can only contain alphanumeric characters (alphabetical letters and numbers)");
    return false;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    return false;
  }

  return true;
}