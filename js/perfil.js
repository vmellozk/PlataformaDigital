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