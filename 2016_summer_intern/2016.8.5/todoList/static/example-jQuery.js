(function() {
    var $todoForm = $('#todoForm');
    var $todoInput = $('#todoInput');
    var $todoList = $('todoList');
    var $todoCount = $('todoCount');

    function count(){
        var len = $todoList.children().length;
        $todoCount.html(len > 0 ? 'œ÷”–' + len + 'œÓ todo list' : '');
    }

    $todoForm.submit(function(e){
        var input_value = $todoInput.val();
        $todoList.append('<li>' + input_value + '&nbsp;<a href="#" class="todoDelete">x</a></li>');
        $todoInput.val('');
        count();
    });
})();