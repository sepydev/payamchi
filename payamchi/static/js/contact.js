const btnLoadMore = document.getElementById('btnLoadMore')
const divLoadMore = document.getElementById('divLoadMore')
const contact_list = document.getElementById('contact_list')
const contact_detail = document.getElementById('contact_detail')
const contact_caption_search = document.getElementById('contact_caption_search')
const list_size = 20
let upper = list_size
let contact_caption = ""

const get_contacts = () => {
    $.ajax({
            type: 'GET',
            url: `/contact-list/${upper}/`,
            data: `caption=${contact_caption}`,
            success: function (response) {
                if (response.search('page-finished') > -1) {
                    divLoadMore.style.display ="none"

                }
                contact_list.innerHTML += response

            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}

function search_contacts() {
    upper = list_size
    contact_caption = contact_caption_search.value
    contact_list.innerHTML = ""
    divLoadMore.style.display = ""
    get_contacts()
}

get_contacts()

btnLoadMore.addEventListener('click', () => {
    upper += list_size
    get_contacts()
})


function load_contact_detail(id) {
    $.ajax({
            type: 'GET',
            url: `/contact-detail/${id}/`,
            success: function (response) {
                contact_detail.innerHTML = response
                prepare_contact_label();
            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}

function prepare_contact_label() {
    $(document).ready(function () {
        $('#contact_labels').select2({
            placeholder: 'لطفا برچسب خود را وارد کنید',
            ajax: {
                url: '/contact-define-labels/',
                delay: 650,
            },
            closeOnSelect: true,
            allowClear: true,
            tags: true,
            multiple: true,
            tokenSeparators: [','],
            insertTag: function (data, tag) {
                // Insert the tag at the end of the results
                let select2element = $(this.$element);
                if (tag.newTag) {
                    tag.id = String(Math.ceil(Math.random() * 100));
                    data.push(tag);
                    let v = select2element.val();
                    if (v.indexOf(tag.id) === -1) {
                        v.push(tag.id)
                    }
                    setTimeout(function () {
                        select2element.val(v).trigger("change");
                    }, 200);

                }
            },
            createTag: function (params) {
                let term = $.trim(params.term);
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
                let $result = $("<span></span>");
                $result.text(data.text);
                if (data.newTag) {
                    $result.append(" <em><strong> ( ایجاد کردن )  </strong></em>");
                }
                return $result;
            },

        });
    });

    $('#contact_labels').on('select2:select', function (e) {
        let data = e.params.data;
        if (data.newTag === true) {
            $('#contact_label_caption').val(data.text);
            $('#create_new_contact_label').modal('toggle');
        } else {
            add_contact_label(data.element.id);
        }
    });
}


function creat_and_add_contact_label() {
    // console.log($('#contact_label_caption').val())
    let tokenizers = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
            type: 'POST',
            url: `/contact-define-label/`,
            data: {
                'caption': $('#contact_label_caption').val(),
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', tokenizers);
            },
            success: function (response) {
                add_contact_label(response.id);
            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}

function add_contact_label(id) {
    let tokenizers = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
            type: 'POST',
            url: `/contact-labels/`,
            data: {
                'contact_id': $('#contact_id').val(),
                'label_id': id,
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', tokenizers);
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


function delete_contact_label(id) {
    let tokenizers = jQuery("[name=csrfmiddlewaretoken]").val();
    let contact_id = $('#contact_id').val()
    $.ajax({
            type: 'DELETE',
            url: `/contact-labels/${contact_id}/${id}/`,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', tokenizers);
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




