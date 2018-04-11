var deleteButtons = document.querySelectorAll('.delete_note');

deleteButtons.forEach(function(button){

  button.addEventListener('click', function(trigger){

    var check = confirm("Delete Note: Please confirm you want to delete?");

    if (!check) {
      trigger.preventDefault();
    }

  })
});
