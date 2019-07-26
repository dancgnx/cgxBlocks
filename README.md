# cgxBlock

WARNING: USE AT YOUR OWN RISK

CloudGenix SDK using block progarmming.

## Versions
* 07/25/2019 - Initial release

## Instructions to install using python:

* Install python3
* Install cloudgenix python sdk : `pip3 install cloudgenix`
* If pip3 isn't install, please install it
* Install flask: `pip3 install Flask`
* Run the script: `python3 cgxBlocks.py`
* Point your browser to http://127.0.0.1:5000/


## Instructions to install using docker:

* Install docker https://www.docker.com/products/docker-desktop
* Open a terminal or cmd or powershell
* Run the following command: `docker run --rm -ti -p 127.0.0.1:5000:5000 dancgx/cgxblocks`
* *WARNING*: If you do not use the `127.0.0.1` in the above command, anyone will be able to connect to the container and execute any code they wish!
* Point your browser to http://127.0.0.1:5000/
* Don't forget to refresh the image for any updates: `docker image pull dancgx/cgxblocks`


## Generating python code and running it:
* If you press the show button, you will see the python code that will be executed when you click "run".
* To use that code, you will need to copy the cgxuax.py file to the directory from which you are running that code.

## Saveing and Loading:
* You can save the cgxBlocks program by clicking "Save" button. It will produce XML string that will be copied to your clipboard and also to the "Saved code:" text box.
* To load a program, clear the "Saved code:" text box and paste XML string into it and hit the "Load" button.
* WARNING: The XML will include the authentication TOKEN.

## Final note
This project using A LOT of code from: https://developers.google.com/blockly/ . Thank you *blockly* to make this happen!


ENJOY!
