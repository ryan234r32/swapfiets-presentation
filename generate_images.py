#!/usr/bin/env python3
"""Generate background images for Swapfiets presentation using Gemini API."""
import json, base64, urllib.request, time, os, sys

API_KEY = "AIzaSyAL-HdeDZfjvzYklQU3_zJ7Wr9d3cZldj8"
MODEL = "gemini-2.5-flash-image"
OUTPUT_DIR = "/Users/ryan/swapfiets-presentation/images"

prompts = {
    "amsterdam_bikes": "Aerial view of thousands of bicycles parked densely along an Amsterdam canal, Dutch canal houses in background, golden hour warm light, editorial photography style, wide cinematic 16:9 format, high quality",
    "bike_graveyard": "Aerial drone photograph of a massive pile of thousands of colorful shared bicycles abandoned in a Chinese city bike graveyard, yellow orange blue bikes piled into mountains, documentary photography, wide 16:9 format",
    "student_delft": "A young university student standing with a bicycle on a charming Dutch cobblestone street in Delft, traditional Dutch row houses with red brick, overcast natural light, lifestyle editorial photography, wide 16:9",
    "swapfiets_store": "Interior of a modern bright minimalist bicycle shop with several clean bikes on display, blue accent wall, industrial-chic design with exposed ceiling, commercial photography, wide 16:9",
    "blue_wheel": "Extreme close-up of a bright vivid blue bicycle front wheel and tire on wet cobblestone, shallow depth of field, blurred Dutch street in background, moody golden hour light, editorial macro photography, wide 16:9",
    "dutch_cycling": "Person riding a classic Dutch upright bicycle through an Amsterdam street alongside a canal, autumn golden hour sunlight, daily commute atmosphere, bicycles parked along bridge railing, editorial lifestyle photography, wide 16:9",
    "bike_workshop": "Well-organized bicycle repair workshop interior, multiple bikes being serviced on stands, tools neatly arranged on pegboard wall, warm industrial lighting, clean professional space, editorial photography, wide 16:9",
    "bike_landfill": "Pile of discarded broken bicycles in a waste landfill, rusted frames twisted metal, overcast gloomy sky, environmental documentary photography, wide 16:9 format",
    "factory": "Inside an aluminum smelting factory, molten metal glowing orange in large crucible, industrial workers in protective gear, dramatic contrast of orange glow and dark factory interior, documentary photography, wide 16:9",
    "sunset": "Amsterdam canal at sunset, iconic view with bicycles parked along iron bridge railing, warm golden orange sky reflected in still canal water, historic buildings silhouetted, travel editorial photography, wide 16:9",
    "crossroads": "Dramatic fork in a misty road at dawn, one path bright and hopeful leading to sunlight, other path dark and foggy, atmospheric cinematic photography, symbolic crossroads choice, wide 16:9",
    "broken_bike": "Abandoned broken rusty bicycle chained to a pole on a rainy Dutch street, flat tire, bent wheel, peeling paint, dark moody atmosphere with rain puddles reflecting streetlights, documentary photography, wide 16:9",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

for name, prompt in prompts.items():
    output_path = f"{OUTPUT_DIR}/{name}.png"
    if os.path.exists(output_path):
        print(f"SKIP {name} (already exists)", flush=True)
        continue

    print(f"Generating {name}...", flush=True)

    data = json.dumps({
        "contents": [{"parts": [{"text": f"Generate an image: {prompt}"}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }).encode()

    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())

        if "candidates" in result:
            for part in result["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    img_bytes = base64.b64decode(part["inlineData"]["data"])
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    print(f"  SAVED {output_path} ({len(img_bytes)} bytes)", flush=True)
                    break
            else:
                print(f"  WARNING: No image in response for {name}", flush=True)
        else:
            err = result.get("error", {})
            print(f"  ERROR: {err.get('message', str(err)[:200])}", flush=True)
    except Exception as e:
        print(f"  EXCEPTION: {e}", flush=True)

    time.sleep(3)

print("\nAll done!", flush=True)
