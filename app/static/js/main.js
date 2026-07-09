// Ventana de confirmación antes de ciertos formularios (eliminación por ejemplo)

document.addEventListener('DOMContentLoaded', () => {
    // busca en todos los formularios que tengas la clase js-confirm
    document.querySelectorAll('.js-confirm').forEach((form) => {
        // al enviar, ejecuta el evento
        form.addEventListener('submit', (event) => {
            // form.dataset.confirmMessage es el mensaje de confirmaicón en HTML
            const message = form.dataset.confirmMessage || '¿Confirmas de verdad esta acción?';
            // si el usuario no confirm, prevee que sae un error...
            if(!window.confirm(message)){event.preventDefault();}
        });
    });
});