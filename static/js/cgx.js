$(document).ready(() => {
    $('#clear_button').button();
    $('#copyout_button').button();
    $('#save_button').button();
    $('#run_button').button();
    $('#load_button').button();
    $('#show_button').button();
});


var CGX_URL="http://127.0.0.1:5000";
var CGX_save;
var CGX_resp;
var CGX_blink_run = false;

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
// var resp;

$('#clear_button').on('click',(event)=>{
    $("#output").val("");
});

$('#copyout_button').on('click',(event)=>{
    copyToClipboard($("#output").val());
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

function blink_run() {
    $('#run_button').fadeOut(300);
    $('#run_button').fadeIn(600);
    if (CGX_blink_run) {
        setTimeout(blink_run,900)
    }
}
$('#run_button').on('click',(event)=>{
    CGX_blink_run = true;
    blink_run();
    Blockly.JavaScript.addReservedWords('code');
    var code = Blockly.Python.workspaceToCode(
      Blockly.getMainWorkspace());

    $.ajax({
        type :'post',
        url: CGX_URL+"/exec",
        data: JSON.stringify({prog: code}),
        dataType: 'json',
        contentType: 'application/json',
        success: (data) => {
            CGX_output(data.output);
            CGX_blink_run = false;
        },
        error: (data) => {
            console.log("Error exec script");
            CGX_output("ERROR RUNNING CODE");
            CGX_blink_run = false;
        }
    });
    
});
$('#show_button').on('click',(event)=>{
    Blockly.JavaScript.addReservedWords('code');
    var code = Blockly.Python.workspaceToCode(
      Blockly.getMainWorkspace());
    code = "import cloudgenix \nimport cgxaux\n\n" + code;
    CGX_output(code);
});