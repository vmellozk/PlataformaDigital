function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

document.getElementById('editProfileForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('edit-username').value;
    const description = document.getElementById('edit-description').value;
    document.getElementById('username').innerText = username;
    document.getElementById('user-description').innerText = description;
    closeModal('editProfileModal');
});

document.getElementById('changePicForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('profile-pic-upload');
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.querySelector('.profile-pic').src = e.target.result;
        }
        reader.readAsDataURL(fileInput.files[0]);
    }
    closeModal('changePicModal');
});
