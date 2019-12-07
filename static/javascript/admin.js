function deleteU(uid){

    $.ajax({
        type: 'post',
        url: '/deleteUser',
        async: true,
        data:{
          'user_id': uid,
        },
        success: function (data) {
            alert("删除成功!")
            window.location.reload()
        }
    })
}

function deleteE(eid){
    alert("试卷即将删除")
    $.ajax({
        type: 'post',
        url: '/deleteExam',
        async: true,
        data:{
          'exam_id': eid,
        },
        success: function (data) {
            alert("删除成功!")
            window.location.reload()
        }
    })
}