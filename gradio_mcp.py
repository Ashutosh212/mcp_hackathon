import requests
import json
import gradio as gr
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# ---------- Load CLIP Model ----------
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# ---------- IGDB POST Helper ----------
def igdb_post(endpoint: str, client_id: str, access_token: str, query: str):
    url = f"https://api.igdb.com/v4/{endpoint}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.post(url, headers=headers, data=query)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ---------- Token Retrieval ----------
def get_igdb_access_token(client_id: str, client_secret: str) -> str:
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    try:
        response = requests.post(url, data=params)
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        return f"❌ Error: {e}"

# ---------- Lookup Helpers ----------
def resolve_lookup(client_id: str, access_token: str, category: str, lookup_id: int) -> str:
    query = f"fields name; where id = {lookup_id}; limit 1;"
    result = igdb_post(category, client_id, access_token, query)
    return result[0]["name"] if result and isinstance(result, list) else str(lookup_id)

def get_gender_name(client_id: str, access_token: str, gender_id: int) -> str:
    return resolve_lookup(client_id, access_token, "character_genders", gender_id)

def get_species_name(client_id: str, access_token: str, species_id: int) -> str:
    return resolve_lookup(client_id, access_token, "character_species", species_id)

# ---------- Character Data ----------
def get_igdb_characters(client_id: str, access_token: str) -> str:
    query = "fields id, name, gender, species, description; limit 10;"
    result = igdb_post("characters", client_id, access_token, query)
    if isinstance(result, dict) and "error" in result:
        return f"❌ {result['error']}"
    return "\n\n".join([
        f"{c['id']}: {c['name']}\n{c.get('description', '')}" for c in result
    ]) or "No characters found."

# ---------- Game & Characters ----------
def search_game_by_name(client_id: str, access_token: str, name: str):
    query = f'search "{name}"; fields id, name, summary, url; limit 1;'
    result = igdb_post("games", client_id, access_token, query)
    return result[0] if isinstance(result, list) and result else None

def get_characters_for_game(client_id: str, access_token: str, game_name: str) -> str:
    game = search_game_by_name(client_id, access_token, game_name)
    if not game:
        return f"❌ Game not found: {game_name}"

    query = f"fields name, description, gender, species, url; where games = ({game['id']}); limit 500;"
    characters = igdb_post("characters", client_id, access_token, query)
    if isinstance(characters, dict) and "error" in characters:
        return f"❌ {characters['error']}"
    if not characters:
        return f"No characters found for '{game['name']}'."

    output = [f"🎮 Game: {game['name']} (ID: {game['id']})\nURL: {game.get('url', '')}\n"]
    for char in characters:
        gender = get_gender_name(client_id, access_token, char.get("gender")) if char.get("gender") else "N/A"
        species = get_species_name(client_id, access_token, char.get("species")) if char.get("species") else "N/A"
        desc = char.get("description", "")
        if len(desc) > 200:
            desc = desc[:200] + "..."
        output.append(f"🧍 {char['name']}\n  Gender: {gender} | Species: {species}\n  {desc}\n")
    return "\n".join(output)

# ---------- Curated Characters ----------
ICONIC_CHARACTERS = [
    "Mario", "Luigi", "Peach", "Yoshi", "Bowser",
    "Link", "Zelda", "Ganondorf", "Samus Aran", "Kirby",
    "Pikachu", "Donkey Kong", "Sonic the Hedgehog", "Shadow the Hedgehog",
    "Master Chief", "Lara Croft", "Kratos", "Cloud Strife", "Sephiroth",
    "Solid Snake", "Mega Man", "Ryu", "Chun-Li", "Gordon Freeman",
    "Geralt of Rivia", "Nathan Drake", "Ellie", "Joel", "Arthur Morgan"
]

def get_character_label_list(client_id: str, access_token: str, limit: int = 0) -> list:
    return ICONIC_CHARACTERS

def identify_top_characters(image: Image.Image, labels: list, top_k=3) -> list:
    inputs = clip_processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    top_probs, top_idxs = torch.topk(probs, top_k)
    return [(labels[i], round(prob.item(), 3)) for i, prob in zip(top_idxs[0], top_probs[0])]

# ---------- Gradio Interface ----------
with gr.Blocks(title="IGDB MCP Tool") as app:
    gr.Markdown("# 🎮 IGDB MCP Tools")

    with gr.Tab("🔑 Get Access Token"):
        with gr.Row():
            cid = gr.Textbox(label="Twitch Client ID")
            csec = gr.Textbox(label="Twitch Client Secret", type="password")
        token_btn = gr.Button("Get Access Token")
        token_output = gr.Textbox(label="Access Token")
        token_btn.click(get_igdb_access_token, [cid, csec], token_output)

    with gr.Tab("👤 Get Basic Characters"):
        with gr.Row():
            char_cid = gr.Textbox(label="Client ID")
            char_token = gr.Textbox(label="Access Token", type="password")
        char_btn = gr.Button("Fetch Characters")
        char_output = gr.Textbox(label="Characters", lines=12)
        char_btn.click(get_igdb_characters, [char_cid, char_token], char_output)

    with gr.Tab("🎯 Search Game + Characters"):
        with gr.Row():
            game_cid = gr.Textbox(label="Client ID")
            game_token = gr.Textbox(label="Access Token", type="password")
        game_name = gr.Textbox(label="Game Name (e.g. Cyberpunk 2077)")
        game_btn = gr.Button("Search & Fetch Characters")
        game_output = gr.Textbox(label="Game Character Info", lines=16)
        game_btn.click(get_characters_for_game, [game_cid, game_token, game_name], game_output)

    with gr.Tab("🖼 Identify Character from Image"):
        with gr.Row():
            img_client_id = gr.Textbox(label="Client ID")
            img_token = gr.Textbox(label="Access Token", type="password")
        image_input = gr.Image(type="pil", label="Upload Character Image")
        result_output = gr.Textbox(label="Character Match", lines=6)
        image_button = gr.Button("Identify Character")

        def handle_image_upload(image, client_id, access_token):
            labels = get_character_label_list(client_id, access_token)
            top_matches = identify_top_characters(image, labels, top_k=3)
            return "\n".join([f"🎯 {name} ({prob * 100:.1f}%)" for name, prob in top_matches])

        image_button.click(fn=handle_image_upload, inputs=[image_input, img_client_id, img_token], outputs=result_output)

if __name__ == "__main__":
    app.launch(mcp_server=True)
