let fetchInit = {
    headers: {
        'X-API-Request': 1
    }
};

function handleErrors(response) {
    if (!response.ok) {
        if (response.status === 401) {
            window.location.href = '/login/';
        } else {
            throw Error(response.statusText);
        }
    }
    return response.json();
}

function flash_message(message, type) {
    const alertNode = $(`<div class="alert alert-${type}" role="alert">${message}</div>`);
    $('#messages').append(alertNode);
    setTimeout(()=>{alertNode.remove()}, 10000);
}

function showModal(title, roles, user) {
    $('.modal-title').text(title);
    $('#selectRole').html(roles.map((role)=>`<option value="${role.id}">${role.name}</option>`));
    if (user !== null) {
        $('#userId').val(user.id);
        $('#inputUsername').val(user.username);
        $('#selectRole').val(user.role.id);
    }
    $('#exampleModalCenter').modal('show');
}

function load_users() {
    fetch(`/users/`, fetchInit)
        .then(handleErrors)
        .then(result => {
            const users = result.map((user) => `<tr><td>${user.id}</td><td>${user.username}</td><td>${user.role.name}</td><td><input type="hidden" name="user_id" value="${user.id}"><button type="button" class="btn btn-outline-primary edit-user mr-4">Edit</button><button type="button" class="btn btn-outline-danger delete-user">Delete</button></td></tr>`)
            $('#users').html(users.join())
        })
        .catch(error => {
            flash_message(`${error}`, 'danger')
        });
}

function init_app() {
    $('#users')
        .on('click', '.edit-user', function (e) {
            const user_id = $(e.target).closest('tr').find('input[name=user_id]').val();

            Promise.all([
                fetch(`/users/${user_id}/`, fetchInit).then(handleErrors),
                fetch(`/roles/`, fetchInit).then(handleErrors)
            ]).then(([user, roles]) => {
                showModal('Edit user', roles, user)
            }).catch(error => {
                flash_message(`${error}`, 'danger')
            });
        })
        .on('click', '.delete-user', function (e) {
            const user_id = $(e.target).closest('tr').find('input[name=user_id]').val();
            fetch(`/users/${user_id}/`, {
                ...fetchInit,
                'method': 'DELETE'
            }).then(handleErrors)
            .then(result => {
                load_users();
                flash_message(result.message, 'success');
            }).catch(error => {
                flash_message(`${error}`, 'danger')
            });
        });
    $('.add-user').on('click', function(e) {
        fetch('/roles/', fetchInit).then(response => response.json()).then((roles) => {
            showModal('Add new user', roles, null);
        });
    });
    $('#exampleModalCenter').on('hidden.bs.modal', function (e) {
        $('.modal-title').text('');
        $('#selectRole').html('');
        $('#userId').val('');
        $('#inputUsername').val('');
        $('#inputPassword').val('');
    });
    $('#saveUser').on('click', function(e) {
        const userId = $('#userId').val();
        const username = $('#inputUsername').val();
        const password = $('#inputPassword').val();
        const roleId = $('#selectRole').val();
        let url = '';
        let method = '';
        let successMessage = '';
        if (userId) {
            url = `/users/${userId}/`;
            method = 'PUT';
            successMessage = 'User updated successfully'
        } else {
            url = '/users/';
            method = 'POST';
            successMessage = 'User added successfully'
        }
        let formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('role_id', roleId);
        fetch(url, {
            ...fetchInit,
            method: method,
            body: formData
        }).then(handleErrors)
            .then(user => {
                load_users();
                $('#exampleModalCenter').modal('hide');
                flash_message(successMessage, 'success');
            })
            .catch(error => {
                flash_message(`${error}`, 'danger')
            });
    });
}

$(document).ready(function() {
    init_app();
    load_users();
});
