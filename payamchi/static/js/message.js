const btnLoadMore = document.getElementById('btnLoadMore')
const divLoadMore = document.getElementById('divLoadMore')
const messageList = document.getElementById('messageList')
const messageDetail = document.getElementById('messageDetail')
const messageCaptionSearch = document.getElementById('messageCaptionSearch')
let messageCaption = ""
const listSize = 10
let upper = listSize
let newMessageLabel = null


messageCaptionSearch.addEventListener(
    "keypress",
    function (event) {
        if (event.key === "Enter") {
            event.preventDefault()
            searchMessages()
        }
    }
)

const getMessages = () => {
    let param = {
        'caption': messageCaption,
    }
    $.ajax(
        {
            type: 'GET',
            url: `/message-list/${upper}/`,
            data: param,
            success: function (response) {
                if (response.search('page-finished') > -1) {
                    divLoadMore.style.display = "none"
                }
                messageList.innerHTML += response
            },
            error: function (error) {
                console.log(error)
            }

        }
    )
}

function searchMessages() {
    upper = listSize
    messageCaption = messageCaptionSearch.value
    messageList.innerHTML = ""
    divLoadMore.style.display = ""
    getMessages()
}

getMessages()

btnLoadMore.addEventListener('click', () => {
    upper += listSize
    getMessages()
})

function loadMessageDetail(id, fromButton = false) {

    $.ajax({
            type: 'GET',
            url: `/message-detail/${id}/`,
            success: function (response) {
                messageDetail.innerHTML = response
                prepareMessageLabel()
                prepareContactLabel()
                loadCharts(id)
                $('#id_send_date_persian').MdPersianDateTimePicker({
                    targetTextSelector: '#id_send_date_persian',
                    targetDateSelector: '#id_send_date',
                    enableTimePicker: true,
                    dateFormat: 'yyyy-MM-dd hh:mm',
                });
                // $('.my_selects').selectpicker()
                if (!fromButton) {
                    $.ajax({
                        type: 'GET',
                        url: `message-list/0/`,
                        data: `message_id=${id}`,
                        success: function (response) {
                            $(`#message-${id}`)[0].innerHTML = response
                        },
                        error: function (error) {
                            console.log(error)
                        }
                    })
                }
            },
            error: function (error) {
                console.log(error)
            }

        }
    )

}

function saveMessage(id) {
    detail_form = document.getElementById('#detail_form')
    let tokenizers = jQuery("[name=csrfmiddlewaretoken]").val();
    let data = $('#detail_form').serialize()
    let messageLabels = $('#messageLabels')
    let contactLabels = $('#contactLabels')
    let newLabels = []
    messageLabels.select2('data').forEach( function (item) {
         if ( item.newTag)
         {
             newLabels.push(item.text)
         }
        }
    )
    data += '&message_labels=' + messageLabels.select2('val')
    data += '&new_message_labels=' + newLabels
    data += '&contact_labels=' + contactLabels.select2('val')
    console.log(data)
    console.log(messageLabels.select2('val'))
    $.ajax({
        type: 'POST',
        url: `/message-detail/${id}/`,
        data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', tokenizers);
        },
        success: function (response) {
            messageDetail.innerHTML = response
            prepareMessageLabel()
            prepareContactLabel()
            loadCharts(id)
            $('#id_send_date_persian').MdPersianDateTimePicker({
                targetTextSelector: '#id_send_date_persian',
                targetDateSelector: '#id_send_date',
                enableTimePicker: true,
                dateFormat: 'yyyy-MM-dd hh:mm',
            });

            $.ajax({
                type: 'GET',
                url: `/message-list/0/`,
                data: `message_id=${id}`,
                success: function (response) {
                    $(`#message-${id}`)[0].innerHTML = response
                },
                error: function (error) {
                    console.log(error)
                }
            })

        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log('SERVER ERROR: ' + thrownError);
        }

    })
}


function prepareMessageLabel() {
    let messageLabels = $('#messageLabels')
    console.log("prepareMessageLabel")

    messageLabels.select2({
        placeholder: 'لطفا برچسب خود را وارد کنید',
        ajax: {
            url: '/message-define-labels/',
            delay: 650,
        },
        dir: "rtl",
        closeOnSelect: true,
        allowClear: true,
        tags: true,
        multiple: true,
        tokenSeparators: [','],
        insertTag: function (data, tag) {
            let select2element = $(this.$element);
            if (tag.newTag) {
                tag.id = String(Math.ceil(Math.random() * 100)*-1);
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
    messageLabels.on('select2:select', function (e) {
        // let data = e.params.data;
        // if (data.newTag === true) {
        //     newMessageLabel = data.text
        //     $('#messageLabelCaption').val(data.text);
        //     $('#createNewMessageLabel').modal('toggle');
        // }
    });

}


function createMessageLabel() {
    // console.log($('#contact_label_caption').val())
    let tokenizers = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
            type: 'POST',
            url: `/message-define-label/`,
            data: {
                'caption': $('#messageLabelCaption').val(),
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', tokenizers);
            },
            success: function (response) {

            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}


function prepareContactLabel() {
    let contactLabels = $('#contactLabels')

    contactLabels.select2({
        placeholder: 'لطفا برچسب خود را وارد کنید',
        ajax: {
            url: '/contact-define-labels/',
            delay: 650,
        },
        dir: "rtl",
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
            // return {
            //     id: term,
            //     text: term,
            //     newTag: true // add additional parameters
            // }
        },
        templateResult: function (data) {
            let $result = $("<span></span>");
            $result.text(data.text);
            // if (data.newTag) {
            //     $result.append(" <em><strong> ( ایجاد کردن )  </strong></em>");
            // }
            return $result;
        },

    });
    // contactLabels.on('select2:select', function (e) {
    //     let data = e.params.data;
    //     // if (data.newTag === true) {
    //     //     $('#messageLabelCaption').val(data.text);
    //     //     $('#createNewMessageLabel').modal('toggle');
    //     // }
    // });

}
function loadCharts(id){
    $.ajax({
        type:'GET',
        url:`/message-detail/chart/${id}/`,
        success: function (response){
            console.log(response)
            Morris.Donut({
                element: 'chartContactType',
                data: [{
                    label: "\xa0 \xa0 موبایل \xa0 \xa0",
                    value: response["mobile_count"],

                }, {
                    label: "\xa0 \xa0 تلفن \xa0 \xa0",
                    value: response["tel_count"]
                },
                ],
                resize: true,
                redraw: true,
                colors: ['#222fb9', 'rgb(255, 122, 1)', '#21b731'],
                //responsive:true,

            });
            Morris.Donut({
                element: 'chartCredit',
                data: [{
                    label: "\xa0 \xa0 معتبر \xa0 \xa0",
                    value: response["valid_numbers"],

                }, {
                    label: "\xa0 \xa0 نامعتبر \xa0 \xa0",
                    value: response["invalid_numbers"]
                }, ],
                resize: true,
                redraw: true,
                colors: ['#222fb9', 'rgb(255, 122, 1)', '#21b731'],
                //responsive:true,

            });

        },
        error: function (error){
            console.log(error)
        }

    })

}
