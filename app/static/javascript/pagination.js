document.addEventListener("DOMContentLoaded", () => {
    const paginationButtons = getPaginationButtons()

    for(let i = 1; i < paginationButtons.length - 1; i++){
        const actualButton = paginationButtons[i]

        actualButton.addEventListener('click', () => {
            if(!actualButton.classList.contains('active')){
                const previousButton = paginationButtons[getActualPage()]

                previousButton.classList.toggle('active')
                actualButton.classList.toggle('active')

                changeFormPage(previousButton.value - 1, actualButton.value - 1)
            }
        })
    }

    document.getElementById('prev').addEventListener('click', (event) => {
        const actualPage = getActualPage()
        const nextPage = actualPage - 1

        const button = event.target
    
        if(nextPage < 1) {
            // button.hidden = true
            return
        }
    
        updatePages(actualPage, nextPage)
    })

    document.getElementById('next').addEventListener('click', (event) => {
        const actualPage = getActualPage()
        const nextPage = actualPage + 1

        const button = event.target
    
        if(nextPage > 4) {
            // button.hidden = true
            // document.getElementById('submit_button').hidden = false
            return
        }
    
        updatePages(actualPage, nextPage)
    })
})

function updatePages(previusPage, nextPage) {
    const paginationButtons = getPaginationButtons()

    paginationButtons[previusPage].classList.toggle('active')
    paginationButtons[nextPage].classList.toggle('active')

    changeFormPage(paginationButtons[previusPage].value - 1, paginationButtons[nextPage].value - 1)
}

function getActualPage() {
    let actualPage = 0
    const paginationButtons = getPaginationButtons()

    for(let i = 1; i < paginationButtons.length - 1; i++){
        const actualButton = paginationButtons[i]

        if(actualButton.classList.contains('active')){
            actualPage = actualButton.value
            break
        }
    }
    if(actualPage != 0) return actualPage
}

function changeFormPage(previusPage, nextPage) {
    const formPages = document.getElementById('hidric_form').getElementsByClassName('page')

    formPages[previusPage].hidden = true
    formPages[nextPage].hidden = false
}

function getPaginationButtons() {
    const paginationButtons = document.getElementById('pagination').getElementsByTagName('li')
    return paginationButtons
}