$(function(){

    console.log(user, roomSlug)

    var url = 'ws://' + window.location.host + '/ws/room/' + roomSlug + '/'
    console.log(url)

    var chatSocket = new WebSocket(url)
    

    chatSocket.onopen = function(e){
        console.log('WEBSOCKET ABIERTO')
    }

    chatSocket.onclose = function(e){
        console.log('WEBSOCKET CERRADO')
    }

    chatSocket.onmessage = function(data) {
        const datamsj = JSON.parse(data.data)
        var msj = datamsj.message
        var username = datamsj.username
        var datetime = datamsj.datetime
        loadMessageHTML(msj, username, datetime);

    }
    

    document.querySelector('#sendMessage').addEventListener('click', sendMessage)
    document.querySelector('#inputMessage').addEventListener('keypress', function(e){
        if(e.keyCode == 13){
            sendMessage()
        }
    })

    function sendMessage(){
        var message = document.querySelector('#inputMessage')

        if(message.value.trim() !== ''){
            chatSocket.send(JSON.stringify({
                message: message.value.trim(),
                username: user,
                datetime: new Date().toISOString()
            }))


            message.value = ''
        } else {
            console.log('Envió un mensaje vacío')
        }

    }

    function loadMessageHTML(m, username, datetime){
        var currentDatetime = new Date();
        var dateObject = new Date(currentDatetime)

        var year = dateObject.getFullYear();
        var month = ('0' + (dateObject.getMonth() + 1)).slice(-2);
        var day = ('0' + dateObject.getDate()).slice(-2);
        var hours = ('0' + dateObject.getHours()).slice(-2);
        var minutes = ('0' + dateObject.getMinutes()).slice(-2);
        var seconds = ('0' + dateObject.getSeconds()).slice(-2);

        const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
        const isOwn = username === user;
        console.log(username, user, isOwn)
        document.querySelector('#boxMessages').innerHTML += `
        <div class="max-w-[80%] rounded-2xl px-4 py-2 text-sm ${isOwn ? 'bg-blue-600 text-white ml-auto mb-4 rounded-br-sm' : 'bg-gray-600 text-white ml-auto mb-4 rounded-bl-sm'}">
            ${m}
            <div class="mt-1 flex items-center gap-2 text-[11px] opacity-80">
                <small class="font-semibold italic">${username}</small>
                <small class="ml-auto">${formattedDate}</small>
            </div>
        </div>
        `
    }

})
