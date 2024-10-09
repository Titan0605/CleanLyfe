const btn_nav_sidebar = document.querySelector('.--button-navbar');

btn_nav_sidebar.addEventListener('click', function () {
  document.getElementById('sidebar').classList.toggle('active');
  console.log(document.getElementById('sidebar'))
});

const btnsidebar = document.querySelector('.--sidebar');

btnsidebar.addEventListener('click', function () {
  document.getElementById('sidebar').classList.toggle('active');
  console.log(document.getElementById('sidebar'))
});