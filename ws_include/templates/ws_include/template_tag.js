document.addEventListener("DOMContentLoaded", function(event) {

    if(typeof(WS_INCLUDE_WEBSOCKET) === 'undefined'){
        WS_INCLUDE_WEBSOCKET = new WebSocket('ws://' + window.location.host + '/ws/ws_include/');

        WS_INCLUDE_WEBSOCKET.addEventListener('message', event => {
            const wsJsonResponse = JSON.parse(event.data);
            const blockId = wsJsonResponse['blockId'];
            const scriptBlockId = `script_${blockId}`;
            if(document.getElementById(scriptBlockId)){
                document.getElementById(scriptBlockId).remove();
                document.getElementById(blockId).innerHTML = wsJsonResponse['html'];
            }
            console.log('Message from server ', wsJsonResponse);
        });
    }

    WS_INCLUDE_WEBSOCKET.addEventListener('open', event => {
        const blockId = "{{block_id}}";
        const context = {{context|safe}};
        const wsRequest = JSON.stringify({
            block_id: blockId,
            path: "{{template_path}}",
            language_code: "{{language_code}}",
            context: context
        });
        // Delete previous content unless it is the spinner
        try{
            document.querySelector("#{{block_id}} > :not(.ws_included-spinner)").remove();
        }catch(TypeError){
        }

        WS_INCLUDE_WEBSOCKET.send(wsRequest);
    });
});
