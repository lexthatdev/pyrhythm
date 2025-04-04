# 🎵 pyrhythm

a rhythm game inspired by **friday night funkin'**, made entirely with python 🐍  
hit notes, vibe to music videos, and play with custom charts and songs 🎶

---

## 💻 requirements

before you jam out, make sure you have:

- python **3.13.2** 👉 (get it from the microsoft store or [official site](https://www.python.org))
- the following python modules:
  - `moviepy`
  - `configparser`

install them by running this in your terminal:

```bash
pip install moviepy configparser
```

---

## 🕹️ features

- 🎼 custom charts support (in the `charts/` folder)
- 📺 optional music videos (`musicvid.mp4`)
- 🎵 custom songs (`song.mp3`)
- 🎨 note skins + color customization
- ⚙️ fully tweakable settings in `options.txt`
- 🕹️ remappable controls
- 🎯 scoring with accuracy and combo tracking
- 🎉 terminal feedback with colored text output

---

## 🔧 options.txt breakdown

this file lets you control how your game works. here's an example:

```ini
[general]
sprite_notes = false          ; use image sprites instead of blocks
custom_colors = false         ; define your own note colors
show_musicvid = true          ; show the background video
quit_oncomplete = true        ; close the game when the song ends
autoplay = false              ; 👀 cheat mode??
username = you                ; for score display
version = pre-alpha 1.7.4     ; current version

[keybinds]
left = K_d
right = K_k
up = K_j
down = K_f
quit = K_DELETE

[colors]
left = (255,255,255)
right = (255,255,255)
up = (255,255,255)
down = (255,255,255)

[sprites]
is_one_sprite = true
one_sprite = "misc\\custom\\note.png"

left =
right =
up =
down =
```

---

## 🗂️ folder structure

your pyrhythm folder should look like this:

```
📁 pyrhythm/
├── charts/
│   └── my_song/
│       ├── song.mp3
│       ├── chart.json
│       └── musicvid.mp4 (optional)
├── misc/
│   ├── logo.png
│   ├── selectedsong.txt
├── options.txt
└── pyrhythm.py
```

- `selectedsong.txt` should contain the name of the song folder inside `charts/`  
  *(like `my_song`, no spaces)*

---

## 🎮 how to play

1. open a terminal in the project folder  
2. run the game with either a shortcut or the select_a_song.bat file!
3. here is an example of a shortcut command:

```bash
cmd.exe /k (path_to_your_batfile)
```

3. use your keybinds (default: `w`, `a`, `s`, `d`) to hit the notes  
4. try to full combo and flex your score 🤓

---

## 📦 add your own content

- 🎼 make a folder in `charts/` for your song  
- add:
  - `song.mp3` for audio  
  - `chart.json` for the note data  
  - optionally, `musicvid.mp4` for background visuals  
- update `misc/selectedsong.txt` with the folder name

---

## 🧠 tips

- enable `sprite_notes` and drop your custom sprites in the `misc/custom/` folder  
- tweak `colors`, `keybinds`, or set your name in `options.txt`  
- don’t delete `logo.png` or the game might cry 😢  
- autoplay exists... but don’t cheat unless you're testing 😉

---

## ❤️ license & credits

this project is open source and licensed under the **mit license**  
feel free to fork it, remix it, make your own mod or skin 🎨  
game coded with 💙 using `pygame`, `moviepy`, and `configparser`  
special thanks to everyone who vibes with rhythm games 🔊

---

*press start to vibe 🎮*
