document.addEventListener("DOMContentLoaded", function(event) {
    if(typeof(WS_INCLUDE_WEBSOCKET) === "undefined"){
        // Counter of remaining ws_include blocks that have not been loaded
        let remainingWsIncludedBlocksCount = document.querySelectorAll(".ws_included-block").length;

        // Websocket that will be used by ws_include app
        WS_INCLUDE_WEBSOCKET = new WebSocket("ws://" + window.location.host + "/ws/ws_include/");

        // Once the websocket is opened, send messages requesting the rendered HTML
        // for each ws_included block.
        WS_INCLUDE_WEBSOCKET.addEventListener("open", event => {
            const wsIncludedBlocks = document.querySelectorAll(".ws_included-block")

            for (const wsIncludedBlock of wsIncludedBlocks) {
                const blockId = wsIncludedBlock.id;
                const wsRequest = JSON.stringify({
                    block_id: blockId,
                    path: wsIncludedBlock.dataset.template_path,
                    language_code: wsIncludedBlock.dataset.language_code,
                    context: wsIncludedBlock.dataset.context
                });
                // Delete previous content unless it is the spinner
                try{
                    document.querySelector(`#${block_id} > :not(.ws_included-spinner)`).remove();
                }catch(TypeError){
                }

                WS_INCLUDE_WEBSOCKET.send(wsRequest);
            }
         });

         // When a message is received, replace block content with the HTML
         WS_INCLUDE_WEBSOCKET.addEventListener("message", event => {
             const wsJsonResponse = JSON.parse(event.data);
             const blockId = wsJsonResponse["blockId"];
             console.log(wsJsonResponse["html"]);
             document.getElementById(blockId).innerHTML = wsJsonResponse["html"];
             remainingWsIncludedBlocksCount--;
             if(remainingWsIncludedBlocksCount === 0){
                 WS_INCLUDE_WEBSOCKET.close(1000, "Success");
             }
         });
    }
});
