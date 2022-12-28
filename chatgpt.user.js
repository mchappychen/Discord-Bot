// ==UserScript==
// @name         ChatGPT relay
// @version      1
// @description  relays messages from chatGPT to a localhost server (which sends it my discord bot)
// @author       Michael
// @match        https://chat.openai.com/chat
// @grant        GM.xmlHttpRequest
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// ==/UserScript==
/* globals jQuery, $, waitForKeyElements */


//Add jquery
var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
document.getElementsByTagName('head')[0].appendChild(script);

//Wait before running next part
function run(){
    console.log('running')
    //Check if chatgpt finished typing
    var DOM_length = $('form button').length;
    $('form button').on('DOMSubtreeModified', function(){
        if ($('form button').length == DOM_length || $('form button').length == 1){
            DOM_length = $('form button').length
            return
        }

        //Get chatgpt response text
        var response_elements = $('main div.flex.flex-col.items-center')[0].children[$('main div.flex.flex-col.items-center')[0].children.length-2].firstChild.lastChild.firstChild.firstChild.firstChild.children;

        var response = ''
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
        //xmlHttpRequest in tampermonkey needs to use this
        GM.xmlHttpRequest({
            method:'POST',
            url:'http://localhost:8080',
            onreadystatechange:function(xhr){
                console.log('received')
                if (xhr.readyState != 4 && xhr.status == 200 || xhr.responseText == "" || xhr.responseText == undefined){
                    console.log(1,xhr)
                    return
                }
                console.log(xhr)
                console.log(xhr.response,xhr.responseText,xhr.responseText == undefined)
                // console.log(JSON.parse(xhr.responseText.replace(/'/g,'"'))['msg'])
                $('textarea')[0].value = xhr.response
                try{
                    $('form button')[1].click()
                } catch(e){
                    $('form button')[1].click()
                }
            },
            data: JSON.stringify({
                'from': 'chatgpt',
                'msg': response
            })
        })

        DOM_length = $('form button').length
    });


    // Make connection with server, make sure server is running
    GM.xmlHttpRequest({
        method:'POST',
        url:'http://localhost:8080',
        onreadystatechange:function(xhr){
            console.log('received')
            if (xhr.readyState != 4 && xhr.status == 200 || xhr.responseText == "" || xhr.responseText == undefined){
                return
            }
            console.log(xhr)
            // console.log(JSON.parse(xhr.responseText.replace(/'/g,'"'))['msg'])
            $('textarea')[0].value = xhr.response
            try{
                $('form button')[1].click()
            } catch(e){
                $('form button')[0].click()
            }
        },
        data: JSON.stringify({
            'from': 'chatgpt',
            'msg':'ready'
        })
    })


}

//This waits until jQuery is loaded before doing run()
function defer(run) {
    if (window.jQuery) {
        run()
    } else {
        setTimeout(function() { defer(run) }, 200);
    }
}
//setTimeout(function(){defer(run)},1000);
defer(run)
