//Ocultando o pop up de logout
document.addEventListener('DOMContentLoaded', function() {
    // Declarando uma variável de acordo com o ID
    var flashMessage = document.getElementById('flash-message');
    
    if (flashMessage) {
        // Definindo o tempo(ms) para sumir o pop up
        var timeout = 2000;

        //Definindo o timeout
        setTimeout(function() {
            flashMessage.style.opacity = 0;
            flashMessage.style.transition = 'opacity 0.5s ease-out';
            setTimeout(function() {
                // Oculta o elemento completamente após a transição
                flashMessage.style.display = 'none';
            }, 500); // Espera o tempo da transição antes de esconder o elemento
        }, timeout);
    }
});
