function deleteU(uid) {

    $.ajax({
        type: 'post',
        url: '/deleteUser',
        async: true,
        data: {
            'user_id': uid,
        },
        success: function (data) {
            alert("删除成功!")
            window.location.reload()
        }
    })
}

function deleteE(eid) {
    alert("试卷即将删除")
    $.ajax({
        type: 'post',
        url: '/deleteExam',
        async: true,
        data: {
            'exam_id': eid,
        },
        success: function (data) {
            alert("删除成功!")
            window.location.reload()
        }
    })
}


function deleteQ(qid, qtype) {
    alert("试题即将删除")
    $.ajax({
        type: 'post',
        url: '/deleteQuestion',
        async: true,
        data: {
            'q_id': qid,
            'q_type': qtype,
        },
        success: function (data) {
            alert("删除成功!")
            window.location.reload()
        }
    })
}

function choiceModal() {
    $('#choice-modal').modal('show')
}

function judgeModal() {
    $('#judge-modal').modal('show')
}

function subjectiveModal() {
    $('#subjective-modal').modal('show')
}


function add_xuanze() {
    var desc = $('#choice_q').val()
    var value = $('#choice_value').val()
    var answer = $('#choice_ans').val()
    var diff = $('#choice_diff').val()
    var q_A = $('#q_A').val()
    var q_B = $('#q_B').val()
    var q_C = $('#q_C').val()
    var q_D = $('#q_D').val()
    var q_class = $('#choice_class').val()

    $.ajax({
        type: 'post',
        url: '/admin_addchoice',
        async: true,
        data: {
            'q_desc': desc,
            'q_answer': answer,
            'q_value': value,
            'q_diff': diff,
            'q_A': q_A,
            'q_B': q_B,
            'q_C': q_C,
            'q_D': q_D,
            'q_class':q_class,
        },
        success: function (data) {
            alert("添加成功!")
            window.location.reload()
        }
    })
}

function add_judge() {
    var desc = $('#judge_q').val()
    var value = $('#judge_value').val()
    var answer = $('#judge_ans').val()
    var diff = $('#judge_diff').val()
    var q_class = $('#judge_class').val()
    $.ajax({
        type: 'post',
        url: '/add_A_question',
        async: true,
        data: {
            'q_type': 2,
            'q_desc': desc,
            'q_answer': answer,
            'q_value': value,
            'q_diff': diff,
            'q_class': q_class
        },
        success: function (data) {
            alert("添加成功!")
            window.location.reload()
        }
    })
}

function add_subj() {
    var desc = $('#subj_q').val()
    var value = $('#subj_value').val()
    var answer = $('#subj_ans').val()
    var diff = $('#subj_diff').val()
    var q_class = $('#subj_class').val()
    $.ajax({
        type: 'post',
        url: '/add_A_question',
        async: true,
        data: {
            'q_type': 3,
            'q_desc': desc,
            'q_answer': answer,
            'q_value': value,
            'q_diff': diff,
            'q_class': q_class
        },
        success: function (data) {
            alert("添加成功!")
            window.location.reload()
        }
    })
}
