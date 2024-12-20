LISTEN = False

import atlastk, ucuq, json, math, random

cRing = None
cDisplay = None
cBuzzer = None

DIGITS = [
  0x3a33ae62e,
  0x11842108e, 
  0x3a213221f,
  0x7c223062e,
  0x8ca97c42,
  0x7e1e0862e,
  0x3a30f462e,
  0x7c2222108,
  0x3a317462e,
  0x3a317862e,
]

COEFF_DISPLAY = 8
coeffRing = 1
countButton = 0
countRing = 0

# Presets
P_USER = "User"
P_DIY = "DIY"
P_SIMULATION = "Simulation"

# Widgets
W_PRESET = "Preset"
W_PIN = "Pin"
W_COUNT = "Count"
W_PWM = "PWM"
W_SDA = "SDA"
W_SCL = "SCL"

# Default hardware settings
SETTINGS = {
  P_USER: {
  },
  P_DIY: {
    W_PIN: "3",
    W_COUNT: "8",
    W_PWM: "21",
    W_SDA: "0",
    W_SCL: "1"
  },
  P_SIMULATION: {
    W_PIN: "15",
    W_COUNT: "16",
    W_PWM: "32",
    W_SDA: "21",
    W_SCL: "22"
  }
}

PRESETS = {
  ucuq.K_UNKNOWN: P_USER,
  ucuq.K_DIY: P_DIY,
  ucuq.K_WOKWI: P_SIMULATION
}

seq = ""
userSeq = ""

def digit(n,off):
  pattern = DIGITS[n]

  for x in range(5):
    for y in range(7):
      cDisplay.rect(off+x*COEFF_DISPLAY,y*COEFF_DISPLAY,COEFF_DISPLAY,COEFF_DISPLAY,1 if pattern & (1 << ((4 - x ) + (6 - y) * 5)) else 0)
  
  cDisplay.show()

def number(n):
  try:
    digit(n // 10, 12)
    digit(n % 10, 76)
  except:
    cDisplay.fill(0).show()

BUTTONS = {
  "Y": [[30, 30, 0], 1, 17],
  "G": [[0, 30, 0], 3, 5],
  "R": [[30, 0, 0], 5, 9],
  "B": [[0, 0, 30], 7, 12],
}

SPOKEN_COLORS = {
  "rouge": "R",
  "bleu": "B",
  "jaune": "Y",
  "vert": "G",
  "verre": "G",
  "verte": "G"
}

pitches = []

for i in range(24):
  pitches.append(int(220*math.pow(math.pow(2,1.0/12), i)))

LAUNCH_JINGLE = [
  3, 10,
  0, 8, 7, 5,
  3, 7, 10,
  8, 5, 3
]

SUCCESS_JINGLE = [
  7, 10, 19, 15, 17, 22
]

FAIL_JINGLE = [
  7, 10, 19, 15, 17, 22
]


def convert(value, converter):
  try:
    value = converter(value)
  except:
    return None
  else:
    return value


async def getInputs(dom):
  values = await dom.getValues([W_PIN, W_COUNT, W_PWM, W_SDA, W_SCL])

  return {
    W_PIN: convert(values[W_PIN], int),
    W_COUNT: convert(values[W_COUNT], int),
    W_PWM: convert(values[W_PWM], int),
    W_SDA: convert(values[W_SDA], int),
    W_SCL: convert(values[W_SCL], int),
  }

def flash(button):
  cRing.fill([0,0,0])
  if button in BUTTONS:
    for i in range(1 + countRing // 4):
      cRing.setValue((list(BUTTONS.keys()).index(button) * countRing // 4 + 1 + i) % countRing,[coeffRing * item for item in BUTTONS[button][0]])
  cRing.write()


def beep(note, delay = 0.29, sleep = 0.01):
  cBuzzer.setFreq(pitches[note]).setU16(30000)
  ucuq.sleep(delay)
  cBuzzer.setU16(0)
  if sleep:
    ucuq.sleep(sleep)


def playJingle(jingle):
  prevButton = ""
  prevPrevButton = ""
  number(None)
  ucuq.commit()
  for n in jingle:
    while True:
      button = random.choice(list(BUTTONS.keys())) 
      if ( button != prevButton ) and ( button != prevPrevButton ):
        break
    prevPrevButton = prevButton
    flash(prevButton := button)
    beep(n, 0.15, 0)
  flash("")
  ucuq.commit()


async def updateHardwareUI(dom):
  await dom.setValues(SETTINGS[await dom.getValue(W_PRESET)])


async def acConnect(dom):
  preset = PRESETS[ucuq.getKitId(await ucuq.ATKConnectAwait(dom, BODY))]

  await dom.setValue(W_PRESET, preset)

  if preset == P_SIMULATION:
    global coeffRing
    coeffRing = 8

  await updateHardwareUI(dom)

  if not LISTEN:
    await dom.setAttribute("Listen","style", "display: none;")


async def acPreset(dom):
  await updateHardwareUI(dom)


async def acSwitch(dom):
  global cRing, cDisplay, cBuzzer, countRing

  inputs = await getInputs(dom)

  countRing = inputs[W_COUNT]


  cRing = ucuq.WS2812(inputs[W_PIN], inputs[W_COUNT])
  cDisplay = ucuq.SSD1306_I2C(128, 64, ucuq.SoftI2C(inputs[W_SDA], inputs[W_SCL]))
  cBuzzer = ucuq.PWM(inputs[W_PWM])
  cBuzzer.setFreq(50).setNS(0)
  number(None)
  ucuq.commit()


async def acListen(dom):
  await dom.executeVoid("launch()")


def display(button):
  cRing.fill([0,0,0])
  if button in BUTTONS:
    for i in range(1 + countRing // 4):
      cRing.setValue((list(BUTTONS.keys()).index(button) * countRing // 4 + 1 + i) % countRing,[coeffRing * item for item in BUTTONS[button][0]])
  cRing.write()
  cBuzzer.setFreq(pitches[BUTTONS[button][2]]).setU16(30000)
  ucuq.sleep(0.29)
  cBuzzer.setU16(0)
  cRing.fill([0,0,0]).write()
  ucuq.sleep(0.01)


def play(sequence):
  for s in sequence:
    display(s)
  ucuq.commit()

  
async def acDisplay(dom):
  colors = json.loads(await dom.getValue("Color"))

  for color in colors:
    color = color.lower()
    if color in SPOKEN_COLORS:
      ucuq.sleep(.25)
      display(SPOKEN_COLORS[color])
      ucuq.commit()


async def acNew():
  global seq

  playJingle(LAUNCH_JINGLE)

  seq = random.choice("RGBY")
  number(len(seq))
  play(seq)


async def acClick(dom, id):
  global seq, userSeq

  if not seq:
    return
  
  userSeq += id
  number(len(seq)-len(userSeq))
  display(id)

  if seq.startswith(userSeq):
    if len(seq) <= len(userSeq):
      playJingle(SUCCESS_JINGLE)
      userSeq = ""
      seq += random.choice("RGBY")
      number(len(seq))
      play(seq)
  else:
    number(len(seq))
    cBuzzer.setFreq(30).setU16(50000)
    ucuq.sleep(1)
    cBuzzer.setU16(0)
    ucuq.commit()
    userSeq = ""
    seq = ""

  ucuq.commit()


CALLBACKS = {
  "": acConnect,
  "Preset": acPreset,
  "Switch": acSwitch,
  "Listen": acListen,
  "Display": acDisplay,
  "New": acNew,
  "Click": acClick,
}

HEAD = """
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
  
  recognition.onresult = function(event) {
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
  
  recognition.onspeechend = function() {
    recognition.start();
  };
  
  recognition.onnomatch = function(event) {
    console.warn("I didn't recognise that color.");
  };
  
  recognition.onerror = function(event) {
    console.err('Error occurred in recognition: ' + event.error);
  };
</script>
<style>
#outer-circle {
  background: #385a94;
  border-radius: 50%;
  height: 400px;
  width: 400px;
  position: relative;
  border-style: solid;
  border-width: 10px;
  margin: auto;
  margin-top: 60px;
  box-shadow: 8px 8px 15px 5px #888888;
}

#G {
  position: absolute;
  height: 200px;
  width: 200px;
  border-radius: 200px 0 0 0;
  -moz-border-radius: 200px 0 0 0;
  -webkit-border-radius: 200px 0 0 0;
  background: darkgreen;
  top: 50%;
  left: 50%;
  margin: -200px 0px 0px -200px;
  border-style: solid;
  border-width: 5px;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
}

#R {
  position: absolute;
  height: 200px;
  width: 200px;
  border-radius: 0 200px 0 0;
  -moz-border-radius: 0 200px 0 0;
  -webkit-border-radius: 0 200px 0 0;
  background: darkred;
  top: 50%;
  left: 50%;
  margin: -200px 0px 0px 0px;
  border-style: solid;
  border-width: 5px;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
}

#Y {
  position: absolute;
  height: 200px;
  width: 200px;
  border-radius: 0 0 0 200px;
  -moz-border-radius: 0 0 0 200px;
  -webkit-border-radius: 0 0 0 200px;
  background: goldenrod;
  top: 50%;
  left: 50%;
  margin: 0px -200px 0px -200px;
  border-style: solid;
  border-width: 5px;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
}

#B {
  position: absolute;
  height: 200px;
  width: 200px;
  border-radius: 0 0 200px 0;
  -moz-border-radius: 0 0 200px 0;
  -webkit-border-radius: 0 0 200px 0;
  background: darkblue;
  top: 50%;
  left: 50%;
  margin: 0px 0px -200px 0px;
  border-style: solid;
  border-width: 5px;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
}

#inner-circle {
  position: absolute;
  background: grey;
  border-radius: 50%;
  height: 200px;
  width: 200px;
  border-style: solid;
  border-width: 10px;
  top: 50%;
  left: 50%;
  margin: -100px 0px 0px -100px;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
}

button {
  font-size: xx-large;
}
/* Switch begin */
.switch-container {
  display: flex;
  margin-top: 10px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 30px;
  height: 17px;
  margin: auto;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s cubic-bezier(0,1,0.5,1);
  border-radius: 4px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 13px;
  width: 13px;
  left: 3px;
  bottom: 2px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s cubic-bezier(0,1,0.5,1);
  border-radius: 3px;
}

input:checked + .slider {
  background-color: #52c944;
}

input:focus + .slider {
  box-shadow: 0 0 4px #7efa70;
}

input:checked + .slider:before {
  -webkit-transform: translateX(10px);
  -ms-transform: translateX(10px);
  transform: translateX(10px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 17px;
}

.slider.round:before {
  border-radius: 50%;
}

#round {
  border-radius: 17px;
}

#round:before {
  border-radius: 50%;
}
/* Switch end */

</style>
</style>
"""

BODY = """
<fieldset style="display: flex;">
  <fieldset>
    <legend>Preset</legend>
  <select xdh:onevent="Preset" id="Preset">
    <option value="User">User</option>
    <optgroup label="q37.info">
      <option value="DIY">DIY</option>
    </optgroup>
    <optgroup label="Wokwi">
      <option value="Simulation">Simulation</option>
    </optgroup>
  </select>
        <span class="switch-container">
          <label class="switch">
            <input id="Switch"  type="checkbox" xdh:onevent="Switch">
            <span class="slider round"></span>
          </label>
        </span>        
  </fieldset>
  <fieldset style="display: flex; flex-direction: column">
    <legend>Ring</legend>
    <label style="display: flex; justify-content: space-between;">
      <span>Pin:</span>
      <input id="Pin" min="1" max="99" type="number">
    </label>
    <label style="display: flex; justify-content: space-between;">
      <span>Count:&nbsp;</span>
      <input id="Count" min="1" max="99" type="number">
    </label>
  </fieldset>
  <fieldset>
    <legend>Sound</legend>
    <label>
      <span>PWM:</span>
      <input id="PWM"  min="1" max="99" type="number">
    </label>
  </fieldset>
  <fieldset style="display: flex; flex-direction: column">
    <legend>OLED</legend>
    <label style="display: flex; justify-content: space-between;">
      <span>SDA:</span>
      <input id="SDA" type="number" value="0" min="0" max="99">
    </label>
    <label style="display: flex; justify-content: space-between;">
      <span>SCL:</span>
      <input id="SCL" type="number" value="1" min="0" max="99">
    </label>
  </fieldset>
</fieldset>
<fieldset>
<input id="Color" type="hidden">
<div id="outer-circle">
  <div id="G" xdh:onevent="Click"></div>
  <div id="R" xdh:onevent="Click"></div>
  <div id="Y" xdh:onevent="Click"></div>
  <div id="B" xdh:onevent="Click"></div>
  <div id="inner-circle" style="display: flex;justify-content: center;align-items: center; flex-direction: column;">
    <div>
      <button xdh:onevent="New">New</button>
    </div>
    <div>
      <button id="Listen" xdh:onevent="Listen">Listen</button>
    </div>
  </div>
</div>
  </fieldset>
"""

atlastk.launch(CALLBACKS, headContent = HEAD)
