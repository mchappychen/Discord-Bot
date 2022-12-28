//This script is ran in chat.openai.com to relay messages to my discord bot

//Add jquery
var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
document.getElementsByTagName('head')[0].appendChild(script);

//Wait before running next part
function run(){
    console.log('running')
    //Check if chatgpt finished typing
    DOM_length = $('form button').length
    $('form button').on('DOMSubtreeModified', function(){
        if ($('form button').length == DOM_length || $('form button').length == 1){
            DOM_length = $('form button').length
            return
        }
        
        //Get chatgpt response text
        response_elements = $('main div.flex.flex-col.items-center')[0].children[$('main div.flex.flex-col.items-center')[0].children.length-2].firstChild.lastChild.firstChild.firstChild.firstChild.children;
        
        response = ''
        for (let x=0; x<response_elements.length;x++){
            if (response_elements[x].tagName == 'P'){
                response += response_elements[x].textContent + '\n\n'
            } else if (response_elements[x].tagName == 'PRE'){
                response += '```' + response_elements[x].firstChild.lastChild.textContent + '```'
            } else if (response_elements[x].tagName == 'OL'){
                response += '\n'
                for (let y=0;y<response_elements[x].children.length;y++){
                    response += y+1 + '. ' + response_elements[x].children[y].textContent + '\n\n'
                }
            } else {
                console.log('ERROR: response_elements tagName at',x,':',response_elements[x].tagName)
            }
        }
    
        console.log('From chatgpt:',response)
    
        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:8080', true);
        xhr.send(JSON.stringify({
            'from': 'chatgpt',
            'msg':response
        }));

        //This runs if we receive a message from discord (our localhost http server)
        xhr.onreadystatechange = function(){
            if (xhr.readyState != 4 && xhr.status == 200 || xhr.response == ""){
                return
            }
            console.log('From discord:',xhr.response)
            // console.log(JSON.parse(xhr.responseText.replace(/'/g,'"'))['msg'])

            $('textarea')[0].value = xhr.response
           $('form button')[1].click()
        }
        DOM_length = $('form button').length
      });
      
    
    // Make connection with server, make sure server is running
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:8080', true);
    
    //This function runs if we receive something from server
    xhr.onreadystatechange = function(){
        if (xhr.readyState != 4 && xhr.status == 200 || xhr.response == ""){
            return
        }
        console.log(xhr)
        console.log(xhr.response)
        // console.log(JSON.parse(xhr.responseText.replace(/'/g,'"'))['msg'])
        $('textarea')[0].value = xhr.response
        try{
            $('form button')[1].click()
        } catch(e){
            $('form button')[0].click()
        }
    }
    
    //Send initial connection to server
    xhr.send(JSON.stringify({
        'from': 'chatgpt',
        'msg':'ready'
    }));
}

//This waits until jQuery is loaded before doing run()
function defer(run) {
    if (window.jQuery) {
        run()
    } else {
        setTimeout(function() { defer(run) }, 50);
    }
}
defer(run)
