import ucuq, atlastk

async def atk(dom):
  await ucuq.ATKConnectAwait(dom, BODY)
  
async def atkSwitch(dom, id):
  ucuq.GPIO(2).high(await dom.getValue(id) == "true")

ATK_HEAD = """
<title>UCUq/ATK boilerplate</title>
"""

BODY = """
<fieldset>
  <label>
    <span>On/off:&nbsp;</span>
    <input type="checkbox" xdh:onevent="Switch">
  </label>
</fieldset>
"""

atlastk.launch(globals=globals())

