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
    
    with io.BytesIO(base64.b64decode(picture)) as stream:
      self.tft.draw(stream, width, height)


hw = None

async def atk(dom):
  global hw

  if not hw:
    hw = ucuq.Multi(HW(await ucuq.ATKConnectAwait(dom, BODY)))
  else:
    await dom.inner("", BODY)

  await dom.executeVoid("Go();")


async def atkSmile(dom, id):
  await dom.disableElement(id)
  await dom.executeVoid("allowCamera();")


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

  await dom.executeVoid("document.getElementById('camera').close();document.getElementById('camera').remove();")


async def atkCameraCancel(dom):
  await dom.executeVoid("document.getElementById('camera').close()")
  await dom.enableElement("Smile")


async def atkShoot(dom):
  # 'dom.executeStrings(…)' does not work with Google Chrome.
  # width, height, picture = await dom.executeStrings("takePicture();")

  # result = await dom.executeString("takePicture();")

  await dom.executeVoid("takePicture();")


async def atkDisplay(dom):
  result = ""

  while True:
    partial = await dom.executeString("getNextChunk(25000);")

    if not partial:
      break

    result += partial

  width, height, picture = result.split(',')
  hw.draw(picture, int(width), int(height))


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

  function display(canvas, w, h) {
    let base64rgb565 = canvasToRGB565Base64(canvas);
    picture = w + "," + h + "," + base64rgb565;
    console.log(picture);
    globalConsumeIndex = 0;
    launchEvent(`dummy|BUTTON|click||(Display)`);
  }

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

    document.getElementById('fileInput').addEventListener('change', function () {
      let file = this.files[0];
      const img = new Image();

      img.onload = function () {
        resizeImage(img, 240, 320, 0)
      };

      img.src = URL.createObjectURL(file);
    });
  }

  function allowCamera() {
    navigator.mediaDevices
      .getUserMedia({ video: true, audio: false })
      .then((stream) => {
        navigator.mediaDevices.enumerateDevices()
          .then(function (devices) {
            const cameras = devices.filter(device => device.kind === 'videoinput');
            launchEvent(`${btoa(unescape(encodeURIComponent(JSON.stringify(cameras))))}|BUTTON|click||(Camera)`);
          })
          .catch(function (err) {
            console.error(err.name + ": " + err.message);
          });
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

  var picture = "";
  var globalConsumeIndex = 0;

  function getNextChunk(chunkSize) {
    if (!picture || chunkSize <= 0) {
      return "";
    }

    if (globalConsumeIndex >= picture.length) {
      return "";
    }

    const chunk = picture.substring(globalConsumeIndex, globalConsumeIndex + chunkSize);

    globalConsumeIndex += chunk.length;

    return chunk;
  }

  function takePicture() {
    const context = canvas.getContext("2d");
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);

      const data = canvas.toDataURL("image/png");

      photo.onload = function () {
        resizeImage(photo, 240, 320, 0, display);
      };

      photo.src = data;
    } else {
      clearPhoto();
    }
  }

  function resizeImage(img, maxWidth, maxHeight, rotateAngleDeg, callback) {
    let needRotate = img.width > img.height;
    let origW = img.width, origH = img.height;
    let width, height, rad = 0;

    if (needRotate) {
      rad = Math.PI / 2;
      let scale = Math.min(maxWidth / origH, maxHeight / origW, 1);
      width = Math.round(origW * scale);
      height = Math.round(origH * scale);

      canvasW = height;
      canvasH = width;
    } else {
      let scale = Math.min(maxWidth / origW, maxHeight / origH, 1);
      width = Math.round(origW * scale);
      height = Math.round(origH * scale);
      canvasW = width;
      canvasH = height;
    }

    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');
    canvas.width = canvasW;
    canvas.height = canvasH;
    ctx.translate(canvasW / 2, canvasH / 2);
    if (needRotate) ctx.rotate(rad);
    ctx.drawImage(
      img,
      -width / 2,
      -height / 2,
      width,
      height
    );
    display(canvas, canvas.width, canvas.height);
  }

  function canvasToRGB565Base64(canvas) {
    let ctx = canvas.getContext("2d");
    let imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    let data = imgData.data;
    let rgb565 = new Uint8Array(canvas.width * canvas.height * 2);
    for (let i = 0, j = 0; i < data.length; i += 4, j += 2) {
      let r = data[i] >> 3;
      let g = data[i + 1] >> 2;
      let b = data[i + 2] >> 3;
      let val = (r << 11) | (g << 5) | b;
      rgb565[j] = val >> 8;
      rgb565[j + 1] = val & 0xFF;
    }

    /* stack overflow with chrome !!! */
    /* return btoa(String.fromCharCode.apply(null, rgb565)); */

    converted = "";
    rgb565.forEach(function(byte) {converted += String.fromCharCode(byte)});
    return btoa(converted);
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
  <legend xdh:onevent="dblclick|UCUqXDevice">TFT</legend>
  <span>
    <div style="display: flex; justify-content: center; gap: 1rem;">
    <button xdh:onevent="Test">Test</button>
    <button id="Smile" xdh:onevent="Smile">Smile!!!</button>
    </div>
    <div style="justify-content: end;">
    <input type="file" id="fileInput">
    </div>
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
  <output id="Picture" style="display: none;"></output>
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

