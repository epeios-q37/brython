from itertools import count
import atlastk, ucuq, random, json

RB_DELAY = .05

SPOKEN_COLORS =  {
  "rouge": [255, 0, 0],
  "vert": [0, 255, 0],
  "verre": [0, 255, 0],
  "verte": [0, 255, 0],
  "bleu": [0, 0, 255],
  "jaune": [255, 255, 0],
  "cyan": [0, 255, 255],
  "magenta": [255, 0, 255],
  "orange": [255, 127, 0],
  "violet": [127, 0, 255],
  "rose": [255, 127, 127],
  "gris": [127, 127, 127],
  "noir": [0, 0, 0],
  "blanc": [255, 255, 255],
  "marron": [127, 59, 0],
  "turquoise": [0, 127, 127],
  "beige": [255, 212, 170]
}


ws2812 = None
lcd = None
matrix = None


def rainbow():
  v =  random.randint(0, 5)
  i = 0
  while i < 7 * ws2812Limiter:
    update_(*ucuq.rbShadeFade(v, int(i), ws2812Limiter), ws2812Limiter)
    ucuq.sleep(RB_DELAY)
    i += ws2812Limiter / 20
  update_(0, 0, 0, ws2812Limiter)


def getValues_(target, R, G, B):
  return {
    target + "R": R,
    target + "G": G,
    target + "B": B
  }


def getNValues_(R, G, B):
  return getValues_("N", R, G, B)


def getSValues_(R, G, B):
  return getValues_("S", R, G, B)


def getAllValues_(R, G, B):
  return getNValues_(R, G, B) | getSValues_(R, G, B)


def drawBarOnMatrix(x, height):
  y = int(height)

  if y != 0:
    matrix.rect(x * 6, 8 - y, x * 6 + 3, 7)


def update_(r, g, b, limit, color=""):
  ws2812.fill(list(map(int, [r, g, b]))).write()

  if matrix:
    matrix.clear()
    drawBarOnMatrix(0, int(r) * 8 / limit)
    drawBarOnMatrix(1, int(g) * 8 / limit)
    drawBarOnMatrix(2, int(b) * 8 / limit)
    matrix.show()

  if lcd:
    lcd.moveTo(0,0)\
      .putString("RGB: {} {} {}".format(*map(lambda s: str(s).rjust(3), [r, g, b])))\
      .moveTo(0,1)\
      .putString(color.center(16))


async def resetAwait(dom):
  await dom.executeVoid(f"colorWheel.rgb = [0, 0, 0]")
  await dom.setValues(getAllValues_(0, 0, 0))
  update_(0, 0, 0, 255)    


def turnOnMain(hardware):
  global ws2812, ws2812Limiter

  if hardware:
    pin = hardware["Pin"]
    count = hardware["Count"]
    ws2812Limiter = hardware["Limiter"]

    ws2812 = ucuq.WS2812(pin, count)
  else:
    raise("Kit has no ws2812!")
  

def turnOnLCD(hardware):
  global lcd

  if hardware:
    soft = hardware["Soft"]
    sda = hardware["SDA"]
    scl = hardware["SCL"]

    lcd = ucuq.HD44780_I2C(ucuq.I2C(sda, scl, soft=soft), 2, 16).backlightOn()
  else:
    lcd = ucuq.Nothing()


def turnOnMatrix(hardware):
  global matrix

  if hardware:
    soft = hardware["Soft"]
    sda = hardware["SDA"]
    scl = hardware["SCL"]

    matrix = ucuq.HT16K33(ucuq.I2C(sda, scl, soft=soft)).clear().show()
  else:
    matrix = ucuq.Nothing()


async def atk(dom):
  infos = await ucuq.ATKConnectAwait(dom, BODY)

  await dom.executeVoid("setColorWheel()")
  await dom.executeVoid(f"colorWheel.rgb = [0, 0, 0]")

  if not ws2812:
    hardware = ucuq.getKitHardware(infos)

    turnOnMain(ucuq.getHardware(hardware, ("Ring", "RGB")))
    turnOnMatrix(ucuq.getHardware(hardware, "Matrix"))
    turnOnLCD(ucuq.getHardware(hardware, "LCD"))


async def atkSelect(dom):
  R, G, B = (await dom.getValues(["rgb-r", "rgb-g", "rgb-b"])).values()
  await dom.setValues(getAllValues_(R, G, B))
  update_(R, G, B, 255)


async def atkSlide(dom):
  (R,G,B) = (await dom.getValues(["SR", "SG", "SB"])).values()
  await dom.setValues(getNValues_(R, G, B))
  await dom.executeVoid(f"colorWheel.rgb = [{R},{G},{B}]")
  update_(R, G, B, 255)


async def atkAdjust(dom):
  (R,G,B) = (await dom.getValues(["NR", "NG", "NB"])).values()
  await dom.setValues(getSValues_(R, G, B))
  await dom.executeVoid(f"colorWheel.rgb = [{R},{G},{B}]")
  update_(R, G, B, 255)


async def atkListen(dom):
  await dom.executeVoid("launch()")


# Launched by the JS 'launch()' script.
async def atkDisplay(dom):
  colors = json.loads(await dom.getValue("Color"))

  for color in colors:
    color = color.lower()
    if color in SPOKEN_COLORS:
      r, g, b = [ws2812Limiter * c // 255 for c in SPOKEN_COLORS[color]]
      await dom.setValues(getAllValues_(r, g, b))
      await dom.executeVoid(f"colorWheel.rgb = [{r},{g},{b}]")
      update_(r, g, b, ws2812Limiter, color)
      break


async def atkRainbow(dom):
  await resetAwait(dom)
  rainbow()


async def atkReset(dom):
  await resetAwait(dom)


ATK_HEAD = """
<script type="text/javascript">
  function setColorWheel() {
    var hsvInputs = [document.getElementById('hsv-h'), document.getElementById('hsv-s'), document.getElementById('hsv-v')];
    var hslInputs = [document.getElementById('hsl-h'), document.getElementById('hsl-s'), document.getElementById('hsl-l')];
    var rgbInputs = [document.getElementById('rgb-r'), document.getElementById('rgb-g'), document.getElementById('rgb-b')];
    var hexInput = document.getElementById('hex');
    function set(input, value) {
      if (input !== document.activeElement) {
        input.value = value;
      }
    }
    window.colorWheel = new ReinventedColorWheel({
      appendTo: document.getElementById('color-wheel-container'),
      wheelDiameter: 300,
      wheelThickness: 30,
      handleDiameter: 24,
      wheelReflectsSaturation: true,
      onChange: function (color) {
        set(hsvInputs[0], color.hsv[0].toFixed(1));
        set(hsvInputs[1], color.hsv[1].toFixed(1));
        set(hsvInputs[2], color.hsv[2].toFixed(1));
        set(hslInputs[0], color.hsl[0].toFixed(1));
        set(hslInputs[1], color.hsl[1].toFixed(1));
        set(hslInputs[2], color.hsl[2].toFixed(1));
        set(rgbInputs[0], color.rgb[0]);
        set(rgbInputs[1], color.rgb[1]);
        set(rgbInputs[2], color.rgb[2]);
      },
    });

    colorWheel.onChange(colorWheel);

    function padStart(s, len) {
      s = String(s);
      while (s.length < len)
        s = ' ' + s;
      return s;
    }
  }
</script>
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/reinvented-color-wheel@0.4.0/css/reinvented-color-wheel.min.css">
<script src="https://cdn.jsdelivr.net/npm/reinvented-color-wheel@0.4.0">
</script>
<style>
  .view {
    display: flex;
    flex-direction: column;
    align-content: space-between
  }

  .view {
    display: flex;
    flex-direction: column;
    align-content: space-between
  }

  .hide {
    display: none
  }
</style>
<script>
  var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
  var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent;

  var recognition = new SpeechRecognition();

  recognition.continuous = false;
  recognition.lang = 'fr-FR';
  recognition.interimResults = false;
  recognition.maxAlternatives = 5;

  function launch() {
    recognition.start();
    console.log('Ready to receive a color command.');
  };

  recognition.onresult = function (event) {
    var color = event.results[0][0].transcript;
    console.log('Confidence: ' + event.results[0][0].confidence);
    results = event.results[0];
    array = [];
    for (const cle in results) {
      if (results.hasOwnProperty(cle)) {
        console.log(`${cle}: ${results[cle].transcript}`);
        array.push(results[cle].transcript);
      }
      console.log(array)
    }
    console.log(color);
    document.getElementById("Color").value = JSON.stringify(array);
    launchEvent("test|BUTTON|click||(Display)");
  };

  recognition.onspeechend = function () {
    recognition.start();
  };

  recognition.onnomatch = function (event) {
    console.warn("I didn't recognize that color.");
  };

  recognition.onerror = function (event) {
    console.err('Error occurred in recognition: ' + event.error);
  };
</script>
"""

BODY = """
<div class="color-tables" style="display: none">
  <input id="hsv-h" type="number">
  <input id="hsv-s" type="number">
  <input id="hsv-v" type="number">
  <input id="hsl-h" type="number">
  <input id="hsl-s" type="number">
  <input id="hsl-l" type="number">
  <input id="rgb-r" type="number">
  <input id="rgb-g" type="number">
  <input id="rgb-b" type="number">
</div>
<fieldset>
  <legend>WS2012</legend>
  <div class="view">
    <div>
      <label style="display: flex; align-items: center;">
        <span>R:&nbsp;</span>
        <input id="SR" style="width: 100%" type="range" min="0" max="255" step="1" xdh:onevent="Slide" value="0">
        <span>&nbsp;</span>
        <input id="NR" xdh:onevent="Adjust" type="number" min="0" max="255" step="5" value="0" style="width: 5ch">
      </label>
      <label style="display: flex; align-items: center;">
        <span>V:&nbsp;</span>
        <input id="SG" style="width: 100%" type="range" min="0" max="255" step="1" xdh:onevent="Slide" value="0">
        <span>&nbsp;</span>
        <input id="NG" xdh:onevent="Adjust" type="number" min="0" max="255" step="5" value="0" style="width: 5ch">
      </label>
      <label style="display: flex; align-items: center;">
        <span>B:&nbsp;</span>
        <input id="SB" style="width: 100%" type="range" min="0" max="255" step="1" xdh:onevent="Slide" value="0">
        <span>&nbsp;</span>
        <input id="NB" xdh:onevent="Adjust" type="number" min="0" max="255" step="5" value="0" style="width: 5ch">
      </label>
      <div style="display: flex; justify-content: space-evenly; margin-bottom: 5px;">
        <button xdh:onevent="Listen">Listen</button>
        <button xdh:onevent="Rainbow">Rainbow</button>
        <button xdh:onevent="Reset">Reset</button>
      </div>
    </div>
    <fieldset id="PickerBox" style="display: flex; justify-content: center; flex-direction: column">
      <div id="color-wheel-container" xdh:onevent="Select"></div>
      <label class="label-checkbox" style="display: flex; justify-content: center;">
        <input type="checkbox" checked
          onchange="colorWheel.wheelReflectsSaturation = this.checked; colorWheel.redraw()">
        <span>wheel reflects saturation</span>
      </label>
    </fieldset>
    <input id="Color" type="hidden">
  </div>
</fieldset>
"""

atlastk.launch(globals=globals())

