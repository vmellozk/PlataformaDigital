// Função para abrir o modal de acordo com a linha 35 e 44 do "perfil.html"
function openModal(modalId) {
    // Seleciona o elemento com o ID especificado, fazendo com o elemento seja exibido
    document.getElementById(modalId).style.display = 'block';
}

// Função para fechar o modal de acordo com a linha 122 e 161 do "perfil.html"
function closeModal(modalId) {
    // Selecione o elemento com o ID especificado e efine que deve ser ocultado
    document.getElementById(modalId).style.display = 'none';
}

// Form de troca de informações da linha 124 do "perfil.html", ele aguarda o click do botão com type="submit" da linha 152. Quando corre, a função passada como segundo argumento é executada. Essa qual é chamada para evitar que o formulário seja enviado da maneira padrão, que seria atualizar a página.
document.getElementById('editProfileForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Captura dos novos valores dos campos do formulário
    const username = document.getElementById('edit-username').value;
    const description = document.getElementById('edit-description').value;
    const birthdate = document.getElementById('edit-birthdate').value;
    const card = document.getElementById('edit-card').value;
    const fullname = document.getElementById('edit-fullname').value;
    const documents = document.getElementById('edit-documents').value;
    const location = document.getElementById('edit-location').value;
    const email = document.getElementById('edit-email').value;
    const social = document.getElementById('edit-social').value;
    const tipocadastro = document.getElementById('edit-tipocadastro').value;

    // Atualiza os elementos no perfil com os novos valores
    document.getElementById('username').innerText = username;
    document.getElementById('user-description').innerText = description;
    document.getElementById('birthdate').innerText = birthdate;
    document.getElementById('card').innerText = card;
    document.getElementById('fullname').innerText = fullname;
    document.getElementById('documents').innerText = documents;
    document.getElementById('location').innerText = location;
    document.getElementById('email').innerText = email;
    document.getElementById('social').innerText = social;
    document.getElementById('tipocadastro').innerText = tipocadastro;

    // Após atualizar o perfil, a função closeModal é chamada para fechar o modal de edição de perfil de acordo com o ID da linha 122.
    closeModal('editProfileModal');
});

// // Form de atualização de foto da linha 163 do "perfil.html", ele aguarda o click do botão com type="submit" da linha 166. Quando corre, a função passada como segundo argumento é executada. Essa qual é chamada para evitar que o formulário seja enviado da maneira padrão, que seria atualizar a página.
document.getElementById('changePicForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Captura do arquivo selecionado pelo usuário de acordo com o ID da linha 164
    const fileInput = document.getElementById('profile-pic-upload');
    //Verifica se o usuário selecionou um arquivo. Se verdadeiro, cria um novo FileReader() para ler o conteúdo do arquivo.
    if (fileInput.files && fileInput.files[0]) {
        // Define o que fazer quando o arquivo terminar de ser lido. Neste caso, atualiza dinamicamente a imagem do perfil (<img class="profile-pic">) com a nova imagem carregada.
        const reader = new FileReader();
        reader.onload = function(e) {
            // Atualiza a imagem do perfil com a nova imagem carregada
            document.querySelector('.profile-pic').src = e.target.result;
        }
        // Inicia a leitura do arquivo selecionado, convertendo-o para um formato de URL de dados que pode ser usado diretamente como a fonte de uma imagem.
        reader.readAsDataURL(fileInput.files[0]);
    }

    // Após atualizar a imagem do perfil, a função closeModal é chamada para fechar o modal de troca de foto do perfil.
    closeModal('changePicModal');

});

// Vai identificar o ID da linha 182 de "perfil.html" e adiciona um evento para detectar mudanças (seleção de arquivo)
document.getElementById('profile-pic-upload').addEventListener('change', function(event) {
    // Obtém o arquivo selecionado
    const file = event.target.files[0];
    // Verifica se o arquivo foi selecionado
    if (file) {
        // Cria um FileReader para ler o arquivo
        const reader = new FileReader();
        // Defininando uma função para ser chamada quando o arquivo estiver completo
        reader.onload = function(e) {
            // Seleciona a imagem para pré visualização
            const preview = document.getElementById('selected-pic-preview');
            // Define a fonte da imagem como o resultado da leitura do arquivo (URL do arquivo)
            preview.src = e.target.result;
            // Mostra a imagem
            preview.style.display = 'block';
        }
        // Lê o arquivo como uma URL de dados (data URL)
        reader.readAsDataURL(file);
    }
});

// Contador de caracteres restantes utilizando o DOM para interagir com o conteúdo da página
document.addEventListener('DOMContentLoaded', () => {
    // Define um array de objetos com informações sobre cada campo
    const fields = [
        { id: 'edit-username', maxLength: 12, counterId: 'usernamecharCounter' },
        { id: 'edit-description', maxLength: 250, counterId: 'descriptioncharCounter' },
        { id: 'edit-birthdate', maxLength: 10, counterId: 'birthdatecharCounter' },
        { id: 'edit-card', maxLength: 19, counterId: 'cardcharCounter' },
        { id: 'edit-fullname', maxLength: 40, counterId: 'fullnamecharCounter' },
        { id: 'edit-tipocadastro', maxLength: 10, counterId: 'cadastrocharCounter' },
        { id: 'edit-documents', maxLength: 14, counterId: 'documentscharCounter' },
        { id: 'edit-location', maxLength: 20, counterId: 'locationcharCounter' },
        { id: 'edit-email', maxLength: 30, counterId: 'emailcharCounter' },
        { id: 'edit-social', maxLength: 15, counterId: 'socialcharCounter' },
    ];

    // Para cada campo definido no array
    fields.forEach(field => {
        // Obtém o elemento de entrada correspondente pelo ID
        const inputElement = document.getElementById(field.id);
        // Obtém o elemento do contador correspondente pelo ID
        const counterElement = document.getElementById(field.counterId);

        // Adicione um ouvinte de evento para o input
        inputElement.addEventListener('input', () => {
            // Calcula o número restate de caracteres permitido
            const remaining = field.maxLength - inputElement.value.length;
            // Atualizada o texto do contador para mostrar os caracteres restantes 
            counterElement.textContent = `${remaining} caracteres restantes`;
        });
    });
});