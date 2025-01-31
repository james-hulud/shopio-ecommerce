const isLoggedIn = document.getElementById('auth-status').getAttribute('data-logged-in')

if (isLoggedIn === "True") {
  const username = document.getElementById('username').getAttribute('data-current-user')

  document.write('<div class="dropdown d-flex">');
  document.write('<button class="btn btn-primary dropdown-toggle dropdown__btn" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">');
  document.write('<i class="fa-solid fa-user"></i>');
  document.write('</button>');
  document.write('<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">');
  document.write(`<a class="dropdown-item" href="/${username}/account">Your account</a>`);
  document.write('<a class="dropdown-item" href="/signout">Sign out</a>');
  document.write('</div></div>');
} else {
  document.write('<div class="dropdown d-flex">');
  document.write('<button class="btn btn-primary dropdown-toggle dropdown__btn" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">');
  document.write('Account');
  document.write('</button>');
  document.write('<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">');
  document.write('<a class="dropdown-item" href="/signin">Sign in</a>');
  document.write('<a class="dropdown-item" href="/register">Register</a>');
  document.write('</div></div>');
}