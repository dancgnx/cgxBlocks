
function CGX_uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
}

var CGX_URL="http://127.0.0.1:5000";
var CGX_key=CGX_uuidv4();
var CGX_Logged_In = false;
var CGX_save;
var CGX_resp;

// login to CGX gateway server
// input token
// return true if successful
function CGX_Login(token) {
    $.ajax({
        type :'post',
        url: CGX_URL+"/login",
        data: JSON.stringify({key: CGX_key, token: token}),
        dataType: 'json',
        async: false,
        contentType: 'application/json',
        success: (data) => {
            console.log("login success");
            CGX_Logged_In = true;
            return true;
        },
        error: (data) => {
            console.log("login failed");
            return false;
        },
    });
}
const copyToClipboard = str => {
    const el = document.createElement('textarea');
    el.value = str;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
};
  
// print message at textarea id=output
function CGX_output(msg) {
    cur = $("#output").val();
    $("#output").val(cur+msg+"\n");
}   
var resp;
// return a list of sites
function CGX_get_sites(){
    CGX_resp=null;
    $.ajax({
        type :'post',
        url: CGX_URL+"/get/sites",
        data: JSON.stringify({key: CGX_key}),
        dataType: 'json',
        async: false,
        contentType: 'application/json',
        success: (data) => {
            resp= data.sites;
        },
        error: (data) => {
            console.log("can't get sites");
        }
    });
    if (resp.status == 200) {
        return resp.responesJSON;
    } else {
        return []
    }
}

$('#clear_button').on('click',(event)=>{
    $("#output").val("");
});
$('#save_button').on('click',(event)=>{
    CGX_save = Blockly.Xml.workspaceToDom(Blockly.getMainWorkspace());
    copyToClipboard((new XMLSerializer()).serializeToString(CGX_save));
    $("#save").val((new XMLSerializer()).serializeToString(CGX_save));
});

$('#load_button').on('click',(event)=>{
    let workspace = Blockly.getMainWorkspace();
    workspace.clear();
    CGX_save=Blockly.Xml.textToDom($('#save').val());
    Blockly.Xml.domToWorkspace(CGX_save, workspace);
});

$('#run_button').on('click',(event)=>{
    Blockly.JavaScript.addReservedWords('code');
    var code = Blockly.Python.workspaceToCode(
      Blockly.getMainWorkspace());

    // var code = Blockly.JavaScript.workspaceToCode(workspace);
    // var myInterpreter = new Interpreter(code);
    // myInterpreter.run();
    $.ajax({
        type :'post',
        url: CGX_URL+"/exec",
        data: JSON.stringify({prog: code}),
        dataType: 'json',
        contentType: 'application/json',
        success: (data) => {
            CGX_output(data.output);
        },
        error: (data) => {
            console.log("can't get sites");
        }
    });
    
});
$('#show_button').on('click',(event)=>{
    Blockly.JavaScript.addReservedWords('code');
    var code = Blockly.Python.workspaceToCode(
      Blockly.getMainWorkspace());
    CGX_output(code);
});