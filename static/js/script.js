document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('notificationModal');
    var openBtn = document.getElementById('openModalBtn');
    var closeBtn = document.getElementsByClassName('close')[0];
    var readBtn = document.getElementById('readBtn');

    openBtn.onclick = function () {
        modal.style.display = 'block';
    }

    closeBtn.onclick = function () {
        modal.style.display = 'none';
    }

    readBtn.onclick = function () {
        modal.classList.add('expanded');
        readBtn.textContent = 'Close';
        readBtn.onclick = function () {
            modal.classList.remove('expanded');
            modal.style.display = 'none';
            // readBtn.textContent = 'Read';
            readBtn.onclick = function () {
                modal.style.display = 'block';
            }
        }
    }
});
