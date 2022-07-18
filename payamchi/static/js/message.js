const btnLoadMore = document.getElementById('btnLoadMore')
const divLoadMore = document.getElementById('divLoadMore')
const messageList = document.getElementById('messageList')
const messageDetail = document.getElementById('messageDetail')
const messageCaptionSearch = document.getElementById('messageCaptionSearch')
let messageCaption = ""
const listSize = 10
let upper = listSize


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

