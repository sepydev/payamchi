class FileUpload {

    constructor(input) {
        this.input = input
        this.max_length = 1024 * 1024 * 10;
    }

    create_progress_bar() {
        var progress = `<div class="file-icon">
                            <i class="fa fa-file-o" aria-hidden="true"></i>
                        </div>
                        <div class="file-details">
                            <p class="filename"></p>
                            <small class="textbox"></small>
                            <div class="progress" style="margin-top: 5px;">
                                <div class="progress-bar bg-success" 
                                role="progressbar" 
                                aria-valuenow="0" 
                                aria-valuemin="0" 
                                aria-valuemax="100" 
                                style="width: 0%">
                                </div>
                            </div>
                        </div>`
        document.getElementById('uploaded_files').innerHTML = progress
    }

    upload() {
        this.create_progress_bar();
        this.initFileUpload();
    }

    initFileUpload() {

        this.file = this.input.files[0];
        this.upload_file(0, null);
    }

    //upload file
    upload_file(start, model_id) {
        var end;
        var self = this;
        var existingPath = model_id;
        var formData = new FormData();
        var nextChunk = start + this.max_length + 1;
        var currentChunk = this.file.slice(start, nextChunk);
        var uploadedChunk = start + currentChunk.size
        if (uploadedChunk >= this.file.size) {
            end = 1;
        } else {
            end = 0;
        }


        formData.append('file', currentChunk)
        formData.append('filename', this.file.name)
        $('.filename').text(this.file.name)
        $('.textbox').text("بارگذاری فایل")
        formData.append('end', end)
        formData.append('existingPath', existingPath);
        formData.append('nextSlice', nextChunk);
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });
        $.ajax({
            xhr: function () {
                var xhr = new XMLHttpRequest();
                xhr.upload.addEventListener('progress', function (e) {
                    if (e.lengthComputable) {
                        if (self.file.size < self.max_length) {
                            var percent = Math.round((e.loaded / e.total) * 100);
                        } else {
                            var percent = Math.round((uploadedChunk / self.file.size) * 100);
                        }
                        $('.progress-bar').css('width', percent + '%')
                        $('.progress-bar').text(percent + '%')
                    }
                });
                return xhr;
            },

            url: '/message-template-upload/',
            type: 'POST',
            cache: false,
            processData: false,
            contentType: false,
            data: formData,
            error: function (xhr) {
                alert(xhr.responseJSON.error)
            },
            success: function (data) {
                if (nextChunk < self.file.size) {
                    // upload file in chunks
                    existingPath = data.existingPath
                    self.upload_file(nextChunk, existingPath);
                } else {
                    // var file_name =  data['file_name'];
                    console.log(data)
                    let audio_source = document.getElementById('id_audio')
                    let url = data['url']
                    audio_source.src = url


                }
            }
        });
    };
}


ondragenter = function (evt) {
    evt.preventDefault();
    evt.stopPropagation();
};

ondragover = function (evt) {
    evt.preventDefault();
    evt.stopPropagation();
};

ondragleave = function (evt) {
    evt.preventDefault();
    evt.stopPropagation();
};

ondrop = function (evt) {
    evt.preventDefault();
    evt.stopPropagation();
    const files = evt.originalEvent.dataTransfer;
    var uploader = new FileUpload(files);
    uploader.upload();
};

