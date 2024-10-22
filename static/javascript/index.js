const btn_nav_sidebar = document.querySelector('.navbar__sidebar-button'); /* Function to call a block of html with a class */

btn_nav_sidebar.addEventListener('click', function () { /*Funtion to modify the class of the block selected when is clicked*/
  document.getElementById('sidebar').classList.toggle('active'); /*This specify which class we are going to add or delete*/
});

const btnsidebar = document.querySelector('.--sidebar');

btnsidebar.addEventListener('click', function () { /*Funtion to modify the class of the block selected when is clicked*/
  document.getElementById('sidebar').classList.toggle('active'); /*This specify which class we are going to add or delete*/
});