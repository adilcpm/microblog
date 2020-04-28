$(document).ready(function() {
    function updateScroll(){
        var element = document.getElementById("chat-history");
        element.scrollTop = element.scrollHeight;
    };
    updateScroll();
    const CHATUSER = $('#chatuser').val();
    const CURRENTUSER = $('#currentuser').val();
    var canPublish = true;
    var throttleTime = 500;
    var clearInterval = 900;
    clearTimerId = setTimeout(function () {
        //clear user is typing message
        $('#typing').hide();
        }, clearInterval);

    var socket = io();
    socket.on('recieve message', function(json_msg) {
        let msg_html = ''
        if(json_msg.recipient == CHATUSER){
            // Check whether this is my message or other user's msg
            msg_html = `
            <li class="clearfix">
                <div class="message-data align-right">
                    <span class="message-data-time" >${ moment().calendar() }</span> &nbsp; &nbsp;
                    <span class="message-data-name" >${ json_msg.author }</span> <i class="fa fa-circle me"></i>
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
                    <span class="message-data-name"><i class="fa fa-circle online"></i> ${ json_msg.author }</span>
                    <span class="message-data-time">${ moment().calendar()}</span>
                </div>
                <div class="message my-message">
                    ${ json_msg.body }
                </div>
            </li>`;
        }
        $("#messages").append(msg_html);
        updateScroll();
        console.log('Received message');
    });

    $('#sendbutton').on('click', function() {
        socket.emit('send message', $('#myMessage').val() );
        $('#myMessage').val('');
    });
    $('.chat-message').keyup(function() {
        // Triggering Typing Animation
        console.log('Inside keyup');
        if(canPublish) {
            console.log('Emitting Typing !');
            socket.emit('typing', CURRENTUSER );
            canPublish = false;
            setTimeout(function() {
              canPublish = true;
            }, throttleTime);
        }
    });
    socket.on('typed', function(user){
        if(user != CURRENTUSER ){ 
            $('#typing').show() ;
            console.log('Triggered Typing')
            clearTimeout(clearTimerId);
            clearTimerId = setTimeout(function () {
                //clear user is typing message
                $('#typing').hide();
                }, clearInterval);
        };
    });
    socket.on('online', function(user){
        console.log('Online : ' + user)
        if(user == CHATUSER){
            console.log('online setted !')
            $('#chat-avatar').attr("style","border-color: #86BB71;")
        }
    });
    socket.on('offline', function(user){
        console.log('')
        if(user == CHATUSER){
            $("#chat-avatar").attr("style","border-color: transparent;")
        }
    })
});