import atlastk, ucuq, json, math, random

onDuty = False
cRing = None
cOLED = None
cBuzzer = None
cLCD = None

EN = {
  0: "Welcome to",
  1: "Simon's game!",
  2: "Reproduce the",
  3: "sequence...",
  4: "Well done!",
  5: "Game over! Click",
  6: "New to restart!",
}

FR = {
  0: "Bienvenue au jeu",
  1: "'Simon' !",
  2: "Reproduire la",
  3: "sequence...",
  4: "Bravo !",
  5: "Perdu ! 'New'",
  6: "pour rejouer !",
}

STRINGS = EN

DIGITS = (
  "708898A8C88870",
  "20602020202070",
  "708808304080f8",
  "f8081030088870",
  "10305090f81010",
  "f880f008088870",
  "708880f0888870",
  "f8081020404040",
  "70888870888870",
  "70888878088870",
)

HAPPY_MOTIF = "03c00c30181820044c32524a80018001824181814812442223c410080c3003c0"
SAD_MOTIF = "03c00c30181820044c3280018001824181814002400227e410080c3003c0"

OLED_COEFF = 8
ringCount = 0
ringOffset = 0
ringLimiter = 0

# Presets
P_USER = "User"
P_DIY = "DIY"
P_WOKWI = "Wokwi"

# Widgets
# Hardware widgets
W_HARDWARE = "Hardware"
W_H_SWITCH = "Switch"
W_H_PRESET = "Preset"
W_H_RING_PIN = "Ring_Pin"
W_H_RING_COUNT = "Ring_Count"
W_H_RING_OFFSET = "Ring_Offset"
W_H_RING_LIMITER = "Ring_Limiter"
W_H_BUZZER_ON = "Buzzer_On"
W_H_BUZZER_PIN = "Buzzer_Pin"
W_H_OLED_SOFT = "OLED_Soft"
W_H_OLED_SDA = "OLED_SDA"
W_H_OLED_SCL = "OLED_SCL"
W_H_LCD_SOFT = "LCD_Soft"
W_H_LCD_SDA = "LCD_SDA"
W_H_LCD_SCL = "LCD_SCL"
# Board widgets
W_BOARD = "Board"
W_B_R = "R"
W_B_G = "G"
W_B_B = "B"
W_B_Y = "Y"
W_B_NEW = "New"
W_B_REPEAT = "Repeat"

def getValuesOfVarsBeginningWith(prefix):
  return [value for var, value in globals().items() if var.startswith(prefix)]

def remove(source, items):
  return [item for item in source if item not in items]


HARDWARE_WIDGETS = getValuesOfVarsBeginningWith("W_H_")
HARDWARE_WIDGETS_WITHOUT_SWITCH = remove(HARDWARE_WIDGETS, [W_H_SWITCH])
BOARD_WIDGETS = getValuesOfVarsBeginningWith("W_B_")

# Default hardware settings
SETTINGS = {
  P_USER: {
  },
  P_DIY: {
    W_H_RING_PIN: ucuq.H_DIY_DISPLAYS["Ring"]["Pin"],
    W_H_RING_COUNT: ucuq.H_DIY_DISPLAYS["Ring"]["Count"],
    W_H_RING_OFFSET: ucuq.H_DIY_DISPLAYS["Ring"]["Offset"],
    W_H_RING_LIMITER:ucuq.H_DIY_DISPLAYS["Ring"]["Limiter"],
    W_H_BUZZER_ON: "true",
    W_H_BUZZER_PIN: ucuq.H_DIY_DISPLAYS["Buzzer"]["Pin"],
    W_H_OLED_SOFT: ucuq.H_DIY_DISPLAYS["OLED"]["Soft"],
    W_H_OLED_SDA: ucuq.H_DIY_DISPLAYS["OLED"]["SDA"],
    W_H_OLED_SCL: ucuq.H_DIY_DISPLAYS["OLED"]["SCL"],
    W_H_LCD_SOFT: ucuq.H_DIY_DISPLAYS["LCD"]["Soft"],
    W_H_LCD_SDA: ucuq.H_DIY_DISPLAYS["LCD"]["SDA"],
    W_H_LCD_SCL: ucuq.H_DIY_DISPLAYS["LCD"]["SCL"],
  },
  P_WOKWI: {
    W_H_RING_PIN: ucuq.H_WOKWI_DISPLAYS["Ring"]["Pin"],
    W_H_RING_COUNT: ucuq.H_WOKWI_DISPLAYS["Ring"]["Count"],
    W_H_RING_OFFSET: ucuq.H_WOKWI_DISPLAYS["Ring"]["Offset"],
    W_H_RING_LIMITER:ucuq.H_WOKWI_DISPLAYS["Ring"]["Limiter"],
    W_H_BUZZER_ON: "true",
    W_H_BUZZER_PIN: ucuq.H_WOKWI_DISPLAYS["Buzzer"]["Pin"],
    W_H_OLED_SOFT: ucuq.H_WOKWI_DISPLAYS["OLED"]["Soft"],
    W_H_OLED_SDA: ucuq.H_WOKWI_DISPLAYS["OLED"]["SDA"],
    W_H_OLED_SCL: ucuq.H_WOKWI_DISPLAYS["OLED"]["SCL"],
    W_H_LCD_SOFT: ucuq.H_WOKWI_DISPLAYS["LCD"]["Soft"],
    W_H_LCD_SDA: ucuq.H_WOKWI_DISPLAYS["LCD"]["SDA"],
    W_H_LCD_SCL: ucuq.H_WOKWI_DISPLAYS["LCD"]["SCL"],
  }
}

PRESETS = {
  ucuq.K_UNKNOWN: P_USER,
  ucuq.K_DIY_DISPLAYS: P_DIY,
  ucuq.K_WOKWI_DISPLAYS: P_WOKWI
}

seq = ""
userSeq = ""

def digit(n,offset):
  cOLED.draw(DIGITS[n], 8, offset, mul=8)

def number(n):
  try:
    digit(n // 10, 12)
    digit(n % 10, 76)
  except:
    cOLED.fill(0)
  cOLED.show()

BUTTONS = {
  "R": [[255, 0, 0], 5, 9],
  "B": [[0, 0, 255], 7, 12],
  "Y": [[255, 255, 0], 1, 17],
  "G": [[0, 255, 0], 3, 5],
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
    return converter(value)
  except:
    raise Exception("Bad or missing value!")


async def getInputs(dom):
  values = await dom.getValues([
      W_H_RING_PIN, W_H_RING_COUNT, W_H_RING_OFFSET, W_H_RING_LIMITER,
      W_H_BUZZER_ON, W_H_BUZZER_PIN,
      W_H_OLED_SOFT, W_H_OLED_SDA, W_H_OLED_SCL,
      W_H_LCD_SOFT, W_H_LCD_SDA, W_H_LCD_SCL])

  return {
    W_H_RING_PIN: convert(values[W_H_RING_PIN], int),
    W_H_RING_COUNT: convert(values[W_H_RING_COUNT], int),
    W_H_RING_OFFSET: convert(values[W_H_RING_OFFSET], int),
    W_H_RING_LIMITER: convert(values[W_H_RING_LIMITER], int),
    W_H_BUZZER_ON: True if values[W_H_BUZZER_ON] == "true" else False,
    W_H_BUZZER_PIN: convert(values[W_H_BUZZER_PIN], int),
    W_H_OLED_SOFT: True if values[W_H_OLED_SOFT] == "true" else False,
    W_H_OLED_SDA: convert(values[W_H_OLED_SDA], int),
    W_H_OLED_SCL: convert(values[W_H_OLED_SCL], int),
    W_H_LCD_SOFT: True if values[W_H_LCD_SOFT] == "true" else False,
    W_H_LCD_SDA: convert(values[W_H_LCD_SDA], int),
    W_H_LCD_SCL: convert(values[W_H_LCD_SCL], int),
  }

def flash(button):
  cRing.fill([0,0,0])
  if button in BUTTONS:
    for i in range(1 + ringCount // 4):
      cRing.setValue((list(BUTTONS.keys()).index(button) * ringCount // 4 + i + ringOffset) % ringCount,[ringLimiter * item // 255 for item in BUTTONS[button][0]])
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
#  number(None)
  for n in jingle:
    while True:
      button = random.choice(list(BUTTONS.keys())) 
      if ( button != prevButton ) and ( button != prevPrevButton ):
        break
    prevPrevButton = prevButton
    flash(prevButton := button)
    beep(n, 0.15, 0)
  flash("")


async def updateHardwareUI(dom):
  await dom.setValues(SETTINGS[await dom.getValue(W_H_PRESET)])


async def atk(dom):
  preset = PRESETS[ucuq.getKitId(await ucuq.ATKConnectAwait(dom, BODY))]

  await dom.setValue(W_H_PRESET, preset)

  await updateHardwareUI(dom)


async def atkPreset(dom):
  await updateHardwareUI(dom)


async def atkSwitch(dom, id):
  global onDuty, cRing, cOLED, cBuzzer, cLCD, ringCount, ringOffset, ringLimiter

  if await dom.getValue(id) == "true":
    try:
      inputs = await getInputs(dom)
    except Exception as exc:
      await dom.setValue(W_H_SWITCH, "false")
      await dom.alert(exc)
      return

    ringCount = inputs[W_H_RING_COUNT]
    ringOffset = inputs[W_H_RING_OFFSET]
    ringLimiter = inputs[W_H_RING_LIMITER]

    ucuq.setCommitBehavior(ucuq.CB_MANUAL)

    cRing = ucuq.WS2812(inputs[W_H_RING_PIN], inputs[W_H_RING_COUNT]).fill([0,0,0]).write()
    cOLED = ucuq.SSD1306_I2C(128, 64, ucuq.I2C(inputs[W_H_OLED_SDA], inputs[W_H_OLED_SCL], soft = inputs[W_H_OLED_SOFT]))
    cLCD = ucuq.HD44780_I2C(ucuq.I2C(inputs[W_H_LCD_SDA], inputs[W_H_LCD_SCL], soft = inputs[W_H_LCD_SOFT]), 2, 16).backlightOff()
    if inputs[W_H_BUZZER_ON]:
      cBuzzer = ucuq.PWM(inputs[W_H_BUZZER_PIN], freq=50, u16 = 0)
    else:
      cBuzzer = ucuq.Nothing()
    cBuzzer.setFreq(50).setNS(0)
    number(None)
    cLCD.backlightOff()
    ucuq.commit()
    await dom.enableElements(BOARD_WIDGETS)
    await dom.disableElements(HARDWARE_WIDGETS_WITHOUT_SWITCH)
    onDuty = True
  else:
    onDuty = False
    await dom.disableElements(BOARD_WIDGETS)
    await dom.enableElements(HARDWARE_WIDGETS_WITHOUT_SWITCH)


async def atkRepeat():
  play(seq)
  ucuq.commit()


def display(button):
  cRing.fill([0,0,0])
  if button in BUTTONS:
    for i in range(1 + ringCount // 4):
      cRing.setValue((list(BUTTONS.keys()).index(button) * ringCount // 4 + i + ringOffset) % ringCount,[ringLimiter * item // 255 for item in BUTTONS[button][0]])
  cRing.write()
  cBuzzer.setFreq(pitches[BUTTONS[button][2]]).setU16(30000)
  ucuq.sleep(0.29)
  cBuzzer.setU16(0)
  cRing.fill([0,0,0]).write()
  ucuq.sleep(0.01)


def play(sequence):
  seq=""
  for s in sequence:
    number(len(seq)+1)
    display(s)
    seq += s
    if len(seq) % 5:
      ucuq.commit()

  
async def atkDisplay(dom):
  colors = json.loads(await dom.getValue("Color"))

  for color in colors:
    color = color.lower()
    if color in SPOKEN_COLORS:
      ucuq.sleep(.25)
      display(SPOKEN_COLORS[color])
      ucuq.commit()


async def atkNew():
  global seq
  
  number(None)

  cLCD.clear()\
  .backlightOn()\
  .moveTo(0,0)\
  .putString(STRINGS[0])\
  .moveTo(0,1)\
  .putString(STRINGS[1])

  playJingle(LAUNCH_JINGLE)
  ucuq.sleep(0.5)
  cLCD.clear()

  seq = random.choice("RGBY")
  cLCD.clear().moveTo(0,0).putString(STRINGS[2]).moveTo(0,1).putString(STRINGS[3])
  number(0)
  ucuq.sleep(.75)
  play(seq)
  ucuq.commit()


async def atkClick(dom, id):
  global seq, userSeq

  if not seq:
    return
  
  userSeq += id
  cLCD.clear().moveTo(0,0).putString(userSeq).backlightOn()
  number(len(seq)-len(userSeq))
  display(id)

  if seq.startswith(userSeq):
    if len(seq) <= len(userSeq):
      cLCD.moveTo(0,0).putString(STRINGS[4])
      number(None)
      cOLED.draw(HAPPY_MOTIF, 16, mul=4, ox=32).show()
      playJingle(SUCCESS_JINGLE)
      ucuq.sleep(0.5)
      cLCD.clear()
      ucuq.commit()
      userSeq = ""
      seq += random.choice("RGBY")
      cLCD.clear().moveTo(0,0).putString(STRINGS[2]).moveTo(0,1).putString(STRINGS[3])
      number(None)
      ucuq.commit()
      number(0)
      ucuq.sleep(.75)
      play(seq)
    else:
      cLCD.backlightOff()
  else:
    cLCD.moveTo(0,0).putString(STRINGS[5]).moveTo(0,1).putString(STRINGS[6])
    number(len(seq))
    cBuzzer.setFreq(30).setU16(50000)
    number(None)
    cOLED.fill(0).draw(SAD_MOTIF, 16, mul=4, ox=32).show()
    ucuq.sleep(1)
    cBuzzer.setU16(0)
    ucuq.commit()
    userSeq = ""
    seq = ""

  ucuq.commit()

ATK_HEAD = """
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

  /****************/
  /* Switch begin */
  /****************/

  .switch-container {
    display: flex;
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
    transition: .4s cubic-bezier(0, 1, 0.5, 1);
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
    transition: .4s cubic-bezier(0, 1, 0.5, 1);
    border-radius: 3px;
  }

  input+.slider {
    background-color: #c95245;
  }

  input:checked+.slider {
    background-color: #52c944;
  }

  input:focus+.slider {
    box-shadow: 0 0 4px #7efa70;
  }

  input:checked+.slider:before {
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

  /**************/
  /* Switch end */
  /**************/
</style>
"""

BODY = """
<fieldset style="display: flex; flex-direction: column">
  <div style="display: flex; justify-content: space-evenly;">
    <select xdh:onevent="Preset" id="Preset">
      <option value="User">User</option>
      <option value="DIY">DIY</option>
      <option value="Wokwi">Wokwi</option>
    </select>
    <span class="switch-container">
      <label class="switch">
        <input id="Switch" type="checkbox" xdh:onevent="Switch">
        <span class="slider round"></span>
      </label>
    </span>
  </div>
  <div id="Hardware" style="display: flex;">
    <fieldset style="display: flex; flex-direction: column; justify-content: space-around;">
      <legend>Ring</legend>
      <div style="display: flex; justify-content: space-between">
        <input id="Ring_Pin" min="0" max="99" type="number" placeholder="Pin">
        <input id="Ring_Count" min="0" max="999" type="number" placeholder="Count">
      </div>
      <div style="display: flex; justify-content: space-between">
        <input id="Ring_Offset" min="-999" max="999" type="number" placeholder="Offset">
        <input id="Ring_Limiter" min="0" max="255" type="number" placeholder="Limiter">
      </div>
    </fieldset>
    <fieldset style="display: flex; flex-direction: column; justify-content: space-around;">
      <legend>Buzzer</legend>
      <label>
        <input id="Buzzer_On" type="checkbox" />
        <span>On</span>
      </label>
      <input id="Buzzer_Pin" min="0" max="99" type="number" placeholder="Pin">
    </fieldset>
    <fieldset style="display: flex; flex-direction: column; justify-content: space-around;">
      <legend>OLED</legend>
      <label>
        <input id="OLED_Soft" type="checkbox">
        <span>Soft</span>
      </label>
      <input id="OLED_SDA" type="number" min="0" max="99" placeholder="SDA">
      <input id="OLED_SCL" type="number" min="0" max="99" placeholder="SCL">
    </fieldset>
    <fieldset style="display: flex; flex-direction: column; justify-content: space-around;">
      <legend>LCD</legend>
      <label>
        <input id="LCD_Soft" type="checkbox">
        <span>Soft</span>
      </label>
      <input id="LCD_SDA" type="number" min="0" max="99" placeholder="SDA">
      <input id="LCD_SCL" type="number" min="0" max="99" placeholder="SCL">
    </fieldset>
</fieldset>
</div>
<fieldset id="Board">
  <input id="Color" type="hidden">
  <div id="outer-circle">
    <div id="G" xdh:onevent="Click"></div>
    <div id="R" xdh:onevent="Click"></div>
    <div id="Y" xdh:onevent="Click"></div>
    <div id="B" xdh:onevent="Click"></div>
    <div id="inner-circle" style="display: flex;justify-content: center;align-items: center; flex-direction: column;">
      <div>
        <button id="Repeat" xdh:onevent="Repeat" disabled="disabled">Repeat</button>
      </div>
      <div>
        <button id="New" xdh:onevent="New" disabled="disabled">New</button>
      </div>
    </div>
  </div>
</fieldset>
"""

atlastk.launch(globals=globals())

