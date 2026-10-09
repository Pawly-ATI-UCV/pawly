(function () {
  'use strict';

  /*  templates: application_form.html, login.html, register.html  */
  function isEmpty(field) {
    return field.value.trim() === '';
  }

  function setError(form, field, message) {
    const box = form.querySelector('[data-error-for="' + field.id + '"]');
    field.setAttribute('aria-invalid', message ? 'true' : 'false');
    if (box) {
      box.textContent = message;
      box.hidden = !message;
    }
  }

  function validate(form) {
    let firstInvalid = null;
    form.querySelectorAll('[required]').forEach(function (field) {
      const message = isEmpty(field) ? field.dataset.error : '';
      setError(form, field, message);
      if (message && !firstInvalid) firstInvalid = field;
    });
    if (firstInvalid) firstInvalid.focus();
    return firstInvalid === null;
  }

  function enableValidation(form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (validate(form) && form.dataset.next) window.location.href = form.dataset.next;
    });
  }

  /*  templates: login.html, register.html  */
  function enablePasswordToggle(button) {
    button.addEventListener('click', function () {
      const input = document.getElementById(button.dataset.togglePassword);
      const show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      button.setAttribute('aria-pressed', String(show));
    });
  }

  /*  template: application_form.html  */
  const applicationMessage = document.querySelector('#application-message');
  if (applicationMessage) enableValidation(applicationMessage.form);

  /*  template: login.html  */
  const loginUser = document.querySelector('#login-user');
  if (loginUser) {
    enableValidation(loginUser.form);
    enablePasswordToggle(document.querySelector('[data-toggle-password="login-password"]'));
  }

  /*  template: register.html  */
  const registerUser = document.querySelector('#register-username');
  if (registerUser) {
    enableValidation(registerUser.form);
    enablePasswordToggle(document.querySelector('[data-toggle-password="register-password"]'));
  }
})();
