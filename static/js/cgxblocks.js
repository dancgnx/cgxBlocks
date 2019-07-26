
// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#5jpbkb

// login block

Blockly.defineBlocksWithJsonArray([
    {
        "type": "cgx_token",
        "message0": "Set Auth Token %1",
        "args0": [
        {
            "type": "input_value",
            "name": "TOKEN"
        }
        ],
        "inputsInline": false,
        "nextStatement": null,
        "colour": 23,
        "tooltip": "insert authentication token here",
        "helpUrl": ""
    }
]);


Blockly.JavaScript['cgx_token'] = function(block) {
    var value_token = Blockly.JavaScript.valueToCode(block, 'TOKEN', Blockly.JavaScript.ORDER_ATOMIC);
    // TODO: Assemble JavaScript into code variable.
    var code = 'CGX_Login('+value_token+');\n';
    return code;
};

Blockly.Python['cgx_token'] = function(block) {
  var value_token = Blockly.Python.valueToCode(block, 'TOKEN', Blockly.Python.ORDER_ATOMIC);
  var code = 'cgx.setToken('+value_token+')\n';
  return code;
};
// output block
// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#8qshnh
Blockly.defineBlocksWithJsonArray([
    {
        "type": "cgx_output",
        "message0": "print %1",
        "args0": [
          {
            "type": "input_value",
            "name": "OUTPUT"
          }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 23,
        "tooltip": "output to console",
        "helpUrl": ""
      }
]);


Blockly.JavaScript['cgx_output'] = function(block) {
    var value_output = Blockly.JavaScript.valueToCode(block, 'OUTPUT', Blockly.JavaScript.ORDER_ATOMIC);
    // TODO: Assemble JavaScript into code variable.
    var code = 'CGX_output('+value_output+');\n';
    return code;
};

Blockly.Python['cgx_output'] = function(block) {
  var value_output = Blockly.Python.valueToCode(block, 'OUTPUT', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = 
  'cgx.output('+value_output+')\n';
  return code;
};


// sites block
// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#o6gtza

Blockly.defineBlocksWithJsonArray([
    {
        "type": "cgx_get_sites",
        "message0": "get sites",
        "output": "Array",
        "colour": 23,
        "tooltip": "get a list of sites",
        "helpUrl": ""
      }
]);

Blockly.JavaScript['cgx_get_sites'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = 'CGX_get_sites();\n';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.Python['cgx_get_sites'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = 
  'cgx.getSites()';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_FUNCTION_CALL];
};

// object attribute

Blockly.defineBlocksWithJsonArray([
  {
    "type": "cgx_site_attribute",
    "message0": "site %1 attribute %2",
    "args0": [
      {
        "type": "input_value",
        "name": "SITE"
      },
      {
        "type": "field_dropdown",
        "name": "FIELD",
        "options": [
          [
            "name",
            "name"
          ],
          [
            "admin_state",
            "admin_state"
          ],
          [
            "element_cluster_role",
            "element_cluster_role"
          ]
        ]
      }
    ],
    "output": null,
    "colour": 30,
    "tooltip": "get site attribute from site",
    "helpUrl": ""
  },
  {
    "type": "cgx_get_interface_attributes",
    "message0": "from interface %1 get attribute %2",
    "args0": [
      {
        "type": "input_value",
        "name": "ELEMENT"
      },
      {
        "type": "field_dropdown",
        "name": "NAME",
        "options": [
          [
            "name",
            "name"
          ],
          [
            "type",
            "type"
          ],
          [
            "admin_up",
            "admin_up"
          ],
          [
            "used_for",
            "used_for"
          ],
          [
            "IP address",
            "IP address"
          ],
          [
            "id",
            "id"
          ]
        ]
      }
    ],
    "output": null,
    "colour": 35,
    "tooltip": "",
    "helpUrl": "get attributes of interface object"
  },
  {
    "type": "cgx_element_attribute",
    "message0": "from element %1 get attribute %2",
    "args0": [
      {
        "type": "input_value",
        "name": "ELEMENT"
      },
      {
        "type": "field_dropdown",
        "name": "FIELD",
        "options": [
          [
            "name",
            "name"
          ],
          [
            "site_name",
            "site_name"
          ],
          [
            "model_name",
            "model_name"
          ],
          [
            "software_version",
            "software_version"
          ],
          [
            "serial_number",
            "serial_number"
          ]
        ]
      }
    ],
    "output": null,
    "colour": 30,
    "tooltip": "get element atrribute from an element",
    "helpUrl": ""
  }
]);

Blockly.Python['cgx_site_attribute'] = function(block) {
  var value_site = Blockly.Python.valueToCode(block, 'SITE', Blockly.Python.ORDER_ATOMIC);
  var dropdown_field = block.getFieldValue('FIELD');
  //var code = value_site+'["'+dropdown_field+'"]';
  var code = 'cgx.getItem(' + value_site + ',"' + dropdown_field + '")';
  return [code, Blockly.Python.ORDER_FUNCTION_CALL];
};
Blockly.Python['cgx_get_interface_attributes'] = function(block) {
  var dropdown_name = block.getFieldValue('NAME');
  var value_element = Blockly.Python.valueToCode(block, 'ELEMENT', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = 'cgx.getItem(' + value_element + ',"' + dropdown_name + '")';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_FUNCTION_CALL];
};
Blockly.Python['cgx_element_attribute'] = function(block) {
  var value_element = Blockly.Python.valueToCode(block, 'ELEMENT', Blockly.Python.ORDER_ATOMIC);
  var dropdown_field = block.getFieldValue('FIELD');
  //var code = value_site+'["'+dropdown_field+'"]';
  var code = 'cgx.getItem('+value_element+',"'+dropdown_field+'")';
  if (dropdown_field=="site_name") {
    var code = 'cgx.getSiteNameByID(cgx.getItem(' + value_element + ',"site_id"))';
  } else {
    var code = 'cgx.getItem(' + value_element + ',"' + dropdown_field + '")';
  }
  return [code, Blockly.Python.ORDER_NONE];
};


// list of objects

Blockly.defineBlocksWithJsonArray([
  {
    "type": "cgx_get_object_list",
    "message0": "get a list of all %1",
    "args0": [
      {
        "type": "field_dropdown",
        "name": "NAME",
        "options": [
          [
            "sites",
            "sites"
          ],
          [
            "elements",
            "elements"
          ],
          [
            "machines",
            "machines"
          ]
        ]
      }
    ],
    "output": "Array",
    "colour": 30,
    "tooltip": "get and cloudgenix object",
    "helpUrl": ""
  }
]);

Blockly.Python['cgx_get_object_list'] = function(block) {
  var dropdown_name = block.getFieldValue('NAME');
  // TODO: Assemble Python into code variable.
  var code = 'cgx.getObjectList("'+dropdown_name+'")';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_FUNCTION_CALL];
};

// element objects
Blockly.defineBlocksWithJsonArray([
  {
    "type": "cgx_get_elements_object_list",
    "message0": "get a list of %1 of element: %2",
    "args0": [
      {
        "type": "field_dropdown",
        "name": "OBJECT_NAME",
        "options": [
          [
            "interfaces",
            "interfaces"
          ],
          [
            "interfaces_status",
            "interfaces_status"
          ]
        ]
      },
      {
        "type": "input_value",
        "name": "NAME",
      }
    ],
    "output": "Array",
    "colour": 35,
    "tooltip": "get object list that belongs to an element",
    "helpUrl": ""
  }
]);

Blockly.Python['cgx_get_elements_object_list'] = function(block) {
  var dropdown_object_name = block.getFieldValue('OBJECT_NAME');
  var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = '...';
  if (dropdown_object_name=="interfaces") {
    code='cgx.getInterfacesByElement('+value_name+')';
  } else if (dropdown_object_name=="interfaces_status") {
    code = '[]';
  }
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_FUNCTION_CALL];
};

// interface -> ellemnt -> attributes

Blockly.defineBlocksWithJsonArray([
  {
    "type": "cgx_get_interface_element_attribute",
    "message0": "for interface %1 of element %2 get attribute %3",
    "args0": [
      {
        "type": "input_value",
        "name": "INTERFACE"
      },
      {
        "type": "input_value",
        "name": "ELEMENT"
      },
      {
        "type": "field_dropdown",
        "name": "ATTRIBUTE",
        "options": [
          [
            "IP Address",
            "IP Address"
          ]
        ]
      }
    ],
    "output": null,
    "colour": 30,
    "tooltip": "get attributes that needs",
    "helpUrl": ""
  }
]);


Blockly.Python['cgx_get_interface_element_attribute'] = function(block) {
  var value_interface = Blockly.Python.valueToCode(block, 'INTERFACE', Blockly.Python.ORDER_ATOMIC);
  var value_element = Blockly.Python.valueToCode(block, 'ELEMENT', Blockly.Python.ORDER_ATOMIC);
  var dropdown_attribute = block.getFieldValue('ATTRIBUTE');
  // TODO: Assemble Python into code variable.
  var code = '...';
  if (dropdown_attribute == "IP Address") {
    code = "cgx.getInterfacePublicIPAddress("+value_element+","+value_interface+")"
  }
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_FUNCTION_CALL];
};