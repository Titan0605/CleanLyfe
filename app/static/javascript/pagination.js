/**
 * Constants used throughout the pagination functionality
 * @constant {Object} CONSTANTS
 */
const CONSTANTS = {
  LAST_PAGE: 5,
  FIRST_PAGE: 1,
  ELEMENTS: {
    FORM: "hidric_form",
    PAGINATION: "pagination",
    NEXT: "next",
    PREV: "prev",
    SUBMIT: "submit_button",
  },
};

/**
 * Main event listener that initializes the pagination functionality when the DOM is fully loaded
 * Sets up navigation buttons and pagination controls
 */
document.addEventListener("DOMContentLoaded", () => {
  const paginationButtons = getPaginationButtons();
  const navigationButtons = {
    next: document.getElementById(CONSTANTS.ELEMENTS.NEXT),
    prev: document.getElementById(CONSTANTS.ELEMENTS.PREV),
    submit: document.getElementById(CONSTANTS.ELEMENTS.SUBMIT),
  };

  // Congigurate pagination buttons
  Array.from(paginationButtons)
    .slice(1, -1)
    .forEach((actualButton) => {
      actualButton.addEventListener("click", () => {
        if (!actualButton.classList.contains("active")) {
          const previousButton = paginationButtons[getActualPage()];
          const currentValue = parseInt(actualButton.value);

          previousButton.classList.toggle("active");
          actualButton.classList.toggle("active");

          // Manage visibility of buttons
          navigationButtons.next.hidden = currentValue >= CONSTANTS.LAST_PAGE;
          navigationButtons.submit.hidden = currentValue < CONSTANTS.LAST_PAGE;
          navigationButtons.prev.hidden = currentValue <= CONSTANTS.FIRST_PAGE;

          changeFormPage(previousButton.value - 1, actualButton.value - 1);
        }
      });
    });

  /**
   * Event handler for the previous page button
   * Updates page visibility and navigation controls when moving to previous page
   */
  navigationButtons.prev.addEventListener("click", (event) => {
    const actualPage = getActualPage();
    const nextPage = actualPage - 1;

    if (actualPage <= CONSTANTS.LAST_PAGE) {
      navigationButtons.next.hidden = false;
      navigationButtons.submit.hidden = true;
    }
    if (nextPage <= CONSTANTS.FIRST_PAGE) event.target.hidden = true;

    updatePages(actualPage, nextPage);
  });

  /**
   * Event handler for the next page button
   * Updates page visibility and navigation controls when moving to next page
   */
  navigationButtons.next.addEventListener("click", (event) => {
    const actualPage = getActualPage();
    const nextPage = actualPage + 1;

    if (actualPage >= CONSTANTS.FIRST_PAGE) navigationButtons.prev.hidden = false;
    if (nextPage >= CONSTANTS.LAST_PAGE) {
      event.target.hidden = true;
      navigationButtons.submit.hidden = false;
    }

    updatePages(actualPage, nextPage);
  });
});

/**
 * Updates the active state of pagination buttons and changes the visible form page
 * @param {number} previusPage - Index of the previous page
 * @param {number} nextPage - Index of the next page to display
 */
function updatePages(previusPage, nextPage) {
  const paginationButtons = getPaginationButtons();

  paginationButtons[previusPage].classList.toggle("active");
  paginationButtons[nextPage].classList.toggle("active");

  changeFormPage(paginationButtons[previusPage].value - 1, paginationButtons[nextPage].value - 1);
}

/**
 * Gets the current active page number
 * @returns {number|null} The current page number or null if no active page is found
 */
function getActualPage() {
  const paginationButtons = Array.from(getPaginationButtons());
  const activeButton = paginationButtons.find((button, index) => index > 0 && index < paginationButtons.length - 1 && button.classList.contains("active"));
  return activeButton ? parseInt(activeButton.value) : null;
}

/**
 * Changes the visibility of form pages, hiding the previous page and showing the next
 * @param {number} previusPage - Index of the page to hide
 * @param {number} nextPage - Index of the page to show
 */
function changeFormPage(previusPage, nextPage) {
  const formPages = Array.from(document.getElementById(CONSTANTS.ELEMENTS.FORM).getElementsByClassName("page"));
  formPages[previusPage].hidden = true;
  formPages[nextPage].hidden = false;
}

/**
 * Gets all pagination buttons from the DOM
 * @returns {HTMLCollection} Collection of pagination button elements
 */
function getPaginationButtons() {
  return document.getElementById(CONSTANTS.ELEMENTS.PAGINATION).getElementsByTagName("li");
}
