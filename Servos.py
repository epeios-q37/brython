import os, io, json, datetime
import ucuq, atlastk

async def getGithubFileContentAwait(file_path):
  return await ucuq.getWebFileContentAwait(f'https://raw.githubusercontent.com/epeios-q37/ucuq-python/refs/heads/main/{file_path}')

MACRO_MARKER_ = '$'

DEFAULT_SPEED = 10

contentsHidden = True

show = {}
macros = {}

# Hardware modes
M_STRAIGHT = "Straight"
M_PCA ="PCA"
M_KIT ="Kit"

# Config keys
HARDWARE_KEY = "Hardware"
HARDWARE_MODE_SUBKEY = "Mode"
SPECS_KEY = "Specs"
TWEAK_KEY = "Tweak"

STEP = int(1625 / 180)


MACRO_HTML="""
<div class="macro" xdh:mark="Macro{}" style="margin-bottom: 3px;">
  <label>
    <span>Name:&nbsp;</span>
    <input disabled="disabled" value="{}">
  </label>
  <label>
    <span>Desc.:&nbsp;</span>
    <input disabled="disabled" value="{}">
  </label>
  <div>
    <button xdh:onevent="Execute">Execute</button>
  </div>
  <textarea class="description" disabled="disabled">{}</textarea>
  <div class="description">
    <button xdh:onevent="Edit">Edit</button>
    <button xdh:onevent="Delete">Delete</button>
  </div>
</div>
"""

servos = {}
devices = []


def reset_():
  moves = []
  for servo in servos.values():
    moves.append([servo, 0])

  ucuq.servoMoves(moves, int(2 * STEP * DEFAULT_SPEED))


async def displayMacros(dom):
  html = "<legend>Macros</legend><div>"

  if len(macros) >= 1:
    for macro in macros:
      if macro != '_':
        html += MACRO_HTML.format(macro, macro, macros[macro]["Description"], macros[macro]["Content"])
  else:
    html += "<em>No macros available</em>"

  html += "</div>"

  await dom.inner("Macros", html)


SOLOS = {
  "Bipedal": "Freenove/Bipedal/RPiPico(2)W",
  "DIY": "q37.info/Servos/180°",
  "Dog": "Freenove/Dog/ESP32"
}

COHORTS = ["Cats"]

async def updateFileList(dom, soloId = ""):
  html = ""

  for solo in SOLOS:
    html = f"<option value=\"{solo}\" {'selected=\"selected\"' if solo == soloId else ''}>{solo}</option>\n" + html

  await dom.inner("Solos", html)

  html = ""

  for cohort in COHORTS:
    html = f"<option value=\"{cohort}\" >{cohort}</option>\n" + html

  await dom.inner("Cohorts", html)


async def atk(dom):
  infos = await ucuq.ATKConnectAwait(dom, BODY)

  # await createCohortServos()

  await createServoAwait(ucuq.getDeviceId(infos), ucuq.getDevice(), infos, "")

  await displayMacros(dom)
  kitLabel =  ucuq.getKitLabel(infos)

  await updateFileList(dom, next((key for key, val in SOLOS.items() if val == kitLabel), None))


async def atkTest():
  reset_()
  step = int(STEP * DEFAULT_SPEED / 2)
  for servo in servos:
    ucuq.servoMoves([[servos[servo], 15]], step)
    ucuq.servoMoves([[servos[servo], -15]], step)
    ucuq.servoMoves([[servos[servo], 0]], step)
  

async def atkReset(dom):
  reset_()


def getToken(stream):
  token = ""

  char = stream.read(1)

  while char and char == ' ':
    char = stream.read(1)

  pos = stream.tell()

  while char and char != ' ':
    token += char
    char = stream.read(1)

  if token:
    return (token, pos)
  else:
    return None
  

def getMacro(token):
  name = ""
  amount = 1

  with io.StringIO(token[0]) as stream:
    if not ( char := stream.read(1) ):
      raise Exception(f"Unexpected error ({token[1]})!")
    
    if char.isdigit():
      amount = int(char)

      while ( char := stream.read(1) ) and char .isdigit():
        amount = amount * 10 + int(char)

    if char != MACRO_MARKER_:
      raise Exception(f"Missing macro reference ({token[1]})!")
    
    if not (char := stream.read(1)):
      raise Exception(f"Empty macro name ({token[1]})!")
    
    if not char.isalpha(): 
      raise Exception(f"Macro name must beginning with a letter ({token[1]})!")
    
    while char and char.isalnum():
      name += char
      char = stream.read(1)

    if char:
      raise Exception(f"Unexpected character after macro call ({token[1]})!")

  if not name in macros:
    raise Exception(f"Unknown macro ({token[1]})!")

  return {"name": name, "amount" :amount}


def getMoves(token):
  moves = []
  speed = None
  device = ""

  with io.StringIO(token[0]) as stream:
    while char := stream.read(1):
      if not char.isalnum():
        raise Exception(f"Servo id expected ({token[1]})!")
      
      servo = char

      char = stream.read(1)

      while char and ( char.isalnum() or char == '_' ):
        servo += char
        char = stream.read(1)

      if char == '.':
        device = servo

        servo += char

        char = stream.read(1)

        while char and ( char.isalnum() or char == '_' ):
          servo += char
          char = stream.read(1)
      else:
        if device != "":
          servo = device + '.' + servo

      if not servo in servos:
        raise Exception(f"No servo of id '{servo}' ({token[1]})")
        
      angle = 0
      sign = 1

      if char:
        if char in "+-":
          if char == '-':
            sign = -1
          char = stream.read(1)


      while char and char.isdigit():
        angle = angle * 10 + int(char)
        char = stream.read(1)

      moves.append((servos[servo], angle * sign))

      if not char:
        break

      if char != "%":
        if char != ':':
          raise Exception(f"Servo move can only be followed by '%' ({token[1]})!")
      else:
        speed = ""

        while (char := stream.read(1)) and char.isdigit():
          speed += char

        if char:
          raise Exception(f"Unexpected char at end of servo moves ({token[1]})!")
        
    return { "moves": moves, "speed": speed}
  

def getSpeed(token):
  speed = 0

  with io.StringIO(token[0]) as stream:
    if stream.read(1) != '%':
      raise Exception(f"Unexpected error ({token[1]})!")
    
    while (char := stream.read(1)) and char.isdigit():
      speed = speed * 10 + int(char)

  return { "value": speed if speed else DEFAULT_SPEED }


def tokenize(string):
  tokens = []

  with io.StringIO(string) as stream:
    while token := getToken(stream):
      tokens.append(token)

  return tokens


def getAST(tokens):
  ast = []
  for token in tokens:
    if token[0][0].isdigit() or token[0][0] == MACRO_MARKER_:
      ast.append(("macro", getMacro(token)))
    elif token[0][0] == '%':
      ast.append(("speed", getSpeed(token)))
    else:
      ast.append(("action",getMoves(token)))

  return ast


async def execute(dom, string, speed = DEFAULT_SPEED):
  try:
    ast = getAST(tokenize(string))

    for item in ast:
      match item[0]:
        case "action":
          tempSpeed = item[1]["speed"]
          ucuq.servoMoves(item[1]["moves"], int(STEP * ( speed if tempSpeed == None else ( int(tempSpeed) if tempSpeed != "" else DEFAULT_SPEED))))
        case "macro":
          for _ in range(item[1]["amount"]):
            await execute(dom, macros[item[1]["name"]]["Content"], speed)
        case "speed":
          speed = item[1]["value"]
  except Exception as err:
    await dom.alert(err)


async def atkExecute(dom, id):
  mark = await dom.getMark(id)

  if mark == "Buffer":
    moves = await dom.getValue("Content")
    await dom.focus("Content")
  else:
    moves = macros[mark[5:]]["Content"]

  if await dom.getValue("Reset") == "true":
    reset_()

  await execute(dom, moves)


async def atkSave(dom):
  await dom.alert("Not implemented yet in Brython version!")



def expand(moves):
  content = ""
  
  for item in getAST(tokenize(moves)):
    match item[0]:
      case 'action':
        for move in item[1]["moves"]:
          content += move[0] + move[1] + ":"
        content = content[:-1]
        if item[2]:
          content += f"%{item[2]}"
        content += " "
      case 'macro':
        if not ( name := item[1]["name"] ) in macros:
          raise Exception(f"No macro named '{item[1]}!")
        else:
          for _ in range(item[1]["amount"]):
            content += macros[item[1]["name"]]["Content"] + " "

  return content


async def atkExpand(dom):
  try:
    await dom.setValue("Content", expand(await dom.getContent("Content")))
  except Exception as err:
    await dom.alert(err)


async def atkDelete(dom, id):
  name = (await dom.getMark(id))[5:]

  if await dom.confirm(f"Delete macro '{name}'?"):
    del macros[name]
    await displayMacros(dom)


async def atkEdit(dom, id):
  name = (await dom.getMark(id))[5:]

  await dom.setValues({
    "Name": name,
    "Description": macros[name]["Description"],
    "Content": macros[name]["Content"],
    "Ask": "false"
  })


async def atkHideContents(dom):
  global contentsHidden

  contentsHidden = not contentsHidden

  if contentsHidden:
    await dom.enableElement("HideContents")
  else:
    await dom.disableElement("HideContents")

  
async def atkSaveToFile(dom):
  await dom.alert("Not implemented in Brython version!")


async def atkLoadFromFile(dom):
  global show, macros


  show = json.loads(await getGithubFileContentAwait(f"demos/Servos/Shows/{await dom.getValue('Shows')}.json"))

  macros = show["Macros"]

  if "_" in macros:
    await dom.setValue("Content", macros["_"]["Content"])

  await displayMacros(dom)

  if "Cohort" in show:
    await createCohortServosAwait(show["Cohort"])


def handleSetupsKits(setups, infos):
  for setup in setups:
    hardware = setups[setup]["Hardware"]

    if hardware[HARDWARE_MODE_SUBKEY] == M_KIT:
      setups[setup]["Hardware"] = ucuq.getHardware(infos, hardware["Key"], index = hardware["Index"])

  return setups


async def getServosSetups(target, infos):


  config = json.loads(await getGithubFileContentAwait("demos/Servos/servos.json"))[target]


  return handleSetupsKits(config["Servos"], infos)


async def createServoAwait(deviceId, device, infos, key):
  global servos

  if key:
    key += '.'

  setups = await getServosSetups(deviceId, infos)

  for setup in setups:
    servo = setups[setup]
    hardware = servo[HARDWARE_KEY]
    specs = servo[SPECS_KEY]
    tweak = servo[TWEAK_KEY]
    if ( not HARDWARE_MODE_SUBKEY in hardware ) or hardware[HARDWARE_MODE_SUBKEY] == M_STRAIGHT:
      pwm = ucuq.PWM(hardware["Pin"],device=device, freq=50, u16=0).setNS(0)
      pwm.setFreq(specs["Freq"])
    elif hardware[HARDWARE_MODE_SUBKEY] == M_PCA:
      if not pca:
        i2c = ucuq.SoftI2C if hardware["soft"] else ucuq.I2C
        pca = ucuq.PCA9685(i2c(hardware["sda"], hardware["scl"],device=device))
        pca.setFreq(specs["Freq"])
        pca.setOffset(hardware["Offset"])
      pwm = ucuq.PWM_PCA9685(pca, hardware["channel"])
    else:
      raise Exception("Unknown hardware mode!")

    servos[key+setup] = ucuq.Servo(pwm, ucuq.Servo.Specs(specs["U16Min"], specs["U16Max"], specs["Range"]), tweak = ucuq.Servo.Tweak(tweak["Angle"],tweak["Offset"], tweak["Invert"]))


async def createCohortServosAwait(cohort):
  global servos

  servos = {}
  
  for key in cohort:
    device = ucuq.Device(id=cohort[key])
    infos = await ucuq.getInfosAwait(device)

    await createServoAwait(cohort[key], device, infos, key)

ATK_HEAD = """
<style>
.macro {
  display: grid;
  grid-template-columns: 25% 25% 30% 20%;
}

.macro > * {
  margin: 1px;
  display: flex;
}

.macro > label > input {
 width: 100%;
}

.macro > label:nth-child(2) {
  grid-column: span 2;
}

.macro > div > button {
 width: 100%;
}

.macro > textarea {
  grid-column: span 3;
}

.macro > div:nth-last-child(1) {
 flex-direction: column;
}
</style>
<style id="HideContents">
  .description {
    display: none;
  }
</style>
"""

BODY = """
<fieldset style="width: 100%">
  <div style="display:flex; justify-content: space-evenly;">
    <div style="display: flex; flex-direction: column;">
      <button xdh:onevent="Reset">Reset</button>
      <button xdh:onevent="Test">Test</button>
    </div>
    <div style="display: flex; flex-direction: column;">
      <label>
        <input id="Reset" checked="checked" type="checkbox">
        <span>Reset before execute</span>
      </label>
      <label>
        <input id="Ask" type="checkbox">
        <span>Do not ask for confirmation before saving</span>
      </label>
    </div>
  </div>
  <fieldset>
    <legend>Editor</legend>
    <div class="macro" xdh:mark="Buffer">
      <label>
        <span>Name:&nbsp;</span>
        <input id="Name">
      </label>
      <label>
        <span>Desc.:&nbsp;</span>
        <input id="Description" type="text">
      </label>
      <div>
        <button xdh:onevent="Execute">Execute</button>
      </div>
      <textarea id="Content" xdh:onevent="Execute"></textarea>
      <div>
        <button xdh:onevent="Expand">Expand</button>
        <button xdh:onevent="Save">Save</button>
      </div>
    </div>
  </fieldset>
  <div style="margin: 25px 0px 0px 0px; display: flex; justify-content: space-evenly">
    <div>
      <select id="Shows">
        <optgroup id="Solos" label="Solo">
        </optgroup>
        <optgroup id="Cohorts" label="Cohort"></optgroup>
      </select>
      <button xdh:onevent="LoadFromFile">Load</button>
    </div>
    <button xdh:onevent="HideContents">Show/Hide contents</button>
    <button xdh:onevent="SaveToFile">Save to file</button>
  </div>
  <fieldset id="Macros"></fieldset>
</fieldset>
  
"""

atlastk.launch(globals=globals())

