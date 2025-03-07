import atlastk, ucuq, json

async def atk(dom):
  infos = await ucuq.ATKConnectAwait(dom, BODY)
  await dom.setValue("Infos", json.dumps(infos, indent=2))

ATK_HEAD = """

"""

BODY = """
<fieldset>
  <pre id="Infos">(<em>Please wait…)</em></pre>
</fieldset>
"""

atlastk.launch(globals=globals())

