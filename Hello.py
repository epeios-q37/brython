import atlastk
from browser import aio

HEAD = """
<title>Hello, World! | Zelbinium</title>
<link rel="icon" type="image/png" href="https://zelbinium.q37.info/Avatar.png" />
"""

BODY = """
<fieldset>
<input id="input" maxlength="20" placeholder="Enter a name here" type="text"
xdh:onevent="Submit" value="World"/>
<button xdh:onevent="Submit">Submit</button>
<hr/>
<fieldset>
<output id="output"></output>
</fieldset>
</fieldset>
"""
text = ""

async def acConnect(dom):
  # dom.debugLog()
  print("acConnect")
  await dom.inner("", BODY)
  await dom.focus("input")


async def acSubmit(dom):
  global text
  text = await dom.getValue("input")
  atlastk.broadcastAction("Display")
  await dom.setValue("input", "")
  await dom.focus("input")

async def acDisplay(dom):
  await dom.setValue("output", f"Bonjour, {text}!")

CALLBACKS = {
  "": acConnect,
  "Submit": acSubmit,
  "Display": acDisplay
}

atlastk.launch(CALLBACKS, headContent=HEAD)    