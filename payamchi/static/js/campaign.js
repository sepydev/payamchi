const btnLoadMore = document.getElementById('btnLoadMore')
const divLoadMore = document.getElementById('divLoadMore')
const campaign_list = document.getElementById('campaign_list')
const campaign_detail = document.getElementById('campaign_detail')
const campaign_caption_search = document.getElementById('campaign_caption_search')
const list_size = 10
let upper = list_size
let campaign_caption = ""
let page_load = true

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

get_campaigns()

btnLoadMore.addEventListener('click', () => {
    upper += list_size
    get_campaigns()
})


function load_campaign_detail(id) {
    $.ajax({
            type: 'GET',
            url: `/campaign-detail/${id}/`,
            success: function (response) {
                campaign_detail.innerHTML = response;
                $('#status_select').selectpicker();
                page_load = false;
                $('#id_date_range').MdPersianDateTimePicker({
                    targetTextSelector: '#id_date_range',
                    targetDateSelector: '#id_date_range_',
                    dateFormat: 'yyyy-MM-dd',
                    range: true
                });
                //$('.must-be-seelcte2').select2();

            },
            error: function (error) {
                console.log(error)
            }
        }
    );
}


