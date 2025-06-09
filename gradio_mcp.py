import requests
import json
import gradio as gr

# ---------- Shared Helpers ----------
def igdb_post(endpoint: str, client_id: str, access_token: str, query: str):
    """
    Helper function to make a POST request to the IGDB API.

    Args:
        endpoint (str): The IGDB API endpoint (e.g., "games", "characters").
        client_id (str): Twitch Client ID.
        access_token (str): IGDB access token.
        query (str): IGDB query string.

    Returns:
        dict | list: The response from the IGDB API, or an error dict.
    """
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
    """
    Retrieves an access token from Twitch to authenticate with IGDB.

    Args:
        client_id (str): Twitch Client ID.
        client_secret (str): Twitch Client Secret.

    Returns:
        str: IGDB access token or an error message.
    """

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

# ---------- Lookup Resolvers ----------
def resolve_lookup(client_id: str, access_token: str, category: str, lookup_id: int) -> str:
    """
    Resolves an ID into a human-readable name from a specific IGDB category.

    Args:
        client_id (str): Twitch Client ID.
        access_token (str): IGDB access token.
        category (str): The IGDB category (e.g., "character_genders").
        lookup_id (int): The ID to resolve.

    Returns:
        str: Resolved name or original ID as string.
    """
    query = f"fields name; where id = {lookup_id}; limit 1;"
    result = igdb_post(category, client_id, access_token, query)
    return result[0]["name"] if result and isinstance(result, list) else str(lookup_id)

def get_gender_name(client_id: str, access_token: str, gender_id: int) -> str:
    """
    Fetches the name of a character's gender.

    Args:
        client_id (str): Twitch Client ID.
        access_token (str): IGDB access token.
        gender_id (int): Gender ID.

    Returns:
        str: Gender name.
    """
    return resolve_lookup(client_id, access_token, "character_genders", gender_id)

def get_species_name(client_id: str, access_token: str, species_id: int) -> str:
    """
    Fetches the name of a character's species.

    Args:
        client_id (str): Twitch Client ID.
        access_token (str): IGDB access token.
        species_id (int): Species ID.

    Returns:
        str: Species name.
    """
    return resolve_lookup(client_id, access_token, "character_species", species_id)

# ---------- Character Fetching ----------
def get_igdb_characters(client_id: str, access_token: str) -> str:
    """
    Retrieves a basic list of IGDB characters.

    Args:
        client_id (str): Twitch Client ID.
        access_token (str): IGDB access token.

    Returns:
        str: Formatted string of characters or error message.
    """
    query = "fields id, name, gender, species, description; limit 10;"
    result = igdb_post("characters", client_id, access_token, query)
    if isinstance(result, dict) and "error" in result:
        return f"❌ {result['error']}"
    return "\n\n".join([
        f"{c['id']}: {c['name']}\n{c.get('description', '')}" for c in result
    ]) or "No characters found."

# ---------- Game Search ----------
def search_game_by_name(client_id: str, access_token: str, name: str):
    """
    Searches for a game by name using the IGDB API.

    Args:
        client_id (str): Twitch Client ID.
        access_token (str): IGDB access token.
        name (str): Name of the game to search.

    Returns:
        dict | None: Game info dictionary or None if not found.
    """
    query = f'search "{name}"; fields id, name, summary, url; limit 1;'
    result = igdb_post("games", client_id, access_token, query)
    if isinstance(result, list) and result:
        return result[0]
    return None

# ---------- Characters for Game ----------
def get_characters_for_game(client_id: str, access_token: str, game_name: str) -> str:
    """
    Retrieves characters for a specific game by name.

    Args:
        client_id (str): Twitch Client ID.
        access_token (str): IGDB access token.
        game_name (str): Name of the game.

    Returns:
        str: Formatted character details or error message.
    """
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

if __name__ == "__main__":
    app.launch(mcp_server=True)
