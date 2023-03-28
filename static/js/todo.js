

$(document).ready(function () {
  show_todo();
});
function show_todo() { // 보여주기 
  fetch('/todo')
    .then((res) => res.json())
    .then((data) => {
      let rows = data['result'];
      $('#todo-list').empty();
      rows.forEach((a) => {
        let todo = a['todo'];
        let id = a['_id']
        let temp_html = `<div id=${id}>
                             <div class="todo-body">
                             <h2 class="gray"><input type="checkbox"> ${todo}</h2>
                             <div class="start">
                                  <button onclick="open_put('${id}')">수정</button>
                                  <button onclick="deletebtn('${id}')">삭제</button>
                             </div>
                                <div class="finish" style="display: none">
                                  <input type="text" value='${todo}'/>
                                  <button onclick="updatebtn('${id}')">완료</button>
                                  <button onclick="cancel_put('${id}')">취소</button>
                                </div>
                              </div>
                            </div>
                            `;
                            

        $('#todo-list').append(temp_html);
      });

    });
}

function save_todo() { // 저장하기
  let todo = $('#todo').val();
  let formData = new FormData();
  formData.append('todo_give', todo);

  fetch('/todo', { method: 'POST', body: formData })
    .then((response) => response.json())
    .then((data) => {
      alert(data['msg']);
      window.location.reload();
    });
}


function deletebtn(id) { // 삭제하기
  let formData = new FormData();
  formData.append('id', id);
  fetch('/todo', { method: 'DELETE', body: formData })
    .then((res) => res.json())
    .then((data) => {
      alert(data['msg']);
      window.location.reload();
    }
    )
}
//업데이트
function updatebtn(id) {
  $(`#${id} .todo-body .start`).show();
  $(`#${id} .todo-body .finish`).hide();
  let formData = new FormData();
  let new_todo = $(`#${id} .todo-body .finish input`).val();
  formData.append("id", id);
  formData.append("new_todo", new_todo);

  fetch('/todo', {
    method: "PUT",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data['msg']);
      window.location.reload();
    }
    )
};

function open_put(id) {
  $(`#${id} .todo-body .start`).hide();
  $(`#${id} .todo-body .finish`).show();
}

function cancel_put(id) {
  $(`#${id} .todo-body .start`).show();
  $(`#${id} .todo-body .finish`).hide();
}
