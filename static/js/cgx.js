$(document).ready(() => {
    $('#clear_button').button();
    $('#copyout_button').button();
    $('#save_button').button();
    $('#run_button').button();
    $('#load_button').button();
    $('#show_button').button();
    
    let workspace = Blockly.getMainWorkspace();
    workspace.clear();
    CGX_save=Blockly.Xml.textToDom('<xml xmlns="http://www.w3.org/1999/xhtml"><variables><variable type="" id="w6Z|M.J3UNMr92N%!PF/">element</variable></variables><block type="cgx_token" id="hzJ@#g(T;exkz@GE?_,f" x="116" y="50"><value name="TOKEN"><block type="text" id="MD2)Kuj-@c!a?cey#m0Y"><field name="TEXT">PASTE TOKEN HERE</field></block></value><next><block type="cgx_output" id="G%kCtGPGYb}47@3(0{*I"><value name="OUTPUT"><block type="text" id="`%;@Z6SK4`4UX/Jnim#g"><field name="TEXT">demo that will list all elements</field></block></value><next><block type="controls_forEach" id="kiA0~1w1l!A72`(DlOZV"><field name="VAR" id="w6Z|M.J3UNMr92N%!PF/" variabletype="">element</field><value name="LIST"><block type="cgx_get_object_list" id="Z8J`FP/dvCsEhAF8|Y5)"><field name="NAME">elements</field></block></value><statement name="DO"><block type="cgx_output" id="d-i4qTG5~v(h+MA4}@ur"><value name="OUTPUT"><block type="cgx_element_attribute" id="^i;;]2Z=PiMXwN@])n8u"><field name="FIELD">name</field><value name="ELEMENT"><block type="variables_get" id="S:Fx6T|3juEpP{UKBg?8"><field name="VAR" id="w6Z|M.J3UNMr92N%!PF/" variabletype="">element</field></block></value></block></value></block></statement></block></next></block></next></block></xml>');
    Blockly.Xml.domToWorkspace(CGX_save, workspace);
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
    if (CGX_blink_run) {
        $('#run_button').fadeOut(300);
        $('#run_button').fadeIn(600);
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