const btnLoadMore = document.getElementById('btnLoadMore')
const divLoadMore = document.getElementById('divLoadMore')
const campaignList = document.getElementById('campaign_list')
const campaignDetail = document.getElementById('campaign_detail')
const campaignCaptionSearch = document.getElementById('campaign_caption_search')
const listSize = 10
let upper = listSize
let campaignCaption = ""
let fromDate = ''
let toDate = ''

campaignCaptionSearch.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        searchCampaigns();
    }
});


const getCampaigns = () => {
    let param = {
        'caption': campaignCaption, 'from_date': fromDate, 'to_date': toDate,
    }

    $.ajax({
        type: 'GET', url: `/campaign-list/${upper}/`, data: param, success: function (response) {
            if (response.search('page-finished') > -1) {
                divLoadMore.style.display = "none";
            }
            campaignList.innerHTML += response;
        }, error: function (error) {
            console.log(error);
        }
    })
}

function searchCampaigns() {
    upper = listSize
    campaignCaption = campaignCaptionSearch.value
    campaignList.innerHTML = ""
    divLoadMore.style.display = ""
    fromDate = ''
    toDate = ''

    let rangeDate;
    try {
        rangeDate = $('#campaign_date_range')[0].value
        fromDate = rangeDate.substring(0, 10)
        toDate = rangeDate.substring(13, 23)

    } catch (e) {
        console.log(e)
    }

    getCampaigns()
}

getCampaigns();

btnLoadMore.addEventListener('click', () => {
    upper += listSize
    getCampaigns()
});

function loadCampaignDetail(id, from_btn = false) {
    $.ajax({
        type: 'GET', url: `/campaign-detail/${id}/`, success: function (response) {
            campaignDetail.innerHTML = response;
            $('#status_select').selectpicker();
            $('#id_date_range_').MdPersianDateTimePicker({
                targetTextSelector: '#id_date_range_',
                targetDateSelector: '#id_date_range',
                dateFormat: 'yyyy-MM-dd',
                rangeSelector: true
            });
            if (!from_btn) {
                $.ajax({
                    type: 'GET', url: `/campaign-list/0/`, data: `campaign_id=${id}`, success: function (response) {
                        $(`#campaign-${id}`)[0].innerHTML = response
                    }, error: function (error) {
                        console.log(error);
                    }
                })
            }
        }, error: function (error) {
            console.log(error)
        }
    });
    loadCampaignMessages(id);
}

function loadCampaignMessages(id) {

    let fromDate = ''
    let toDate = ''
    let messageType = ''
    let rangeDate;
    try {
        rangeDate = $('#id_date_range')[0].value
        fromDate = rangeDate.substring(0, 10)
        toDate = rangeDate.substring(13, 23)
    } catch (e) {
    }
    try {
        messageType = $('#status_select')[0].value
    } catch (e) {
    }

    if (messageType == -1) {
        messageType = ''
    }

    let param = {
        'campaign_id': id, 'message_type': messageType, 'from_date': fromDate, 'to_date': toDate
    }

    $.ajax({
        type: 'GET', url: `/campaign-messages/`, data: param, success: function (response) {
            setTimeout(function () {


                $('#div_campaign_messages')[0].innerHTML = response;
            }, 300);

        }, error: function (error) {
            console.log(error)
        }
    });
}


