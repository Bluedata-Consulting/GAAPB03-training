from flask import Blueprint, request, jsonify, render_template
from openai import AzureOpenAI, APIError, RateLimitError
import  logging
from .cards import detect_card_type
from .prompt_builder import build_prompt
from .validator import validate_reply

bp = Blueprint("api",__name__)

#rdb = redis.from_url(os.getenv("REDIS_URL","redis://localhost:6379"))

client = AzureOpenAI(timeout=20)

# Azure AI Foundry deployment name
model = "myllm"

## Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)


@bp.route("/chat",methods=['POST'])
def chat():
    msg = request.get_json(force=True)['message']
    if not msg.strip():
        return jsonify({"Error":"empty message"}),400
    
    hist = []  #rdb.lrange("chat",0,-1)
    card = detect_card_type(msg.lower().strip())
    prompt = build_prompt(card, hist, msg)

    try:
        response = client.chat.completions.create(messages=prompt,
                                              model=model, temperature=0.2)
        assistant_res = response.choices[0].message.content

        if not validate_reply(assistant_res):
            logger.warning("format validation failed - sending corrective message")
            prompt.append({"role":"assistant","content":"FORMAT Error Re-answer in layout"})

            assistant_res = client.chat.completions.create(model=model,messages=prompt).choices[0].message.content
        
        return jsonify({"answer":assistant_res})
    except (RateLimitError, APIError) as err:
        logger.error("OpenAI Call failed %s",err)
        return jsonify({"error":"upstream failure"}),502


@bp.route("/")
def mainUI():return render_template("chat.html")