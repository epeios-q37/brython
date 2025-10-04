import atlastk, ucuq, datetime, json

epaper = None

W_QRC_TEXT = "QRCText"

W_TXT_TEXT = "TXTText"
W_TXT_WIDTH = "TXTWidth"
W_TXT_X = "TXTX"
W_TXT_Y = "TXTY"
W_TXT_FONT_SIZE = "TXTFontSize"
W_TXT_FONT = "TXTFont"
W_TXT_CENTER_X = "TXTCenterX"
W_TXT_CENTER_Y = "TXTCenterY"
W_TXT_CANVAS = "TXTCanvas"

async def txtUpdate(dom):
  text, x, y, width, font, fontSize, centerX, centerY = (await dom.getValues((W_TXT_TEXT, W_TXT_X, W_TXT_Y, W_TXT_WIDTH, W_TXT_FONT, W_TXT_FONT_SIZE, W_TXT_CENTER_X, W_TXT_CENTER_Y))).values()

  coords = json.loads(await dom.executeString(f"JSON.stringify(createTextCanvas('{W_TXT_CANVAS}','{text}', {x}, {y}, {width}, \"{font}\", {fontSize}, {centerX}, {centerY}));"))

  values = {W_TXT_X: coords['x'], W_TXT_Y: coords['y']}

  if centerX != "true":
    del values[W_TXT_X]
    
  if centerY != "true":
    del values[W_TXT_Y]

  if values:
    await dom.setValues(values)


async def atk(dom):
  global epaper

  await ucuq.ATKConnectAwait(dom, BODY)

  epaper = ucuq.SSD1680_SPI(7, 1, 2, 3, ucuq.SPI(1, baudrate=2000000, polarity=0, phase=0, sck=4, mosi=6))
  epaper.fill(0).hText("E-paper ready !", 50).hText(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 75).show()

  await dom.focus(W_QRC_TEXT)
  await txtUpdate(dom)


# Called from JS!
async def atkDisplay(dom, data):
  image = json.loads(data)

  epaper.fill(0).draw(image["pattern"], width = image['width'], ox = image['offsetX'], oy = image['offsetY'], mul = image['mul']).show()


async def atkQRCSubmit(dom):
  await dom.executeVoid(f"QRCodeLaunch('{await dom.getValue(W_QRC_TEXT)}')")
  await dom.focus(W_QRC_TEXT)


async def atkQRCClear(dom):
  await dom.setValue(W_QRC_TEXT, "")
  await dom.focus(W_QRC_TEXT)


async def atkTXTUpdate(dom):
  await txtUpdate(dom)


async def atkTXTSubmit(dom):
  text, x, y, width, font, fontSize, centerX, centerY = (await dom.getValues((W_TXT_TEXT, W_TXT_X, W_TXT_Y, W_TXT_WIDTH, W_TXT_FONT, W_TXT_FONT_SIZE, W_TXT_CENTER_X, W_TXT_CENTER_Y))).values()

  await dom.executeVoid(f"displayText('{W_TXT_CANVAS}','{text}', {x}, {y}, {width}, \"{font}\", {fontSize}, {centerX}, {centerY})")


async def atkTXTClear(dom):
  await dom.setValue(W_TXT_TEXT, "")


async def atkTXTCenterX(dom, id):
  if ( ( await dom.getValue(id) ) == "true"):
    await dom.disableElement(W_TXT_X)
    await txtUpdate(dom)
  else:
    await dom.enableElement(W_TXT_X)


async def atkTXTCenterY(dom, id):
  if ( ( await dom.getValue(id) ) == "true"):
    await dom.disableElement(W_TXT_Y)
    await txtUpdate(dom)
  else:
    await dom.enableElement(W_TXT_Y)


async def atkReset(dom, id):
  global epaper
  epaper = ucuq.SSD1680_SPI(7, 1, 2, 3, ucuq.SPI(1, baudrate=2000000, polarity=0, phase=0, sck=4, mosi=6)).fill(0).show()

ATK_HEAD = """
<script>
  function getHexBitmap(canvas) {
    let ctx = canvas.getContext("2d");
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const pixels = imageData.data;

    const binaryPixels = [];
    for (let i = 0; i < pixels.length; i += 4) {
      const r = pixels[i];
      const g = pixels[i + 1];
      const b = pixels[i + 2];
      const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
      binaryPixels.push(luminance < 128 ? 1 : 0);
    }

    if (canvas.width % 4 !== 0) {
      throw new Error("QR code width is not a multiple of 4 pixels.");
    }

    let hexString = "";
    for (let i = 0; i < binaryPixels.length; i += 4) {
      let val = 0;
      for (let j = 0; j < 4; j++) {
        val |= (binaryPixels[i + j] << (3 - j));
      }
      hexString += val.toString(16);
    }

    return hexString;
  }

  async function QRCodeGenerate(data) {
    const url = `https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=${encodeURIComponent(data)}`;
    const img = new Image();
    img.crossOrigin = "Anonymous";

    const imageLoadPromise = new Promise((resolve, reject) => {
      img.onload = () => resolve();
      img.onerror = reject;
    });
    img.src = url;
    await imageLoadPromise;

    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);

    return getHexBitmap(canvas);
  }

  function QRCodeLaunch(text) {
    QRCodeGenerate(text)
      .then(hexString => {
        image = {
          pattern: hexString,
          width: 120,
          offsetX: 60,
          offsetY: 6,
          mul: 1
        };

        launchEvent(`${JSON.stringify(image)}|BUTTON|click||(Display)`);
      })
      .catch(e => console.error(e));
  }


  function getCenteredTextCoordinates(ctx, text, canvasWidth, canvasHeight, maxWidth) {
    const metrics = ctx.measureText(text);

    const ascent = metrics.actualBoundingBoxAscent || 0;
    const descent = metrics.actualBoundingBoxDescent || 0;
    const fullWidth = metrics.width;
    const textHeight = ascent + descent;
    const textWidth = Math.min(fullWidth, maxWidth);

    ctx.textAlign = 'start';

    const x = Math.floor(Math.max((canvasWidth - textWidth) / 2, 0));

    const y = Math.floor((canvasHeight / 2) + (ascent - textHeight / 2));

    return { x, y };
  }



  function createTextCanvas(canvasId, text, x, y, width, font, fontSize, centerX, centerY) {
    canvas = document.getElementById(canvasId);

    const ctx = canvas.getContext('2d');

    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    /* const fontSize = Math.floor(height * 0.6); */
    ctx.font = `${fontSize}px ${font}`;

    ctx.textAlign = 'left';
    ctx.textBaseline = 'bottom';

    ctx.fillStyle = 'black';

    let centeredX = 0, centeredY = 0;

    const centeredCoords = getCenteredTextCoordinates(ctx, text, canvas.width, canvas.height, width);

    x = centerX ? centeredCoords['x'] : x;
    y = centerY ? centeredCoords['y'] : y;

    ctx.fillText(text, x, y, width);

    return { x, y };
  }


  function displayText(canvasId, text, x, y, width, font, fontSize, coeff, centerX, centerY) {
    canvas = document.getElementById(canvasId);

    image = {
      pattern: getHexBitmap(canvas),
      width: canvas.width,
      offsetX: 0,
      offsetY: 0,
      mul: 1
    };

    launchEvent(`${JSON.stringify(image)}|BUTTON|click||(Display)`);
  }

</script>
"""

BODY = """
<fieldset>
  <legend>E-paper</legend>
  <fieldset>
    <legend>QR code</legend>
    <input id="QRCText" xdh:onevent="QRCSubmit" type="text" style="width: 100%" placeholder="Text to convert"
      value="https://q37.info/ucuq/">
    <div style="display: flex; justify-content: space-around; padding-top: 10px;">
      <button xdh:onevent="QRCSubmit">Submit</button>
      <button xdh:onevent="QRCClear">Clear</button>
    </div>
  </fieldset>
  <fieldset style="display: flex; flex-direction: column; row-gap: 5px; justify-content: space-around;">
    <legend>Text</legend>
    <input id="TXTText" xdh:onevents="(TXTSubmit)(input|TXTUpdate)" type="text" value="Hello World!">
    <span style="display: flex; justify-content: space-around">
      <span style="display: flex; flex-direction: column; row-gap: 5px;">
        <span style="display: flex; flex-direction: row; justify-content: space-between;">
          <label style="display: flex;">
            <span>↔: </span>
            <input type="checkbox" id="TXTCenterX" xdh:onevent="TXTCenterX" checked>
          </label>
          <label style="display: flex; align-items: baseline;">
            <span>↕: </span>
            <input type="checkbox" id="TXTCenterY" xdh:onevent="TXTCenterY" checked>
          </label>
        </span>
        <label style="display: flex; justify-content: space-between; width: 100%;">
          <span>X:&nbsp;</span>
          <input id="TXTX" xdh:onevent="input|TXTUpdate" type="number" min="0" max="250" value="0" disabled>
        </label>
      </span>
      <span style="display: flex; flex-direction: column; row-gap: 5px;">
        <label style="display: flex; justify-content: space-between; width: 100%;">
          <span>Width:&nbsp;</span>
          <input id="TXTWidth" xdh:onevent="input|TXTUpdate" type="number" min="8" max="248" value="248">
        </label> <label style="display: flex; justify-content: space-between; width: 100%;">
          <span>Y:&nbsp;</span>
          <input id="TXTY" xdh:onevent="input|TXTUpdate" type="number" min="0" max="122" value="0" disabled>
        </label>

      </span>
    </span>
    <span>
      <label>Font:
        <select id="TXTFont" xdh:onevent="TXTUpdate">
          <option value="Arial, sans-serif" style="font-family:Arial, sans-serif;">Arial</option>
          <option value="Verdana, sans-serif" style="font-family:Verdana, sans-serif;">Verdana</option>
          <option value="Tahoma, sans-serif" style="font-family:Tahoma, sans-serif;">Tahoma</option>
          <option value="Trebuchet MS, sans-serif" style="font-family:'Trebuchet MS', sans-serif;">Trebuchet MS</option>
          <option value="Times New Roman, serif" style="font-family:'Times New Roman', serif;">Times New Roman</option>
          <option value="Georgia, serif" style="font-family:Georgia, serif;">Georgia</option>
          <option value="Garamond, serif" style="font-family:Garamond, serif;">Garamond</option>
          <option value="Courier New, monospace" style="font-family:'Courier New', monospace;">Courier New</option>
          <option value="Lucida Console, monospace" style="font-family:'Lucida Console', monospace;">Lucida Console
          </option>
          <option value="Comic Sans MS, cursive, sans-serif" style="font-family:'Comic Sans MS', cursive, sans-serif;">
            Comic Sans MS</option>
          <option value="Impact, Charcoal, sans-serif" style="font-family:Impact, Charcoal, sans-serif;">Impact</option>
          <option value="Palatino Linotype, Book Antiqua, Palatino, serif"
            style="font-family:'Palatino Linotype', 'Book Antiqua', Palatino, serif;">Palatino Linotype</option>
          <option value="Segoe UI, sans-serif" style="font-family:'Segoe UI', sans-serif;">Segoe UI</option>
          <option value="Calibri, sans-serif" style="font-family:Calibri, sans-serif;">Calibri</option>
          <option value="Cambria, serif" style="font-family:Cambria, serif;">Cambria</option>
          <option value="Optima, sans-serif" style="font-family:Optima, sans-serif;">Optima</option>
          <option value="serif" style="font-family:serif;">Serif (générique)</option>
          <option value="monospace" style="font-family:monospace;">Monospace (générique)</option>
          <option value="cursive" style="font-family:cursive;">Cursive (générique)</option>
          <option value="fantasy" style="font-family:fantasy;">Fantasy (générique)</option>
        </select>
      </label>
      <input id="TXTFontSize" xdh:onevent="input|TXTUpdate" type="number" min="8" max="150" value="100">
    </span>
    <span style="display: flex; justify-content: center;">
      <canvas id="TXTCanvas" width="248" height="122" style="border: 1px solid black;"></canvas>
    </span>
    <div style="display: flex; justify-content: space-around; padding-top: 5px;">
      <button xdh:onevent="TXTSubmit">Submit</button>
      <button xdh:onevent="TXTClear">Clear</button>
    </div>
  </fieldset>
  <span style="display: flex; width:100%; justify-content: space-around; padding-top: 10px;">
    <button xdh:onevent="Reset">Reset</button>
  </span>
</fieldset>
"""

atlastk.launch(globals=globals())

