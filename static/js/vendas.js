document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea');
s
    function adjustHeight(el) {
        el.style.height = 'auto';
        el.style.height = `${el.scrollHeight}px`;
    }

    textareas.forEach(textarea => {
        textarea.addEventListener('input', () => adjustHeight(textarea));
        adjustHeight(textarea);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const fields = [
        { id: 'question1', maxLength: 100, counterId: 'question1Counter' },
        { id: 'question2', maxLength: 100, counterId: 'question2Counter' },
        { id: 'question3', maxLength: 100, counterId: 'question3Counter' },
        { id: 'question4', maxLength: 100, counterId: 'question4Counter' },
        { id: 'question5', maxLength: 100, counterId: 'question5Counter' },
        { id: 'question6', maxLength: 100, counterId: 'question6Counter' },
        { id: 'question7', maxLength: 100, counterId: 'question7Counter' },
        { id: 'question8', maxLength: 100, counterId: 'question8Counter' },
        { id: 'question9', maxLength: 100, counterId: 'question9Counter' },
        { id: 'question10', maxLength: 100, counterId: 'question10Counter' },
    ];

    fields.forEach(field => {

        const inputElement = document.getElementById(field.id);
        const counterElement = document.getElementById(field.counterId);

        inputElement.addEventListener('input', () => {
            const remaining = field.maxLength - inputElement.value.length;

            if (inputElement.value.length > field.maxLength) {
                inputElement.value = inputElement.value.slice (0, field.maxLength);
            }

            counterElement.textContent = `${remaining >=0 ? remaining: 0} caracteres restantes`;
        });
    });
});