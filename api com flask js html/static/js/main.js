document.addEventListener('DOMContentLoaded', function() {
    const userForm = document.getElementById('user-form');
    const usersTableBody = document.querySelector('#users-table tbody');

    // Função para carregar a lista de usuários
    function loadUsers() {
        fetch('/users')
            .then(response => response.json())
            .then(users => {
                usersTableBody.innerHTML = ''; // Limpar a tabela
                users.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td><button class="delete-btn" data-id="${user.id}">Excluir</button></td>
                    `;
                    usersTableBody.appendChild(row);
                });
                addDeleteHandlers();
            })
            .catch(error => console.error('Erro ao carregar usuários:', error));
    }

    // Função para adicionar um novo usuário
    userForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(userForm);
        const data = {
            name: formData.get('name'),
            email: formData.get('email')
        };

        fetch('/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(user => {
            loadUsers();  // Atualizar a lista de usuários
            userForm.reset();  // Limpar o formulário
        })
        .catch(error => console.error('Erro ao adicionar usuário:', error));
    });

    // Função para adicionar evento de delete aos botões
    function addDeleteHandlers() {
        const deleteButtons = document.querySelectorAll('.delete-btn');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const userId = this.getAttribute('data-id');
                fetch(`/users/${userId}`, {
                    method: 'DELETE'
                })
                .then(() => {
                    loadUsers();  // Atualizar a lista de usuários
                })
                .catch(error => console.error('Erro ao excluir usuário:', error));
            });
        });
    }

    // Carregar a lista de usuários ao abrir a página
    loadUsers();
});
