
document.querySelector('form').addEventListener('submit', () => {
    document.documentElement.scrollTop = 0;
    document.querySelector('.card').classList.add('blur');
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    document.querySelector('body').appendChild(spinner);
});

[...document.querySelectorAll('.fields div')].map(fieldGroup =>
    fieldGroup.querySelector('input').addEventListener('input', event =>
        fieldGroup.querySelector('span').textContent = event.target.value
    )
);