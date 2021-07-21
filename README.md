## Video Listener

Upon receiving a GET request flask server responds with the _best_ image captured in a set time interval.

### To start:

1. Get all the dependancies with `pip3 install -r requirements.txt`
2. Configure the functionality using `config.json`
3. Run `python3 main.py` (Has to be ran in terminal/cmd)

#### Endpoints:

1. `localhost:5000/<int:cam_id>` to fetch best image in cameras[cam_id] buffer
2. `localhost:5000/cam_id=<int:cam_id>&req_time=<float:req_time>` similar to the previous req, but here the user specifies the exact time this request was send. This helps to adjust for delays.
3. Adding "/gif" to the end of previous 2 endpoints e.g. `localhost:5000/<int:cam_id>/gif` sends back a gif of the buffer.
4. `localhost:5000/<int:cam_id>/start/<int:item_code>` starts recording cam_id and stores best frame each second in `capturedFootage/item_code`
5. `localhost:5000/<int:cam_id>/stop/<int:item_code>` stops recording cam_id
