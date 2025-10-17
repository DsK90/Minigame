# 🎮 Anime Monster Fighter

A dungeon-crawling action game built with Python and Pygame featuring an anime character fighting monsters through multiple dungeon maps.

## ✨ Features

- **Anime-style characters**: Pink anime character with expressive face animations
- **Monster variety**: Three different monster types with unique stats and appearances
- **Dungeon progression**: Escape through multiple maps, each with unique layouts
- **Road-based movement**: Both player and monsters can only move on the dungeon roads
- **Strategic combat**: Attack monsters before they reach you to avoid taking damage
- **Map completion bonus**: Earn 100 points for reaching each map exit
- **Multiple map types**: Cross patterns, mazes, spirals, and random layouts
- **Progressive difficulty**: Monsters get stronger with each level
- **Contact damage system**: Monsters deal damage on contact and die after 1 second
- **Lightning attack effects**: Blue lightning spark when attacking
- **Clay pot power-ups**: Destroy pots for temporary lightning upgrades

## 🎮 Controls

- **Movement**: Arrow keys or WASD
- **Attack**: Spacebar (has cooldown)
- **Restart**: Press R when game over

## 🚀 Quick Start

**Double-click this file to start the game:**

```
start_game.bat
```

## 📦 Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 How to Run

**Option 1: Double-click the batch file**

```
start_game.bat
```

**Option 2: Command line**

```bash
python game.py
```

## 🎯 Gameplay

- **Start**: You begin in the center of each dungeon map
- **Monsters**: White ghost monsters spawn randomly and chase you
- **Combat**: Use spacebar to attack monsters before they reach you
- **Movement**: You can only move on the gray road tiles (shown with center dots)
- **Progression**: Reach the yellow exit tiles to advance to the next map (+100 points)
- **Random Maps**: Each level has a randomly selected layout (grid, spiral, corridor, or random)
- **Progressive Difficulty**: Monsters get stronger, faster, and more numerous with each level
- **Contact Damage**: Monsters deal damage when touching you and die after 1 second of contact
  - **Fast ghosts**: Deal 10 damage on contact
  - **Tank ghosts**: Deal 20 damage on contact
  - **Balanced ghosts**: Deal 15 damage on contact
- **Power-ups**: Destroy clay pots for temporary lightning attack upgrades (stackable up to 3)
- **Audio system**: Melodic background music, attack sound effects, and contact damage sounds
- **Strategy**: Balance attacking monsters vs reaching exits for maximum score

## 👻 Monster Types

- **Fast ghosts**: Quick but low health (require 1 hit at level 1, 2+ hits at higher levels)
- **Tank ghosts**: Slow but high health (require 2-3+ hits depending on level)
- **Balanced ghosts**: Medium speed and health

## ⚡ Power-ups

- **Clay Pots**: Brown squares found on roads
- **Lightning Upgrades**: Destroy pots to increase attack range (4 seconds, stackable up to 3 times)
- **Strategy**: Use upgrades during heavy monster waves or to clear paths to exits

## 🛠️ Technical Details

- **Engine**: Python 3.7+ with Pygame 2.5.2
- **Performance**: 60 FPS smooth gameplay
- **Graphics**: Custom anime-style sprite rendering
- **Collision**: Precise tile-based movement system
- **AI**: Pathfinding monsters with contact damage mechanics
- **Audio**: Background music and sound effects ready for implementation
- **Resolution**: 1200x900 window with scalable UI

## 📈 What's Included

✅ **Complete Game** - Fully playable desktop version
✅ **All Features** - Random maps, progressive difficulty, power-ups
✅ **Easy Start** - Double-click `start_game.bat` to play
✅ **Source Code** - All Python files for customization
✅ **Documentation** - Comprehensive README with gameplay guide

## 🎯 Perfect For

- **Casual Gaming** - Easy to learn, hard to master
- **Game Development Learning** - Well-structured Python code
- **Quick Gaming Sessions** - Short but challenging levels
- **Strategy Enthusiasts** - Balance combat vs progression
