import atlastk, ucuq, datetime, time

epaper = None

W_TEXT = "Text"

async def atk(dom):
  global epaper

  await ucuq.ATKConnectAwait(dom, BODY)
  epaper = ucuq.SSD1680_SPI(7, 1, 2, 3, ucuq.SPI(1, baudrate=2000000, polarity=0, phase=0, sck=4, mosi=6))
  epaper.fill(0).hText("E-paper ready !", 50).hText(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 75).show()
  await dom.focus(W_TEXT)

# Called from JS!
async def atkDisplay(dom, id):
  epaper.fill(0).draw(id, ox=60, oy=6, width=120).show()


async def atkSubmit(dom):
  await dom.executeVoid(f"QRCodeLaunch('{await dom.getValue(W_TEXT)}')")
  await dom.focus(W_TEXT)


async def atkClear(dom):
  await dom.setValue(W_TEXT, "")
  await dom.focus(W_TEXT)


async def atkReset(dom, id):
  global epaper
  epaper = ucuq.SSD1680_SPI(7, 1, 2, 3, ucuq.SPI(1, baudrate=2000000, polarity=0, phase=0, sck=4, mosi=6)).fill(0).show()


ATK_HEAD = """
<script>
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

    const width = canvas.width;
    if (width % 4 !== 0) {
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

    return { hexString, width };
  }

  function QRCodeLAunch(text) {
    QRCodeGenerate(text)
      .then(({ hexString, width }) => {
        launchEvent(`${hexString}|BUTTON|click||(Display)`);
      })
      .catch(e => console.error(e));
  }

</script>
"""

BODY = """
<fieldset>
  <legend>E-paper</legend>
  <fieldset>
    <legend>QR code</legend>
    <input id="Text" xdh:onevent="Submit" type="text" style="width: 100%" placeholder="Text to convert"
      value="https://q37.info/ucuq/">
    <div style="display: flex; justify-content: space-around; padding-top: 10px;">
      <button xdh:onevent="Submit">Submit</button>
      <button xdh:onevent="Clear">Clear</button>
    </div>
  </fieldset>
  <span style="display: flex; width:100%; justify-content: space-around; padding-top: 10px;">
    <button xdh:onevent="Reset">Reset</button>
  </span>
</fieldset>
"""

atlastk.launch(globals=globals())

