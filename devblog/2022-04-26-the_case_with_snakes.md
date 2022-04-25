# devlog, 23.04.22

Mainly a restart of this project, with the concept of using opencv for detecting piece positions..

Also, this is now a python flask project!

# Start 

```bash
# runs flask app
./run.sh board-run

  # removes json caches
./run.sh board-clean 

```

## Register and play around

Head to the [dashboard](http://0.0.0.0:8031/tools/dashboard) and register some (the given?) bots.

Now you can filter bots.

```
state=online&piece=wk
```

## OpenCV

```bash
# run image detection
./run.sh ocv-detect  
# crop test images
./run.sh ocv-crop    
```

results in `./src/opencv_research/out`


## Robot `GET /` response content

```json
{
    "id":"herzbube",
    "motors":{
        "left":{
            "pins":{
                "pinA":"0",
                "pinB":"0",
                "pinPwm":"0"
            }
        },
        "right":{
            "pins":{
                "pinA":"0",
                "pinB":"0",
                "pinPwm":"0"
            }
        }
    },
    "piece":"wk",
    "position_image":"http://0.0.0.0:8031/tools/mockbot/01_position_image.png",
    "state":"online",
    "url":"http://0.0.0.0:8031/tools/mockbot/01"
}
```

## Robot `POST /register` payload

```json
["http://0.0.0.0:8037","http://0.0.0.0:8031/tools/mockbot"]
```


## Board paths

```bash
 > export FLASK_APP=flaskr
 > flask routes
Endpoint               Methods  Rule
---------------------  -------  -----------------------------------------------
bots.get_index         GET      /bots/
bots.post_register     POST     /bots/register
index                  GET      /
static                 GET      /static/<path:filename>
tools.board_print      GET      /tools/board_print
tools.dashboard        GET      /tools/dashboard
tools.mockbot          GET      /tools/mockbot/<string:name>
tools.mockbot_picture  GET      /tools/mockbot/<string:name>_position_image.png
```

## venv stuff
```bash
python3 -m venv venv
. venv/bin/activate # note the space behind the dot
```

### Parts

- https://www.fambach.net/esp32-cam-modul/

# Notes

- You need 5 bits to address each bot (31 => 11111).
- Yoou need 3 bits to address a piece name (6+1 => 111)
- With fieldsize 2000mm, you can have a piece diameter of 140mm ((2000 / 10) * 0.70) (0.75 would be touching, so 10% tolerance)
