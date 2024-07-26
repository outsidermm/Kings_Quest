# King's Quest Game

## Overview

King's Quest is a turn-based combat game featuring various player characters and enemies. Players can navigate through different game states including menus, character selection, level selection, and combat. The game is built using Pygame and Pygame GUI for handling the graphical user interface.

## Table of Contents

- [Usage](#usage)
- [Project Structure](#project-structure)

## Usage

1. Run the game:
    ```sh
    python main.py
    ```

2. Follow the in-game instructions to navigate through the menus, select your character, and engage in battles.

## Project Structure

```plaintext
kings_quest/
├── assets/
│   ├── abilities/
│   ├── abilities_downsize/
│   ├── characters/
│   ├── fight/
│   ├── fonts/
│   ├── icons_18/
│   ├── icons_48/
│   ├── background_images/
│   └── __init__.py
├── characters/
│   ├── enemies/
│   └── players/
│   └── base_character.py
├── gui/
│   ├── ability_hud.py
│   ├── enemy_combat_hud.py
│   ├── health_bar.py
│   ├── player_combat_hud.py
│   ├── statistic_bar.py
│   └── statistic_hud.py
├── settings/
│   ├── character_selection_theme.json
│   ├── combat_theme.json
│   ├── general.json
│   ├── health_bar.json
│   ├── level_selection_theme.json
│   └── user_settings.json
├── states/
│   ├── base_state.py
│   ├── character_selection_menu.py
│   ├── end_menu.py
│   ├── level_selection_menu.py
│   ├── quest_menu.py
│   ├── start_menu.py
│   └── turn_based_fight.py
├── utilities/
│   ├── __init__.py
│   ├── animation_utility.py
│   ├── general_utility.py
│   ├── img_utility.py
│   ├── json_utility.py
├── venv/
├── .gitattributes
├── .gitignore
├── ability.py
├── combat_controller.py
├── game.py
├── LICENSE
├── main.py
├── quest.py
├── README.md
├── state_manager.py
├── visual_dialogue.py
└── xp.py