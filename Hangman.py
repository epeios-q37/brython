import os, sys, zlib, base64

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk, ucuq

from random import randint

L_FR = 0
L_EN = 1

LANGUAGE = L_FR

L10N = (
  (
    "Vous êtes à court d'essais !",
    "You've run out of guesses!",
  ),
  (
    "Vous avez fait {errors} erreurs et trouvé {correct} bonnes lettres.",
    "You had {errors} errors and {correct} correct guesses."
  ),
  (
    "Le mot était '{}'.",
    "The world was '{}'."
  ),
  (
    "Bravo !",
    "Congratulations!"
  ),
  (
    "Vous avez gagné ! Félicitations !",
    "You've won! Congratulations!"
  ),
  # 5
  (
    "Recommencer",
    "Restart"
  )
)

getL10N = lambda m, *args, **kwargs: L10N[m][LANGUAGE].format(*args, **kwargs)

DICTIONARY_EN = (
  "apple", "banana", "grape", "orange", "mango", "peach", "pineapple", "strawberry",
  "blueberry", "blackberry", "kiwi", "melon", "pear", "plum", "cherry", "coconut",
  "watermelon", "papaya", "apricot", "lemon", "lime", "pomegranate", "fig", "date",
  "tomato", "cucumber", "carrot", "potato", "onion", "garlic", "pepper", "spinach",
  "lettuce", "broccoli", "cabbage", "celery", "zucchini", "eggplant", "beet", "radish",
  "turnip", "squash", "pumpkin", "asparagus", "artichoke", "parsley", "basil", "oregano",
  "cilantro", "thyme", "rosemary", "sage", "chili", "cinnamon", "ginger", "nutmeg",
  "vanilla", "peppermint", "cardamom", "anise", "clove", "fennel", "cumin", "coriander",
  "mustard", "sesame", "sunflower", "almond", "walnut", "pecan", "hazelnut", "cashew",
  "pistachio", "peanut", "grain", "barley", "oat", "wheat", "rice", "quinoa",
  "corn", "millet", "sorghum", "rye", "buckwheat", "spelt", "farro", "teff",
  "chickpea", "lentil", "kidney", "blackbean", "soybean", "pinto", "tofu", "tempeh",
  "seitan", "vegan", "vegetarian", "carnivore", "omnivore", "sustainable", "organic"
)

DICTIONARY_FR = (
  "abondant", "bateau", "chien", "dormir", "fleur", "gantier", "hiver",
  "jardin", "kiwi", "lune", "maison", "nuage", "oiseau", "plage",
  "quai", "rire", "soleil", "table", "usine", "verre", "wagon", "hippopotame",
  "arbre", "bonheur", "ciel", "danse", "feuille", "guitare", "herbe",
  "insecte", "jouet", "livre", "montagne", "neige", "glacier", "pluie",
  "question", "sable", "train", "univers", "vent", "whisky", "avion",
  "ballon", "chapeau", "drapeau", "foret", "glace", "horloge", "igloo",
  "kayak", "lampe", "musique", "nuit", "papillon", "radio", "stylo",
  "voiture", "amour", "biscuit", "cacao", "dent", "fromage", "graine",
  "hibou", "image", "jupe", "koala", "lait", "miel", "orange", "pomme",
  "quiche", "rose", "sucre", "tomate", "violon", "yaourt", "abeille",
  "banane", "carotte", "dauphin", "fraise", "gorille", "hamster",
  "igname", "jonquille", "kiosque", "lavande", "mouton", "narcisse",
  "poire", "renard", "serpent", "tulipe", "valise", "wasabi", "xylophone",
  "yoga", "zeste", "abricot", "bambou", "cactus", "dahlia", "framboise",
  "gantier", "hautbois", "jardinier", "kiosquier", "laurier", "magnolia",
  "mouvement", "nation", "nature", "nuageux", "paysage", "chasseur", "petit",
  "pouvoir", "rapport", "region", "ramification", "retour", "cauchemar", "rivage",
  "saison", "sang", "sauvetage", "secours", "sentier", "film", "service",
  "situation", "village", "spectacle", "sport", "station", "style", "appareil",
  "tendance", "terrain", "concert", "tourisme", "travail", "tribunal", "colifichet"
)

DICTIONARY = DICTIONARY_FR if LANGUAGE == L_FR else DICTIONARY_EN

HANGED_MAN = "Head Body LeftArm RightArm LeftLeg RightLeg".split()

unpack = lambda data : zlib.decompress(base64.b64decode(data)).decode()

START_PATTERN = unpack("eJwzMDBPA4NUAyBAZpsZGMApOrENRtmjbNqw03AAACZsma8=")

HANGED_MAN_PATTERNS = (
  unpack("eJwzMDBPA4NUAyBAZpsZGMApKrPTEGzjtGQ429wgFc42A9MQdrKBMUlsZL3IZiLbhewGJAeOsocpOw0HAAAjmpxP"),
  unpack("eJwzMDBPA4NUAyBAZpsZGMApKrPTEGzjtGQ429wgFc42A9MQdrKBMUlsZL3IZiLbhewGmvhxsLENRjY7DQcAANVInME="),
  unpack("eJzl0EEKgDAMRNErjRSS3ic09z+CUiH+TUFBV84mb9FOQyXPmaEjtEk1XnZebhll1yjbnKdD7ZF5l518izvc2tnpjjPoNIMbvHV0Bmyf/jOtfzsX2QG1wJ1J"),
  unpack("eJzlkDEOwCAMA79khGTyH0T+/4SitApeGJDaqV58C+YUoHlkYEaZQNbL7Iur9+SGkczomzvqEetb3dS/1OHUubitTa5NUpyZPsVY7OE6q+dwiH54Z2X8m32TC+KXnfY="),
  unpack("eJzF0EEKwCAMBMAvbQhE/yPm/0+oWInbYg9CS3PJXIybAMl7VbRiGxDtZfu0egkn1LD1frpAt8xveSb/xRl2M4vnOdPmTDPKbJFHskke1tZKDO5BP7xzIkteG3QTutvVSo5dbo69xuOl8Zf9oQ5w1p6c"),
  unpack("eJy9kEEOwCAIBL+0hoTS9xj5/xNqbAN70INJIxfmoMsAcPmohl7MCkT7mT1ZvAZfaME6+ssVssX8lzN5FjvsOhe3zNTMVCVnDZ9iWuxj6a1G8BA9c+dy25QF5E93W9y/LxK7MMt4lsN1wiDB4+yLegALt59A"),
)

HAPPY_PATTERN = "03c00c30181820044c32524a80018001824181814812442223c410080c3003c0"


class Core:
  def reset(self):
    self.errors = 0
    self.correctGuesses = []
    self.secretWord = ""
    self.chosen = ""

  def __init__(self):
    self.reset()


def randword():
  return DICTIONARY[randint(0, len(DICTIONARY)-1)]


def normalize(string):
  if len(string) < 16:
    return string.ljust(16)
  else:
    return string[-16:]
  

def isWokwi():
  return ringCount == 16


COUNTER_LEDS = {
  True: ((7,9),(6,10),(5,11),(3,13),(2,14),(1,15)),
  False: ((5,),(6,),(7,),(1,),(2,),(3,))
}


FIXED_LEDS = {
  True: (0,4,8,12),
  False: (4,0)
}


def patchRingIndex(index):
  return ( index + ringOffset ) % ringCount


async def showHanged(dom, errors):
  if (errors):
    cOLED.draw(HANGED_MAN_PATTERNS[errors-1],48, ox=47).show()
    await dom.removeClass(HANGED_MAN[errors-1], "hidden")

  for e in range(errors+1):
    for l in COUNTER_LEDS[isWokwi()][e-1]:
      cRing.setValue(patchRingIndex(l), [ringLimiter, 0, 0])

  for e in range(errors+1, 7):
    for l in COUNTER_LEDS[isWokwi()][e-1]:
      cRing.setValue(patchRingIndex(l), [0, ringLimiter, 0])

  for l in FIXED_LEDS[isWokwi()]:
    cRing.setValue(patchRingIndex(l), [ringLimiter * errors // 6, 0, ringLimiter * ( 6 - errors ) // 6])

  cRing.write()


async def showWord(dom, secretWord, correctGuesses):
  output = ("_" * len(secretWord))
  
  for i in range(len(secretWord)):
    if secretWord[i] in correctGuesses:
      output = output[:i] + secretWord[i] + output[i + 1:]

  cLCD.moveTo(0,0).putString(output.center(16))

  html = atlastk.createHTML()
  html.putTagAndValue("h1", output)
  await dom.inner("output", html)


async def reset(core, dom):
  core.reset()
  await dom.inner("", BODY.format(restart=getL10N(5)))
  core.secretWord = randword()
  print(core.secretWord)
  cOLED.fill(0).draw(START_PATTERN, 48, ox=47).show()
  await showWord(dom, core.secretWord, core.correctGuesses)
  cLCD.moveTo(0,1).putString(normalize(""))
#  cRing.fill([0,0,0]).setValue(0,[0,ringLimiter,0]).write()
  await showHanged(dom, 0)


async def atk(core, dom):
  global cLCD, cOLED, cRing, cBuzzer, ringCount, ringOffset, ringLimiter

  infos = await ucuq.ATKConnectAwait(dom, "")
  hardware = ucuq.getKitHardware(infos)

  cLCD = ucuq.HD44780_I2C(ucuq.I2C(*ucuq.getHardware(hardware, "LCD", ["SDA", "SCL", "Soft"])), 2, 16)
  cOLED =  ucuq.SSD1306_I2C(128, 64, ucuq.I2C(*ucuq.getHardware(hardware, "OLED", ["SDA", "SCL", "Soft"])))
  cBuzzer = ucuq.PWM(*ucuq.getHardware(hardware, "Buzzer", ["Pin"]), freq=50, u16 = 0).setNS(0)
  pin, ringCount, ringOffset, ringLimiter = ucuq.getHardware(hardware, "Ring", ["Pin", "Count", "Offset", "Limiter"])
  cRing = ucuq.WS2812(pin, ringCount)

  await reset(core,dom)


async def atkSubmit(core, dom, id):
  await dom.addClass(id, "chosen")

  guess = id.lower()
  core.chosen += guess

  if guess in core.secretWord:
    core.correctGuesses.append(guess)

    correct = 0

    for i in range(len(core.secretWord)):
      if core.secretWord[i] in core.correctGuesses:
        correct += 1

    await showWord(dom, core.secretWord, core.correctGuesses)

    if correct == len(core.secretWord):
      cLCD.moveTo(0,1).putString(getL10N(3))
      cOLED.draw(HAPPY_PATTERN, 16, mul=4, ox=32).show()
      for _ in range(3):
        for l in range(ringCount):
          cRing.setValue(patchRingIndex(l),[randint(0,ringLimiter // 3),randint(0,ringLimiter // 3),randint(0,ringLimiter // 3)]).write()
          ucuq.sleep(0.075)
      await dom.alert(getL10N(4))
      await reset(core, dom)
      return
  else:
    core.errors += 1
    await showHanged(dom, core.errors)
    cLCD.moveTo(0,1).putString(normalize(''.join([char for char in core.chosen if char not in core.correctGuesses])))
    cBuzzer.setFreq(30).setU16(50000)
    ucuq.sleep(0.5)
    cBuzzer.setU16(0)

  
  if core.errors >= len(HANGED_MAN):
    await dom.removeClass("Face", "hidden")
    await showWord(dom, core.secretWord, core.secretWord)
    await dom.alert(f"{getL10N(0)}\n{getL10N(1, errors=core.errors, correct=len(core.correctGuesses))}\n\n{getL10N(2,core.secretWord)}")
    await reset(core, dom)


async def atkRestart(core, dom):
  if (core.secretWord != "" ):
    await dom.alert(f"{getL10N(1, errors=core.errors, correct=len(core.correctGuesses))}\n\n{getL10N(2,core.secretWord)}")

  await reset(core, dom)

ATK_USER = Core

ATK_HEAD = """
<title>Hangman with the Atlas toolkit</title>
<link rel="icon" type="image/png"
    href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgBAMAAACBVGfHAAAAMFBMVEUEAvyEhsxERuS8urQsKuycnsRkYtzc2qwUFvRUVtysrrx0ctTs6qTMyrSUksQ0NuyciPBdAAABHklEQVR42mNgwAa8zlxjDd2A4POfOXPmzZkFCAH2M8fNzyALzDlzg2ENssCbMwkMOsgCa858YOjBKxBzRoHhD7LAHiBH5swCT9HQ6A9ggZ4zp7YCrV0DdM6pBpAAG5Blc2aBDZA68wCsZPuZU0BDH07xvHOmAGKKvgMP2NA/Zw7ADIYJXGDgLQeBBSCBFu0aoAPYQUadMQAJAE29zwAVWMCWpgB08ZnDQGsbGhpsgCqBQHNfzRkDEIPlzFmo0T5nzoMovjPHoAK8Zw5BnA5yDosDSAVYQOYMKIDZzkoDzagAsjhqzjRAfXTmzAQgi/vMQZA6pjtAvhEk0E+ATWRRm6YBZuScCUCNN5szH1D4TGdOoSrggtiNAH3vBBjwAQCglIrSZkf1MQAAAABJRU5ErkJggg==" />
<style type="text/css">
    #Keyboard text {
        font-style: normal;
        font-weight: normal;
        font-size: 61.80482101px;
        font-family: Arial;
        text-anchor: middle;
        stroke-width: 4.41463029pt
    }

    #Keyboard :not(.chosen) text {
        fill: rgb(0, 0, 0);
    }

    #Keyboard g:not(.chosen) {
        cursor: pointer;
    }

    #Keyboard g:active {
        filter: invert(100%);
    }

    .hidden {
        display: none;
    }

    .chosen {
        cursor: not-allowed;
    }

    .chosen text {
        fill:red;
    }

    h1 {
        margin: 0;
        font-family: monospace;
        letter-spacing: 5px;
    }
</style>
"""

BODY = """
<fieldset>
  <div style="display: table; margin: 10px auto auto auto;">
    <svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#"
      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg"
      xmlns="http://www.w3.org/2000/svg" id="master-artboard" viewBox="0 0 212.32262 296.85388" version="1.1" x="0px"
      y="0px" width="212.32262" height="296.85388">
      <defs id="defs4026" />
      <rect id="ee-background" x="-124.85162" y="-7.7507467" width="497.996" height="348.5972"
        style="fill:#ffffff;fill-opacity:0" />
      <metadata id="metadata7">
        <rdf:RDF>
          <cc:Work rdf:about="">
            <dc:format>image/svg+xml</dc:format>
            <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
            <dc:title></dc:title>
          </cc:Work>
        </rdf:RDF>
      </metadata>
      <path
        style="fill:#ffffff;fill-opacity:1;stroke:#000000;stroke-width:2.08117723;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
        id="Head" d="m 185.43265,81.702921 a 20.551628,20.551631 0 0 1 -41.1032,0 20.551628,20.551631 0 1 1 41.1032,0 z"
        class="hidden" />
      <path
        style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2.08117723;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
        d="m 147.20715,116.82761 -28.3463,49.09718" id="RightArm" class="hidden" />
      <path id="LeftArm" d="m 182.00845,116.25614 28.3462,49.09718"
        style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2.08117723;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
        class="hidden" />
      <path
        style="fill:#ffffff;fill-opacity:1;stroke:#000000;stroke-width:2.08117723;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
        id="Body" d="m 190.73095,154.51911 a 25.754572,51.769291 0 0 1 -51.5091,0 25.754572,51.769291 0 1 1 51.5091,0 z"
        class="hidden" />
      <path
        style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2.08117723;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
        d="m 182.55495,195.13924 28.3462,49.09718" id="LeftLeg" class="hidden" />
      <path id="RightLeg" d="m 147.91815,195.13924 -28.3462,49.09718"
        style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2.08117723;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
        class="hidden" />
      <g transform="matrix(0.35571142,0,0,0.35571142,-124.85164,-7.7507687)" id="Gallow">
        <g id="g10119" transform="matrix(2.9253731,0,0,2.9253731,56.181525,-337.2678)">
          <path id="path6224" d="m 102.14286,406.6479 43.05105,-24.85554"
            style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
          <path
            style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
            d="M 189.19391,406.6479 146.14286,381.79236" id="path7195" />
        </g>
        <path transform="matrix(2.9253731,0,0,2.9253731,18.569584,-335.17825)"
          style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
          d="m 158.52553,380.78033 0,-257.70387" id="path8175" />
        <path transform="matrix(2.9253731,0,0,2.9253731,18.569584,-335.17825)"
          style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
          d="m 158.52553,123.07646 111.42857,0" id="path9146" />
        <path id="path10117" d="m 814.5161,24.866309 0,162.985051"
          style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:5.85099983;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
        <path transform="matrix(2.9253731,0,0,2.9253731,18.569584,-335.17825)"
          style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
          d="m 159.07114,162.2035 38.76461,-38.7646" id="path10123" />
      </g>
      <g transform="matrix(0.35571142,0,0,0.35571142,-124.85164,-7.7507687)" id="Face" class="hidden">
        <g transform="translate(3.2131215,0)" id="g4883">
          <ellipse
            style="opacity:1;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
            id="path4037" cx="785.99969" cy="234.55737" rx="5.2213116" ry="4.8196721" />
          <ellipse ry="4.8196721" rx="5.2213116" cy="233.75409" cx="836.60626" id="ellipse4847"
            style="opacity:1;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" />
        </g>
        <path id="path4871" d="m 796.04789,285.16393 c 19.35395,-26.01272 36.88635,-0.94937 36.88635,-0.94937 l 0,0"
          style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:5.85099983;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
      </g>
    </svg>
  </div>
  <div style="display: table; margin: 10px auto auto auto;">
    <fieldset id="output">
      <h1>&nbsp;</h1>
    </fieldset>
  </div>
  <div style="display: table; margin: 10px auto auto auto;">
    <svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#"
      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg"
      xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="302.13028" height="160.89368"
      version="1.1" id="Keyboard">
      <metadata id="metadata32">
        <rdf:RDF>
          <cc:Work rdf:about="">
            <dc:format>image/svg+xml</dc:format>
            <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
            <dc:title></dc:title>
          </cc:Work>
        </rdf:RDF>
      </metadata>
      <defs id="defs19">
        <linearGradient id="linearGradient607">
          <stop stop-color="#cfcfcf" offset="0" id="stop608" />
          <stop stop-color="#efefef" offset="1" id="stop609" />
        </linearGradient>
        <linearGradient id="linearGradient565">
          <stop stop-color="#9d9d9f" offset="0" id="stop566" />
          <stop stop-color="#e5e5e5" offset="1" id="stop567" />
        </linearGradient>
        <radialGradient xlink:href="#linearGradient565" spreadMethod="repeat" r="1.0161459" id="radialGradient568"
          fy="0.49218801" fx="0.47153401" cy="0.49218801" cx="0.47153401" />
        <linearGradient y2="-0.037312999" y1="0.99253702" xlink:href="#linearGradient565" x2="0.72092998"
          x1="-0.085270002" spreadMethod="pad" id="linearGradient569" gradientUnits="objectBoundingBox" />
        <linearGradient y2="0" y1="0.99253702" xlink:href="#linearGradient565" x2="-0.046512" x1="-0.0077530001"
          spreadMethod="pad" id="linearGradient580" gradientUnits="objectBoundingBox" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient576" />
        <linearGradient y2="0.122951" y1="0.86885202" xlink:href="#linearGradient607" x2="0.78280503" x1="0.117647"
          spreadMethod="pad" id="linearGradient610" gradientUnits="objectBoundingBox" />
        <linearGradient y2="0.28125" y1="0.94531298" xlink:href="#linearGradient565" x2="0.76847303" x1="0.108374"
          spreadMethod="pad" id="linearGradient611" gradientUnits="objectBoundingBox" />
        <linearGradient y2="33.863163" y1="113.68299" xlink:href="#linearGradient607" x2="112.68261" x1="47.562195"
          spreadMethod="pad" id="linearGradient613" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" />
        <linearGradient y2="15.428203" y1="123.06186" xlink:href="#linearGradient565" x2="129.09589" x1="17.322577"
          spreadMethod="pad" id="linearGradient615" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient620"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073"
          gradientUnits="userSpaceOnUse" />
        <linearGradient gradientTransform="scale(1.0317925,0.96918716)" y2="15.428203" y1="123.06186"
          xlink:href="#linearGradient565" x2="129.09589" x1="17.322577" spreadMethod="pad" id="linearGradient615-5"
          gradientUnits="userSpaceOnUse" />
        <linearGradient gradientTransform="scale(1.0027892,0.99721857)" y2="33.863163" y1="113.68299"
          xlink:href="#linearGradient607" x2="112.68261" x1="47.562195" spreadMethod="pad" id="linearGradient613-3"
          gradientUnits="userSpaceOnUse" />
        <linearGradient gradientUnits="userSpaceOnUse" y2="20.13073" x2="131.57249" y1="20.13073" x1="21.713028"
          gradientTransform="scale(1.0027892,0.99721857)" xlink:href="#linearGradient607" id="linearGradient620-0" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6170" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6172" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6174" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6202" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6204" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6206" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6234" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6236" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6238" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6266" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6268" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6270" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6298" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6300" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6302" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6625" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6627" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6629" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6631" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6633" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6635" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6637" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6639" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6641" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6643" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6645" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6647" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6649" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6651" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6653" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6655" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6657" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6659" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6661" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6663" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6665" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6988" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6990" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6992" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient6994" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6996" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient6998" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7000" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7002" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7004" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7006" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7008" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7010" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7012" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7014" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7016" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7018" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7020" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7022" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7024" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7026" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7028" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7357" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7359" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7361" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7363" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7365" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7367" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7369" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7371" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7373" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7375" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7377" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7379" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
        <linearGradient xlink:href="#linearGradient565" id="linearGradient7381" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0317925,0.96918716)" x1="17.322577" y1="123.06186" x2="129.09589" y2="15.428203"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7383" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="47.562195" y1="113.68299" x2="112.68261" y2="33.863163"
          spreadMethod="pad" />
        <linearGradient xlink:href="#linearGradient607" id="linearGradient7385" gradientUnits="userSpaceOnUse"
          gradientTransform="scale(1.0027892,0.99721857)" x1="21.713028" y1="20.13073" x2="131.57249" y2="20.13073" />
      </defs>
      <g id="A" transform="matrix(0.28785058,0,0,0.28785058,-0.5224919,-1.1433585)" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621" height="139.46495"
          style="fill:url(#linearGradient615);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622" height="107.05391"
          style="fill:url(#linearGradient613);fill-rule:evenodd;stroke:url(#linearGradient620);stroke-width:2.5" />
        <text font-style="normal" font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637">A</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,42.549418,-1.1433585)" id="B" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-0" height="139.46495"
          style="fill:url(#linearGradient615-5);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-7"
          height="107.05391"
          style="fill:url(#linearGradient613-3);fill-rule:evenodd;stroke:url(#linearGradient620-0);stroke-width:2.5" />
        <text font-style="normal" font-weight="normal" font-size="14" y="95.374039" x="76.735825"
          id="text637-4">B</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,85.621338,-1.1433585)" id="C" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-4" height="139.46495"
          style="fill:url(#linearGradient6298);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-1"
          height="107.05391"
          style="fill:url(#linearGradient6300);fill-rule:evenodd;stroke:url(#linearGradient6302);stroke-width:2.5" />
        <text font-style="normal" font-weight="normal" font-size="14" y="95.374039" x="76.735825"
          id="text637-3">C</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,128.69326,-1.1433585)" id="D" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-5" height="139.46495"
          style="fill:url(#linearGradient6170);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-6"
          height="107.05391"
          style="fill:url(#linearGradient6172);fill-rule:evenodd;stroke:url(#linearGradient6174);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-6">D</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,171.76517,-1.1433585)" id="E" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-9" height="139.46495"
          style="fill:url(#linearGradient6202);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-4"
          height="107.05391"
          style="fill:url(#linearGradient6204);fill-rule:evenodd;stroke:url(#linearGradient6206);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-2">E</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,214.83709,-1.1433585)" id="F" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-8" height="139.46495"
          style="fill:url(#linearGradient6234);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-47"
          height="107.05391"
          style="fill:url(#linearGradient6236);fill-rule:evenodd;stroke:url(#linearGradient6238);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-44">F</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,257.90896,-1.1433585)" id="G" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-1" height="139.46495"
          style="fill:url(#linearGradient6266);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-77"
          height="107.05391"
          style="fill:url(#linearGradient6268);fill-rule:evenodd;stroke:url(#linearGradient6270);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-8">G</text>
      </g>
      <g id="H" transform="matrix(0.28785058,0,0,0.28785058,-0.2090919,39.001711)" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-7" height="139.46495"
          style="fill:url(#linearGradient6625);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-8"
          height="107.05391"
          style="fill:url(#linearGradient6627);fill-rule:evenodd;stroke:url(#linearGradient6629);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-0">H</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,42.862828,39.001711)" id="I" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-0-3" height="139.46495"
          style="fill:url(#linearGradient6631);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-7-6"
          height="107.05391"
          style="fill:url(#linearGradient6633);fill-rule:evenodd;stroke:url(#linearGradient6635);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-4-8">I</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,85.934748,39.001711)" id="J" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-4-6" height="139.46495"
          style="fill:url(#linearGradient6637);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-1-4"
          height="107.05391"
          style="fill:url(#linearGradient6639);fill-rule:evenodd;stroke:url(#linearGradient6641);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-3-3">J</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,129.00667,39.001711)" id="K" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-5-7" height="139.46495"
          style="fill:url(#linearGradient6643);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-6-7"
          height="107.05391"
          style="fill:url(#linearGradient6645);fill-rule:evenodd;stroke:url(#linearGradient6647);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-6-3">K</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,172.07858,39.001711)" id="L" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-9-1" height="139.46495"
          style="fill:url(#linearGradient6649);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-4-7"
          height="107.05391"
          style="fill:url(#linearGradient6651);fill-rule:evenodd;stroke:url(#linearGradient6653);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-2-5">L</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,215.1505,39.001711)" id="M" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-8-1" height="139.46495"
          style="fill:url(#linearGradient6655);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-47-2"
          height="107.05391"
          style="fill:url(#linearGradient6657);fill-rule:evenodd;stroke:url(#linearGradient6659);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-44-2">M</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,258.22236,39.001711)" id="N" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-1-5" height="139.46495"
          style="fill:url(#linearGradient6661);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-77-9"
          height="107.05391"
          style="fill:url(#linearGradient6663);fill-rule:evenodd;stroke:url(#linearGradient6665);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-8-8">N</text>
      </g>
      <g id="O" transform="matrix(0.28785058,0,0,0.28785058,0.1043281,79.146771)" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-7-4" height="139.46495"
          style="fill:url(#linearGradient6988);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-8-7"
          height="107.05391"
          style="fill:url(#linearGradient6990);fill-rule:evenodd;stroke:url(#linearGradient6992);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-0-8">O</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,43.176248,79.146771)" id="P" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-0-3-8" height="139.46495"
          style="fill:url(#linearGradient6994);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-7-6-7"
          height="107.05391"
          style="fill:url(#linearGradient6996);fill-rule:evenodd;stroke:url(#linearGradient6998);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-4-8-0">P</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,86.248158,79.146771)" id="Q" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-4-6-1" height="139.46495"
          style="fill:url(#linearGradient7000);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-1-4-9"
          height="107.05391"
          style="fill:url(#linearGradient7002);fill-rule:evenodd;stroke:url(#linearGradient7004);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-3-3-7">Q</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,129.32008,79.146771)" id="R" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-5-7-4" height="139.46495"
          style="fill:url(#linearGradient7006);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-6-7-9"
          height="107.05391"
          style="fill:url(#linearGradient7008);fill-rule:evenodd;stroke:url(#linearGradient7010);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-6-3-4">R</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,172.39199,79.146771)" id="S" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-9-1-9" height="139.46495"
          style="fill:url(#linearGradient7012);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-4-7-9"
          height="107.05391"
          style="fill:url(#linearGradient7014);fill-rule:evenodd;stroke:url(#linearGradient7016);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-2-5-0">S</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,215.46391,79.146771)" id="T" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-8-1-0" height="139.46495"
          style="fill:url(#linearGradient7018);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-47-2-9"
          height="107.05391"
          style="fill:url(#linearGradient7020);fill-rule:evenodd;stroke:url(#linearGradient7022);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-44-2-8">T</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,258.53586,79.146771)" id="U" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-1-5-4" height="139.46495"
          style="fill:url(#linearGradient7024);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-77-9-2"
          height="107.05391"
          style="fill:url(#linearGradient7026);fill-rule:evenodd;stroke:url(#linearGradient7028);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-8-8-1">U</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,43.489648,119.29184)" id="V" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-0-3-8-9" height="139.46495"
          style="fill:url(#linearGradient7357);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-7-6-7-6"
          height="107.05391"
          style="fill:url(#linearGradient7359);fill-rule:evenodd;stroke:url(#linearGradient7361);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-4-8-0-5">V</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,86.561568,119.29184)" id="W" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-4-6-1-9" height="139.46495"
          style="fill:url(#linearGradient7363);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-1-4-9-1"
          height="107.05391"
          style="fill:url(#linearGradient7365);fill-rule:evenodd;stroke:url(#linearGradient7367);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-3-3-7-0">W</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,129.63349,119.29184)" id="X" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-5-7-4-1" height="139.46495"
          style="fill:url(#linearGradient7369);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-6-7-9-8"
          height="107.05391"
          style="fill:url(#linearGradient7371);fill-rule:evenodd;stroke:url(#linearGradient7373);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-6-3-4-8">X</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,172.70541,119.29184)" id="Y" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-9-1-9-4" height="139.46495"
          style="fill:url(#linearGradient7375);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-4-7-9-1"
          height="107.05391"
          style="fill:url(#linearGradient7377);fill-rule:evenodd;stroke:url(#linearGradient7379);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-2-5-0-4">Y</text>
      </g>
      <g transform="matrix(0.28785058,0,0,0.28785058,215.77732,119.29184)" id="Z" xdh:onevent="Submit">
        <rect y="4.516449" x="2.3595431" width="148.54411" ry="20.669067" id="rect621-8-1-0-8" height="139.46495"
          style="fill:url(#linearGradient7381);fill-rule:evenodd;stroke:#acb0b0;stroke-width:0.81659004pt" />
        <rect y="21.324738" x="23.02359" width="107.66589" ry="10.325302" rx="7.5169368" id="rect622-47-2-9-3"
          height="107.05391"
          style="fill:url(#linearGradient7383);fill-rule:evenodd;stroke:url(#linearGradient7385);stroke-width:2.5" />
        <text font-weight="normal" font-size="14" y="95.374039" x="76.735825" id="text637-44-2-8-4">Z</text>
      </g>
    </svg>
  </div>
  <div style="display: table; margin: 10px auto auto auto;">
    <button xdh:onevent="Restart">{restart}</button>
  </div>
</fieldset>
"""

atlastk.launch(globals=globals())

