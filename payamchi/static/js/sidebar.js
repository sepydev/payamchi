load_contact_labels_menu();


function load_contact_labels_menu() {

    //$('#div_contact_label_menu')[0].innerHTML = ''
    $.ajax({
            type: 'GET',
            url: `/contact-define-label/`,
            success: function (response) {
                $('#div_contact_label_menu')[0].innerHTML = response
            },
            error: function (error) {
                console.log(error);
            }
        }
    )


}