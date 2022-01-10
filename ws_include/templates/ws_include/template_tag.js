document.addEventListener("DOMContentLoaded", function(event) {

    // Common code
    if(typeof(WS_INCLUDE_WEBSOCKET) === "undefined"){
        WS_INCLUDE_WEBSOCKET = new WebSocket("ws://" + window.location.host + "/ws/ws_include/");

        // When a message is received, replace block content with the HTML
        WS_INCLUDE_WEBSOCKET.addEventListener("message", event => {
            const wsJsonResponse = JSON.parse(event.data);
            const blockId = wsJsonResponse["blockId"];
            const scriptBlockId = `script_${blockId}`;
            document.getElementById(scriptBlockId).remove();
            document.getElementById(blockId).innerHTML = wsJsonResponse["html"];
        });
    }

    // Send a message for each block once the websocket is open
    WS_INCLUDE_WEBSOCKET.addEventListener("open", event => {
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
