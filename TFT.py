import ucuq, base64, io, atlastk, json

class HW:
  def __init__(self, infos, device=None):
    self.device, self.tft = ucuq.getBits(infos, ucuq.B_TFT, device=device)

    if self.tft:
      pin, = ucuq.getHardware(infos, ucuq.B_TFT, ["Backlight"])
      ucuq.GPIO(pin, device=device).high()

  def __getattr__(self, methodName):
    def wrapper(*args, **kwargs):
      getattr(self.tft, methodName)(*args, **kwargs)
      return self
    return wrapper
  
  def sleep(self, delay = 0.75):
    self.device.sleep(delay)

  def draw(self, picture, width, height):
    self.tft.clear()
    self.tft.draw(picture, width, height)


hw = None

async def atk(dom):
  global hw

  if not hw:
    hw = ucuq.Multi(HW(await ucuq.ATKConnectAwait(dom, BODY)))
  else:
    await dom.inner("", BODY)


async def atkSmile(dom, id):
  await dom.disableElement(id)
  await dom.executeVoid("Go();allowCamera();")


async def atkCamera(dom, id):
  cameras = json.loads(base64.b64decode(id).decode('utf-8'))

  html = ""

  for camera in cameras:
    html += f'<option value="{camera["deviceId"]}">{camera["label"]}</option>'

  await dom.inner("cameras", html)
  await dom.executeVoid("document.getElementById('camera').showModal();")


async def atkCameraOk(dom):
  deviceId = await dom.getValue("cameras")
  if deviceId:
    await dom.executeVoid(f"launchCamera('{deviceId}');")
    await dom.disableElement("HidePhoto")
  else:
    await dom.enableElement("Smile")

  await dom.executeVoid("document.getElementById('camera').close().remove();")


async def atkCameraCancel(dom):
  await dom.executeVoid("document.getElementById('camera').close()")
  await dom.enableElement("Smile")


async def atkShoot(dom):
  await dom.executeVoid("takePicture();")
  width, height, picture = await dom.executeStrings("resizeCanvasAndConvertToRGB565Base64(canvas)")
  hw.draw(io.BytesIO(base64.b64decode(picture)), int(width), int(height))


async def atkTest(dom):
  test()

def test():
  hw.clear((0,0,255))
  hw.sleep()

  hw.clear()

  hw.hline(10, 309, 229, (255, 0, 255))
  hw.sleep()

  hw.vline(10, 0, 309, (0, 255, 255))
  hw.sleep()

  hw.rect(23, 50, 30, 75, (255, 255, 0))
  hw.sleep()

  hw.rect(23, 50, 75, 30, (0, 255, 255), fill=False)
  hw.sleep()

  hw.line(127, 0, 64, 127, (255, 0, 0))
  hw.sleep()

  coords = [[200, 163], [78, 80], [122, 92], [50, 50], [78, 15], [200, 163]]
  hw.lines(coords, (0, 255, 0))
  hw.sleep()

  hw.clear()

  hw.poly(5, 120, 286, 30, (0, 64, 255), rotate=15, fill=False)
  hw.sleep()

  hw.poly(9, 180, 186, 40, (255, 64, 0), rotate=15)
  hw.sleep()

  hw.clear()
  hw.circle(132, 132, 70, (0, 255, 0))
  hw.sleep()

  hw.circle(132, 96, 70, (0, 0, 255), fill=False)
  hw.sleep()

  hw.ellipse(96, 96, 30, 16, (255, 0, 0))
  hw.sleep()

  hw.ellipse(96, 256, 16, 30, (255, 255, 0), fill=False)
  hw.sleep()

  hw.text(100, 100, "Hello World!", (255, 255, 255), (0, 0, 0), rotate=90)

async def UCUqXDevice(dom, device):
  hw.add(HW(await ucuq.getInfosAwait(device), device))

ATK_HEAD = """
<style>
  button {
    display: block;
    margin-block: 1rem;
  }

  .camera>button {
    position: relative;
    margin: auto;
    bottom: 32px;
    background-color: rgb(0 150 0 / 50%);
    border: 1px solid rgb(255 255 255 / 70%);
    box-shadow: 0px 0px 1px 2px rgb(0 0 0 / 20%);
    font-size: 14px;
    color: rgb(255 255 255 / 100%);
  }

  #video,
  #photo {
    border: 1px solid black;
    box-shadow: 2px 2px 3px black;
    width: 100%;
    height: auto;
  }

  #canvas {
    display: none;
  }

  .camera,
  .output {
    display: inline-block;
    width: 49%;
    height: auto;
  }

  .output {
    vertical-align: top;
  }

  code {
    background-color: lightgrey;
  }
</style>
<script>

  const width = 320;
  let height = 0;

  let streaming = false;

  var video;
  var canvas;
  var photo;
  var startButton;
  var allowButton;

  function Go() {
    video = document.getElementById("video");
    canvas = document.getElementById("canvas");
    photo = document.getElementById("photo");
    video.addEventListener(
      "canplay",
      (ev) => {
        if (!streaming) {
          height = video.videoHeight / (video.videoWidth / width);

          video.setAttribute("width", width);
          video.setAttribute("height", height);
          canvas.setAttribute("width", width);
          canvas.setAttribute("height", height);
          streaming = true;
        }
      },
      false,
    );
  }

  function allowCamera() {
    navigator.mediaDevices
      .getUserMedia({ video: true, audio: false })
      .then((stream) => {
        navigator.mediaDevices.enumerateDevices()
          .then(function (devices) {
            const cameras = devices.filter(device => device.kind === 'videoinput');
            console.log(cameras);
            cameras.forEach(function (camera, index) {
              console.log(`Camera ${index}: label="${camera.label}", id=${camera.deviceId}`);
            });
            launchEvent(`${btoa(unescape(encodeURIComponent(JSON.stringify(cameras))))}|BUTTON|click||(Camera)`);
          })
          .catch(function (err) {
            console.error(err.name + ": " + err.message);
          });
      })
      .catch((err) => {
        console.error(`An error occurred: ${err}`);
      });

    return;

    navigator.mediaDevices.enumerateDevices()
      .then(function (devices) {
        const cameras = devices.filter(device => device.kind === 'videoinput');
        cameras.forEach(function (camera, index) {
          console.log(`Camera ${index}: label="${camera.label}", id=${camera.deviceId}`);
        });
      })
      .catch(function (err) {
        console.error(err.name + ": " + err.message);
      });


    navigator.mediaDevices
      .getUserMedia({ video: true, audio: false })
      .then((stream) => {
        video.srcObject = stream;
        video.play();
      })
      .catch((err) => {
        console.error(`An error occurred: ${err}`);
      });
  }

  function launchCamera(id) {
    navigator.mediaDevices.getUserMedia({
      video: { deviceId: { exact: id } }
    }).then(function (stream) {
        video.srcObject = stream;
        video.play();
    }).catch(function (err) {
      console.error("Erreur d'accès caméra :", err);
    });
  }


  function clearPhoto() {
    const context = canvas.getContext("2d");
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    const data = canvas.toDataURL("image/png");
    photo.setAttribute("src", data);
  }

  clearPhoto();

  function resizeCanvasImageToJPEG(canvas, maxWidth = 240, maxHeight = 320, quality = 0.92) {
    const ctx = canvas.getContext('2d');
    const originalWidth = canvas.width;
    const originalHeight = canvas.height;

    const scaleWidth = maxWidth / originalWidth;
    const scaleHeight = maxHeight / originalHeight;
    const scale = Math.min(scaleWidth, scaleHeight, 1);

    const newWidth = Math.floor(originalWidth * scale);
    const newHeight = Math.floor(originalHeight * scale);

    const resizedCanvas = document.createElement('canvas');
    resizedCanvas.width = newWidth;
    resizedCanvas.height = newHeight;
    const resizedCtx = resizedCanvas.getContext('2d');

    resizedCtx.drawImage(canvas, 0, 0, originalWidth, originalHeight, 0, 0, newWidth, newHeight);

    const jpegDataURL = resizedCanvas.toDataURL('image/jpeg', quality);

    return jpegDataURL;
  }

  function resizeCanvasAndConvertToRGB565Base64(originalCanvas, maxWidth = 240, maxHeight = 320) {
    const originalWidth = originalCanvas.width;
    const originalHeight = originalCanvas.height;
    const scale = Math.min(maxWidth / originalWidth, maxHeight / originalHeight, 1);
    const newWidth = Math.floor(originalWidth * scale);
    const newHeight = Math.floor(originalHeight * scale);

    const resizedCanvas = document.createElement('canvas');
    resizedCanvas.width = newWidth;
    resizedCanvas.height = newHeight;
    const ctx = resizedCanvas.getContext('2d');

    ctx.drawImage(originalCanvas, 0, 0, originalWidth, originalHeight, 0, 0, newWidth, newHeight);

    const imageData = ctx.getImageData(0, 0, newWidth, newHeight);
    const pixels = imageData.data;

    const rgb565Buffer = new Uint8Array(newWidth * newHeight * 2);
    let offset = 0;
    for (let i = 0; i < pixels.length; i += 4) {
      const r = pixels[i];
      const g = pixels[i + 1];
      const b = pixels[i + 2];

      const r5 = (r >> 3) & 0x1F;
      const g6 = (g >> 2) & 0x3F;
      const b5 = (b >> 3) & 0x1F;
      const rgb565 = (r5 << 11) | (g6 << 5) | b5;

      rgb565Buffer[offset++] = (rgb565 >> 8) & 0xFF;
      rgb565Buffer[offset++] = rgb565 & 0xFF;
    }

    function uint8ToBase64(u8Arr) {
      let binary = '';
      for (let i = 0; i < u8Arr.length; i++) {
        binary += String.fromCharCode(u8Arr[i]);
      }
      return btoa(binary);
    }

    const base64String = uint8ToBase64(rgb565Buffer);

    return `"${newWidth}","${newHeight}","${base64String}"`;
  }


  function takePicture() {
    const context = canvas.getContext("2d");
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);

      /*    const data = canvas.toDataURL("image/png"); */
      const data = resizeCanvasImageToJPEG(canvas, 240, 320, 0.92);

      photo.setAttribute("src", data);
    } else {
      clearPhoto();
    }
  }
</script>
<style id="HidePhoto">
  .photo {
    display: none;
  }
</style>
"""

BODY = """
<fieldset>
  <legend xdh:onevent="UCUqXDevice">TFT</legend>
  <span style="display: flex; justify-content: center; gap: 1rem;">
    <button xdh:onevent="Test">Test</button>
    <button id="Smile" xdh:onevent="Smile">Smile!!!</button>
  </span>
  <span class="photo">
    <div class="camera">
      <video id="video">Video stream not available.</video>
      <button xdh:onevent="Shoot">Capture photo</button>
    </div>
    <canvas id="canvas"></canvas>
    <div class="output">
      <img id="photo" alt="The screen capture will appear in this box." />
    </div>
  </span>
</fieldset>
<dialog id="camera">
  <select id="cameras">
  </select>
  <span style="display: flex; justify-content: center; gap: 1rem;">
    <button xdh:onevent="CameraOk">OK</button>
    <button xdh:onevent="CameraCancel">Cancel</button>
  </span>
</dialog>
"""

atlastk.launch(globals=globals())

