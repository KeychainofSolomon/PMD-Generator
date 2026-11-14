# Deliverance Character Generator

A character and NPC generator for **Pokémon Mystery Dungeon: Deliverance**, a tabletop RPG set in New Palafitte on the Great Bayou.

Open `index.html` in a browser. It needs no install and no internet connection. All the Pokémon data lives in `data.js`, next to it.

## What it does

- **Player characters** follow the creation rules:
  - Start at level 1, at the first stage of an evolution line. A Pokémon that evolves from a baby (Pikachu from Pichu) also counts as first stage.
  - Legendary and Mythical Pokémon are story-only.
  - Regional variants need the Exotic trait. Dual types need Dual, and the rarer types need Rare. A house-rule tick box turns the type limits off.
  - Type-locked backgrounds (The Thief for Dark types, and so on) only fit Pokémon of that type.
  - Starting moves are the species' default level-1 moves. The full move pool it can learn later is listed underneath.
- **NPCs** can be any species at any level from 1 to 50. Stats, points, evolution bonuses and level-up moves follow the level. A warning shows when an evolved form is below the Rank it needs.
- **Randomize** builds a complete legal character or NPC.
- **Sheet** gives a ready-to-paste character sheet. Copy it, download it as .txt, or save it to a roster kept in your browser.

Moves show their Deliverance Tier, their to-hit penalty and a damage preview at the character's Rank.

## Updating the data

`data.js` is built from [PokeAPI's data tables](https://github.com/PokeAPI/pokeapi/tree/master/data/v2/csv). To rebuild it, download those CSV files into one folder and run `python tools/build_data.py` from inside that folder. Then copy the new `data.js` here.

Pokémon and all related names are trademarks of Nintendo, Game Freak and The Pokémon Company. This is an unofficial fan project.
