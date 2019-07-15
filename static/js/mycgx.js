
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
}

var CGX_URL="http://127.0.0.1:5000";
var key=uuidv4();

function output(msg) {
    cur = $("#output").val();
    $("#output").val(cur+msg+"\n");
    
}
$('#sites_button').on('click',(event)=>{
    $.ajax({
        type :'post',
        url: CGX_URL+"/get/sites",
        data: JSON.stringify({key: key}),
        dataType: 'json',
        contentType: 'application/json',
        success: (data) => {
            console.log(data)
            for (site of data.sites) {
                output(site.name);
            };
        },
        error: (data) => {
            console.log("can't get sites");
        },
    });
})
$('#token_button').on('click',(event)=>{
    $.ajax({
        type :'post',
        url: CGX_URL+"/login",
        data: JSON.stringify({key: key, token: $("#token").val()}),
        dataType: 'json',
        contentType: 'application/json',
        success: (data) => {
            console.log("login success");
            output("login successfull");
        },
        error: (data) => {
            console.log("login failed");
            output(data);
        },
    });
})

$('#clear_button').on('click',(event)=>{
    $("#output").val("");

})