const btnLoadMore = document.getElementById('btnLoadMore')
const divLoadMore = document.getElementById('divLoadMore')

const contact_list = document.getElementById('contact_list')
const contact_detail = document.getElementById('contact_detail')
const contact_caption_search = document.getElementById('contact_caption_search')

const list_size = 20
let upper = list_size
let contact_caption = ""
const getContacts = () => {
    $.ajax({
            type: 'GET',
            url: `/contact-list/${upper}/`,
            data: `caption=${contact_caption}`,
            success: function (response) {
                if (response.search('page-finished') > -1) {
                    console.log('dfas')
                    divLoadMore.style = "display: none"

                }
                contact_list.innerHTML += response

            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}
getContacts()
btnLoadMore.addEventListener('click', () => {
    upper += list_size
    getContacts()
})


function load_contact_detail(id) {
    $.ajax({
            type: 'GET',
            url: `/contact-detail/${id}/`,
            success: function (response) {
                contact_detail.innerHTML = response
                // console.log(response);
                load_my_select2();
                // load_conatct_modal();
            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}

function load_conatct_modal() {
    let ModalDiv = $("#contact-modal-wrapper");
    open_contact_modal = document.getElementById('open-contact-modal')
    open_contact_modal.addEventListener('click', () => {


        $.ajax({
            url: open_contact_modal.getAttribute('data-url'),
            type: 'GET',
            success: function (data) {
                ModalDiv.html(data);
                $("#editContract_").modal('show');
            }
        })
    });


    // $("#open-contact-modal").on("click", function() {
    //     $.ajax({
    //         url: $(this).attr("data-url"),
    //         type: 'GET',
    //         success: function(data) {
    //             ModalDiv.html(data);
    //             $("#share-note").modal('show');
    //         }
    //     });
    // });
}




function load_my_select2() {

    var lastResults = [];
    $(document).ready(function () {
        var select_item_c = $('#mySelect2').select2({
            placeholder: 'لطفا برچسب خود را وارد کنید',


            ajax: {
                url: 'http://127.0.0.1:8000/select2/',
                delay: 650,
            },
            closeOnSelect: true,
            allowClear: true,
            tags: true,
            multiple: true,
            tokenSeparators: [','],


            insertTag: function (data, tag) {
                // Insert the tag at the end of the results
                var select2element = $(this.$element);
                if (tag.newTag) {
                    tag.id = String(Math.ceil(Math.random() * 100));
                    data.push(tag);
                    var v = select2element.val();
                    if (v.indexOf(tag.id) == -1) {
                        v.push(tag.id)
                    }
                    setTimeout(function () {
                        select2element.val(v).trigger("change");
                    }, 200);

                }
            },
            createTag: function (params) {
                var term = $.trim(params.term);
                if (term === '') {
                    return null;
                }
                console.log(term)
                return {
                    id: term,
                    text: term,
                    newTag: true // add additional parameters
                }
            },
            templateResult: function (data) {
                var $result = $("<span></span>");
                $result.text(data.text);
                if (data.newTag) {
                    $result.append(" <em><strong> ( ایجاد کردن )  </strong></em>");
                }
                return $result;
            },

        });
    });

    $('#mySelect2').on('select2:select', function (e) {
        var data = e.params.data;
        if (data.newTag === true) {
            $('#contact_label_caption').val(data.text);
            $('#create_new_contact_label').modal('toggle');
        } else {
            add_contact_label(data.element.id, false);
        }


    });


    //
    // $('#mySelect2').select2({
    //     tags: true,
    //     createTag: function (params) {
    //         var term = $.trim(params.term);
    //         if (term === '') {
    //             return null;
    //         }
    //         return {
    //             id: term,
    //             text: term,
    //             newTag: true // add additional parameters
    //         }
    //     }
    // });
    //
    // $('#mySelect2').on('select2:select', function (e) {
    //     var data = e.params.data;
    //     if (data.newTag === true) {
    //         // var $select = $('#mySelect2');
    //         // var idToRemove = data.id;
    //         //
    //         // var values = $select.val();
    //         // if (values) {
    //         //     var i = values.indexOf(idToRemove);
    //         //     if (i >= 0) {
    //         //         values.splice(i, 1);
    //         //         $select.val(values).change();
    //         //     }
    //         // }
    //         $('#contact_label_caption').val(data.text);
    //         $('#create_new_contact_label').modal('toggle');
    //     } else {
    //         add_contact_label(data.element.id, false);
    //     }
    //
    //
    // });
    // $('#mySelect2').on('select2:unselect', function (e) {
    //     // Do something
    //     var data = e.params.data;
    //     delete_contact_label(data.element.id)
    // });
    //

}

function search_contacts() {
    upper = list_size
    contact_caption = contact_caption_search.value
    contact_list.innerHTML = ""
    divLoadMore.style = ""
    getContacts()
}

function creat_and_add_contact_label() {
    // console.log($('#contact_label_caption').val())
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
            type: 'POST',
            url: `/contact-define-label/`,
            data: {
                'caption': $('#contact_label_caption').val(),
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: function (response) {
                id = response.id;
                caption = response.caption
                add_contact_label(id, true);


            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}

function add_contact_label(id, reload) {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
            type: 'POST',
            url: `/contact-labels/`,
            data: {
                'contact_id': $('#contact_id').val(),
                'label_id': id,
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: function (response) {
                console.log(response)
            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function delete_contact_label(id) {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var contact_id = $('#contact_id').val()
    $.ajax({
            type: 'DELETE',
            url: `/contact-labels/${contact_id}/${id}/`,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: function (response) {
                console.log(response)
            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}




