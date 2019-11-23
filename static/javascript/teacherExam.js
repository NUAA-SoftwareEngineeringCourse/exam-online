base_url_str = 'http://localhost:5000'

function submmit_exam() {
    $('#exam-submit-button').click(function (event) {
        alert('exam submit button click')
    })
}


$(document).ready(function () {
    submmit_exam()
})