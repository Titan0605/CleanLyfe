document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.querySelector('[data-drawer-toggle="drawer-navigation"]');
  const sidebar = document.getElementById("drawer-navigation");

  if (toggleButton && sidebar) {
    toggleButton.addEventListener("click", function () {
      sidebar.classList.toggle("-translate-x-full");
    });

    // Cerrar sidebar al hacer clic fuera de él
    document.addEventListener("click", function (event) {
      if (!sidebar.contains(event.target) && !toggleButton.contains(event.target)) {
        sidebar.classList.add("-translate-x-full");
      }
    });
  }
});
