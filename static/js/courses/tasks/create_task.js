document.addEventListener('DOMContentLoaded', () => {
    const selectTask = document.querySelector('#SelectTask')

    // Hidden Components
    const hiddenComponentsIds = ['TaskText', 'TaskVideo', 'TaskProject', 'TaskQuestions', 'TaskCode']
    let hiddenComponents = []

    hiddenComponentsIds.forEach(hiddenComponentId => {
        hiddenComponents.push(document.querySelector(`#${hiddenComponentId}`))
    })

    // Hide all components
    const hideAllComponents = () => {
        for (const hiddenComponent of hiddenComponents) {
            hiddenComponent.style.display = 'none'
        }
    }    

    // Show selected component
    selectTask.addEventListener('change', () => {
        let selectedValue = selectTask.value

        hideAllComponents()

        const elem = document.querySelector(`#${selectedValue}`);
        elem.style.display = 'flex';
    })

})