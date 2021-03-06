/**
 * views_counter JS plugin
 * Developed by RavenKiller, 2021.12.28
 * This source code is licensed under the MIT License found in the
 * LICENSE file in the root directory of this source tree.
 */
 $(document).ready(function(){
    var ids = ["vc_page_views", "vc_site_views", "vc_page_users", "vc_site_users"];
    var server_url = undefined;
    ids.forEach(id => {
        if($("#"+id).data("server-url")){
            if(!server_url){
                server_url = $("#"+id).data("server-url");
            }
        }
    })
    function vc_hide(){
        ids.forEach(id => {
            $("#"+id).hide();
        })
    }
    function vc_text(res){
        ids.forEach(id => {
            $("#"+id).text(res[id]);
        })
    }
    function vc_show(){
        ids.forEach(id => {
            $("#"+id).show();
        })
    }
    function vc_acquire(){
        vc_hide();
        $.ajax({
            url: server_url,
            type: "POST",
            crossDomain: true,
            data: {
                src: window.location.href,
            },
            success: res => {
            if(res["success"]){
                vc_text(res);
                vc_show();
            }else{
                console.log("Server error.")
            }
            },
            error: (XMLHttpRequest, textStatus, errorThrown) => {
                console.log(errorThrown);
            }
        })
    }
    vc_acquire();
})