$(document).ready(function() {
    function updateScroll(){
        var element = document.getElementById("chat-history");
        element.scrollTop = element.scrollHeight;
    };
    updateScroll();
    const CHAT_USER = $('#chatuser').val()
    const CURRENT_USER = $('#currentuser').val();
    var canPublish = true;
    var throttleTime = 300;
    var clearInterval = 900;
    var socket = io();
    clearTimerId = setTimeout(function () {
        //clear user is typing message
        $('#typing').hide();
        }, clearInterval);

    $('#sendbutton').on('click', function() {
        if($('#myMessage').val().trim() == ''){ return } //Check if field is empty, then do nothing
        socket.emit('send message', $('#myMessage').val() );
        $('#myMessage').val('');
    });
    $('.chat-message').keyup(function(e) {
        // Triggering Typing Animation
        if(e.keyCode == 13){
            $('#sendbutton').trigger('click'); //If key pressed is Enter, trigger click function
        };
        if(canPublish) {
            socket.emit('typing', CURRENT_USER );
            canPublish = false;
            setTimeout(function() {
              canPublish = true;
            }, throttleTime);
        }
    });
    socket.on('receive message', function(json_msg) {
        let msg_html = ''
        if(json_msg.author == CURRENT_USER){
            // Check whether this is my message or other user's msg
            msg_html = `
            <li class="clearfix">
                <div class="message-data align-right">
                    <span class="message-data-time" >${ moment().calendar() }</span> &nbsp; &nbsp;
                    <span class="message-data-name" >${ json_msg.author }</span> <span class="mydot me"></span>
                </div>
                <div class="message other-message float-right">
                    ${json_msg.body}
                    </div>
            </li>`;
        }
        else{
            msg_html = `
            <li>
                <div class="message-data">
                    <span class="message-data-name"><span class="mydot online"></span> ${ json_msg.author }</span>
                    <span class="message-data-time">${ moment().calendar()}</span>
                </div>
                <div class="message my-message">
                    ${ json_msg.body }
                </div>
            </li>`;
            socket.emit('read msg');
        }
        $("ul#messages li:nth-last-child(2)").after(msg_html);
        updateScroll();
    });
    socket.on('typed', function(user){
        if(user != CURRENT_USER ){ 
            $('#typing').show() ;
            clearTimeout(clearTimerId);
            clearTimerId = setTimeout(function () {
                //clear user is typing message
                $('#typing').hide();
                }, clearInterval);
        };
    });
    socket.on('online', function(user){
        if(user == CHAT_USER){
            $('#chat-avatar').attr("style","border-color: #86BB71;") 
        }
    });
    socket.on('offline', function(user){
        console.log('')
        if(user == CHAT_USER){
            $("#chat-avatar").attr("style","border-color: transparent;")
        }
    });
    socket.on('refresh', function(){ 
        //Reload the Page, true is not force from server
        location.reload(true);
    });
});
