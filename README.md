# python package -- vs2020

Provide `vs2020-sentinel` that control the program `VisualStage 2020`.
These commands enable users to develop a program by talking to `VisualStage 2020`. 

The command `vs2020-sentinel` is for control `VisualStage 2020` via network.

# Dependency

## VisualStage 2020 for Windows

YY confirmed this work with VisualStage Version 1.2.2.0.

## [Python 3.7 for Windows](https://www.python.org/downloads/windows/)

Include "C:\Python37\;C:\Python37\Scripts\" in %PATH%.

# Installation

Install this package as Administrator as:

    ADMIN.CMD> pip install git+https://gitlab.misasa.okayama-u.ac.jp/pythonpackage/vs2020/-/archive/master/vs2020-master.zip

or download [vs2020-master.zip](https://gitlab.misasa.okayama-u.ac.jp/pythonpackage/vs2020/-/archive/master/vs2020-master.zip) to a local directory and install it as Administrator as:

    $ cd ~/Downloads/
    $ wget https://gitlab.misasa.okayama-u.ac.jp/pythonpackage/vs2020/-/archive/master/vs2020-master.zip
    ADMIN.CMD> cd %USERPROFILE%\Downloads\
    ADMIN.CMD> pip list
    ADMIN.CMD> pip uninstall vs2020
    ADMIN.CMD> pip install vs2020-master.zip

Successful installation is confirmed by:

    CMD> vs2020-sentinel --help

# Commands

Commands are summarized as:

| command | description                       | note |
| ------- | --------------------------------- | ---- |
| vs2020-sentinel  | Control VisualStage 2020 via network |      |


# Usage

See online document with option `--help`.

# Control a stage from remote

Start VisualStage2020 and lunch vs2020-sentinel as shown below. Revise configuration file (~/.vs2020rc) when necessary.

    > vs2020-sentinel
    reading |C:\Users\SEM\.vs2020rc| ...
    2022-01-27 16:28:14,345 INFO:version 0.0.1
    2022-01-27 16:28:14,345 INFO:connecting database.misasa.okayama-u.ac.jp:1883
    2022-01-27 16:28:14,365 INFO:Connected with result code 0
    2022-01-27 16:28:14,365 INFO:subscribe topic |stage/ctrl/stage-of-5fBX60| to receive stage control command...
    2022-01-27 16:28:15,474 INFO:connecting stage controller...
    2022-01-27 16:28:15,474 INFO:starting thread_position...
    2022-01-27 16:28:15,474 INFO:publish message {"isStageConnected": "false", "isVSRunning": "true", "isAPIAvailable": "true", "isStageMoving": "false", "dataname": "", "updated_at": "2022-01-27T16:28:15"} on topic stage/status/stage-of-5fBX6
    2022-01-27 16:28:15,484 INFO:POSITION -> POSITION SUCCESS,-338.86148,471.68106 (response: 0.01 sec) in position
    2022-01-27 16:28:15,494 INFO:publish message {"x_world": "-338.86148", "y_world": "471.68106", "updated_at": "2022-01-27T16:28:15"} on topic stage/position/stage-of-5fBX60
    2022-01-27 16:28:15,494 INFO:publish message {"command": "POSITION", "output": "POSITION SUCCESS,-338.86148,471.68106", "response": 0.010000228881835938, "updated_at": "2022-01-27T16:28:15"} on topic stage/info/stage-of-5fBX60
    2022-01-27 16:28:16,475 INFO:publish message {"isStageConnected": "true", "isVSRunning": "true", "isAPIAvailable": "true", "isStageMoving": "false", "dataname": "", "updated_at": "2022-01-27T16:28:16"} on topic stage/status/stage-of-5fBX60
    2022-01-27 16:28:16,495 INFO:POSITION -> POSITION SUCCESS,-338.86148,471.68106 (response: 0.00 sec) in position
    2022-01-27 16:28:16,495 INFO:publish message {"x_world": "-338.86148", "y_world": "471.68106", "updated_at": "2022-01-27T16:28:16"} on topic stage/position/stage-of-5fBX60
    2022-01-27 16:28:16,495 INFO:publish message {"command": "POSITION", "output": "POSITION SUCCESS,-338.86148,471.68106", "response": 0.0, "updated_at": "2022-01-27T16:28:16"} on topic stage/info/stage-of-5fBX60
    2022-01-27 16:28:17,475 INFO:publish message {"isStageConnected": "true", "isVSRunning": "true", "isAPIAvailable": "true", "isStageMoving": "false", "dataname": "", "updated_at": "2022-01-27T16:28:17"} on topic stage/status/stage-of-5fBX60
    2022-01-27 16:28:17,495 INFO:POSITION -> POSITION SUCCESS,-338.86148,471.68106 (response: 0.00 sec) in position
    2022-01-27 16:28:17,495 INFO:publish message {"x_world": "-338.86148", "y_world": "471.68106", "updated_at": "2022-01-27T16:28:17"} on topic stage/position/stage-of-5fBX60
    2022-01-27 16:28:17,495 INFO:publish message {"command": "POSITION", "output": "POSITION SUCCESS,-338.86148,471.68106", "response": 0.0, "updated_at": "2022-01-27T16:28:17"} on topic stage/info/stage-of-5fBX60
    ....

### Example of configuration file

    > cat ~/.vs2020rc
    ---
    stage_name: stage-of-sisyphus-THINK
    timeout: 8000
    vsdata_path: Z:\
    world_origin: ld
    stage_origin: ru
    
### control via web browser
Access [machine list](https://database.misasa.okayama-u.ac.jp/machine/) and open an [Edit Machine (ex. SIMS-1280)](https://database.misasa.okayama-u.ac.jp/machine/machines/3/edit) for the machine you want to control (by clicking the gear icon next to the machine name on the list).
Input the stage name (for example `stage-of-sisyphus-THINK`) and click OK.
Then you can see the XY position of the stage on web browser in real time.

### control via command line
Download and install a MQTT client software [mosquitto](http://mosquitto.org/download/)
To receive current position (and status) of `stage-of-sisyphus-THINK`, issue following command. 

    > mosquitto_sub -h database.misasa.okayama-u.ac.jp -t stage/info/stage-of-sisyphus-THINK

In order to move the stage `stage-of-sisyphus-THINK` to the specified position (for example [0.0, 0.0]), issue following command.

    > mosquitto_pub -h database.misasa.okayama-u.ac.jp -t stage/ctrl/stage-of-sisyphus-THINK -m "{\"command\":\"GOTO\",\"d_x\":\"0.0\",\"d_y\":\"0.0\"}"