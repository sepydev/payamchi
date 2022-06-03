const btnLoadMore = document.getElementById('btnLoadMore')
const divLoadMore = document.getElementById('divLoadMore')
const campaign_list = document.getElementById('campaign_list')
const campaign_detail = document.getElementById('campaign_detail')
const campaign_caption_search = document.getElementById('campaign_caption_search')
const list_size = 10
let upper = list_size
let campaign_caption = ""

campaign_caption_search.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        search_campaigns();
    }
});


const get_campaigns = () => {
    $.ajax({
            type: 'GET',
            url: `/campaign-list/${upper}/`,
            data: `caption=${campaign_caption}`,
            success: function (response) {
                if (response.search('page-finished') > -1) {
                    divLoadMore.style.display = "none";
                }
                campaign_list.innerHTML += response;
            },
            error: function (error) {
                console.log(error);
            }
        }
    )
}

function search_campaigns() {
    upper = list_size
    campaign_caption = campaign_caption_search.value
    campaign_list.innerHTML = ""
    divLoadMore.style.display = ""
    get_campaigns()
}

get_campaigns();

btnLoadMore.addEventListener('click', () => {
    upper += list_size
    get_campaigns()
});

function load_campaign_detail(id, from_btn = false) {
    $.ajax({
            type: 'GET',
            url: `/campaign-detail/${id}/`,
            success: function (response) {
                campaign_detail.innerHTML = response;
                $('#status_select').selectpicker();
                $('#id_date_range_').MdPersianDateTimePicker({
                    targetTextSelector: '#id_date_range_',
                    targetDateSelector: '#id_date_range',
                    dateFormat: 'yyyy-MM-dd',
                    rangeSelector: true
                });
                if (!from_btn) {
                    $.ajax({
                            type: 'GET',
                            url: `/campaign-list/0/`,
                            data: `campaign_id=${id}`,
                            success: function (response) {
                                $(`#campaign-${id}`)[0].innerHTML = response
                            },
                            error: function (error) {
                                console.log(error);
                            }
                        }
                    )
                }
            },
            error: function (error) {
                console.log(error)
            }
        }
    );
    load_campaign_messages(id);
}

function load_campaign_messages(id) {

    let from_date = ''
    let to_date = ''
    let message_type = ''
    let range_date;
    try {
        range_date = $('#id_date_range')[0].value
        from_date = range_date.substring(0, 10)
        to_date = range_date.substring(13, 23)
    } catch (e) {
    }
    try {
        message_type = $('#status_select')[0].value
    } catch (e) {
    }

    if (message_type == -1) {
        message_type = ''
    }

    let param = {
        'campaign_id': id,
        'message_type': message_type,
        'from_date': from_date,
        'to_date': to_date
    }

    $.ajax({
            type: 'GET',
            url: `/campaign-messages/`,
            data: param,
            success:
                function (response) {
                    $('#div_campaign_messages')[0].innerHTML = response;
                }
            ,
            error: function (error) {
                console.log(error)
            }
        }
    )
    ;
}


