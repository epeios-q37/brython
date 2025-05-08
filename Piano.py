import ucuq, atlastk, math

# Widgets
W_TARGET = "Target"
W_RATIO_SLIDE = "RatioSlide"
W_RATIO_VALUE = "RatioValue"

pwm = None
baseFreq = 440.0*math.pow(math.pow(2,1.0/12), -16)
ratio = 0.5
target = None

hardware = None

def turnMainOn(hardware):
  global pwm

  if hardware == None:
    raise Exception("Kit with no sound component!")
  
  pwm = ucuq.PWM(hardware["Pin"], freq=50, u16=0).setNS(0)


async def atk(dom):
  global pwm, target, hardware

  infos = await ucuq.ATKConnectAwait(dom, BODY)

  if not pwm:
    hardware = ucuq.getKitHardware(infos)

    turnMainOn(ucuq.getHardware(hardware, "Buzzer"))

    if "Loudspeaker" in hardware:
      await dom.disableElement("HideTarget")
      target = "Buzzer"
  elif target: 
    await dom.setValue(W_TARGET, target)
    await dom.disableElement("HideTarget")


async def atkPlay(dom,id):
  freq = int(baseFreq*math.pow(math.pow(2,1.0/12), int(id)))
  pwm.setFreq(freq).setU16(int(ratio*65535))
  ucuq.sleep(.5)
  pwm.setU16(0)


async def atkSetRatio(dom, id):
  global ratio

  ratio = float(await dom.getValue(id))

  await dom.setValue(W_RATIO_SLIDE if id == W_RATIO_VALUE else W_RATIO_SLIDE, ratio)


async def atkSwitchTarget(dom, id):
  global target

  target = await dom.getValue(id)

  turnMainOn(ucuq.getHardware(hardware, target))

ATK_HEAD = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/beautiful-piano@0.0.6/styles.min.css">
</link>
<script src="https://cdn.jsdelivr.net/npm/beautiful-piano@0.0.6/dist/piano.min.js"></script>
<style id="HideTarget">
  #Target {
    display: none;
  }
</style>
"""

BODY = """
<fieldset>
  <fieldset>
    <ul id="beautiful-piano">
      <li>
        <div id="0" xdh:onevent="Play" class="anchor F3"></div>
      </li>
      <li>
        <div id="2" xdh:onevent="Play" class="anchor G3"></div>
        <span id="1" xdh:onevent="Play" class="Fs3 Gb3"></span>
      </li>
      <li>
        <div id="4" xdh:onevent="Play" class="anchor A3"></div>
        <span id="3" xdh:onevent="Play" class="Gs3 Ab3"></span>
      </li>
      <li>
        <div id="6" xdh:onevent="Play" class="anchor B3"></div>
        <span id="5" xdh:onevent="Play" class="As3 Bb3"></span>
      </li>
      <li>
        <div id="7" xdh:onevent="Play" class="anchor C4"></div>
      </li>
      <li>
        <div id="9" xdh:onevent="Play" class="anchor D4"></div>
        <span id="8" xdh:onevent="Play" class="Cs4 Db4"></span>
      </li>
      <li>
        <div id="11" xdh:onevent="Play" class="anchor E4"></div>
        <span id="10" xdh:onevent="Play" class="Ds4 Eb4"></span>
      </li>
      <li>
        <div id="12" xdh:onevent="Play" class="anchor F4"></div>
      </li>
      <li>
        <div id="14" xdh:onevent="Play" class="anchor G4"></div>
        <span id="13" xdh:onevent="Play" class="Fs4 Gb4"></span>
      </li>
      <li>
        <div id="16" xdh:onevent="Play" class="anchor A4"></div>
        <span id="15" xdh:onevent="Play" class="Gs4 Ab4"></span>
      </li>
      <li>
        <div id="18" xdh:onevent="Play" class="anchor B4"></div>
        <span id="17" xdh:onevent="Play" class="As4 Bb4"></span>
      </li>
      <li>
        <div id="19" xdh:onevent="Play" class="anchor C5"></div>
      </li>
      <li>
        <div id="21" xdh:onevent="Play" class="anchor D5"></div>
        <span id="20" xdh:onevent="Play" class="Cs5 Db5"></span>
      </li>
      <li>
        <div id="23" xdh:onevent="Play" class="anchor E5"></div>
        <span id="22" xdh:onevent="Play" class="Ds5 Eb5"></span>
      </li>
      <li>
        <div id="24" xdh:onevent="Play" class="anchor F5"></div>
      </li>
      <li>
        <div id="26" xdh:onevent="Play" class="anchor G5"></div>
        <span id="25" xdh:onevent="Play" class="Fs5 Gb5"></span>
      </li>
      <li>
        <div id="28" xdh:onevent="Play" class="anchor A5"></div>
        <span id="27" xdh:onevent="Play" class="Gs5 Ab5"></span>
      </li>
      <li>
        <div id="30" xdh:onevent="Play" class="anchor B5"></div>
        <span id="29" xdh:onevent="Play" class="As5 Bb5"></span>
      </li>
      <li>
        <div id="31" xdh:onevent="Play" class="anchor C6"></div>
      </li>
      <li>
        <div id="33" xdh:onevent="Play" class="anchor D6"></div>
        <span id="32" xdh:onevent="Play" class="Cs6 Db6"></span>
      </li>
      <li>
        <div id="35" xdh:onevent="Play" class="anchor E6"></div>
        <span id="34" xdh:onevent="Play" class="Ds6 Eb6"></span>
      </li>
    </ul>
  </fieldset>
  <fieldset style="display: flex; justify-content: space-around">
    <select id="Target" xdh:onevent="SwitchTarget">
      <option value="Buzzer">Buzzer</option>
      <option value="Loudspeaker">Loudspeaker</option>
    </select>
    <label style="display: flex;">
      <span>Ratio: </span>
      <input id="RatioSlide" xdh:onevent="SetRatio" type="range" min="0" max="1" step=".025" value=".5">
      <span>&nbsp;</span>
      <input id="RatioValue" xdh:onevent="SetRatio" type="number" min="0" max="1" step=".025" value="0.5">
    </label>
  </fieldset>
</fieldset>
"""

atlastk.launch(globals=globals())

