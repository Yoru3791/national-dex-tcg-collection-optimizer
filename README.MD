# 🃏 National Dex TCG Challenge & Optimizer

Welcome to the **National Dex TCG Challenge**! The goal of this project is to collect all 1,025+ Pokémon in their physical Trading Card Game (TCG) form, using a mix of pack-opening fun and mathematical efficiency. 

This repository contains the ultimate (not really, there are probably some upgrades to be made) strategy guide to complete the binder without going bankrupt, as well as a **Python Optimizer Script** that calculates which expansion you should buy next based on your currently missing Pokémon.

## 📖 The Master Plan

Collecting every single Pokémon in TCG format requires strategy. Modern sets mix Pokémon from all generations, so buying blindly leads to massive duplicate piles. We divide the plan in 4 large steps:

### Phase 1: Preparation
* **The Binder:** Invest in a 16-Pocket (1,000+ cards) or multiple 9-Pocket Zip Binder (e.g., VaultX, Gamegenic). *Never use O-ring binders; they will damage your cards over time.*
* **Protection:** Get standard Penny Sleeves. Every card goes into a sleeve before entering the binder.
* **The Tracker:** Set up a Google Sheets document to track your collection (You could use any app that you like, but since we will using a .csv for optimizing the searchm we might aswell use Google Sheets).

### Phase 2: Early Expansion
*The goal here is sheer quantity. We avoid duplicate fatigue by prioritizing set variety.*
* **Kanto Focus:** Start with products from *Scarlet & Violet: 151* to clear out Generation 1 quickly.
* **Modern Variety:** Buy packs from sets like *Crown Zenith* (massive generation variety) or *Paldea Evolved* (heavy on Gen 9).
* **The Golden Rule:** Never buy more than 15-20 booster packs of the exact same expansion. Switch sets!
* **Use the Optimizer:** This is when you start running `optimizer.py` (more on this below) to figure out which set gives you the best odds of pulling new Pokémon.

### Phase 3: Trading and Bulk (Around 40% Completion)
*Once you have about 400-500 Pokémon, opening packs becomes mathematically inefficient.*
* **Hunt for "Bulk":** Look in local Facebook groups or TCG communities for players selling "Bulk" (boxes of thousands of common/uncommon cards for very cheap). 
* **Trade your Hits:** Use any duplicate rare cards (ex, V, Full Arts) as trade currency at your local card shop or online to acquire missing Pokémon.
* **Stop Pack-Opening:** Only use the optimizer for very specific sets or just stop buying sealed products altogether.

### Phase 4: Precision Hunting (Last 15%)
*Do not buy sealed packs in this phase. The math is entirely against you.*
* **Singles Market:** Buy individual missing cards on platforms like TCGPlayer, Cardmarket, or local stores to fill the exact gaps in your binder.

---

## 💻 The Algorithm: `optimizer.py`

When you are in Phase 2 or early Phase 3, you'll want to buy packs occasionally. But which pack gives you the highest chance of getting a Pokémon you don't have? 

This Python script reads your collection tracker, queries the official [Pokémon TCG API](https://pokemontcg.io/), and calculates the probability of pulling a new Pokémon for every set on the market.

### How to Use It with Google Sheets

**1. Set up your Google Sheet Tracker:**
You can create your own or use my ready-to-go template! 
👉 **[Click here to get a copy of the National Dex Tracker Template](https://docs.google.com/spreadsheets/d/16LEe5n-7ahg8bXKGTxlK5Em03giADBo90cdpZCu2Psc/edit?usp=sharing)**

*Just click the link, hit "Make a copy", and it will be saved to your own Google Drive. It already includes all 1,025 Pokémon and the color-coding rules!*

**2. Export to CSV:**
In Google Sheets, go to **File > Download > Comma Separated Values (.csv)**. Rename the downloaded file to `collection.csv` and place it in the same folder as the script.

**3. Run the Script:**
Open your terminal or command prompt in that folder and run:
```bash
python optimizer.py

```

**4. Check the Output:**
The script handles server timeouts automatically and will output a ranked list. Buy packs from the highest-ranked set!

```text
--- TOP EXPANSIONS TO BUY ---
1. Crown Zenith
   Probability of pulling a new Pokemon: 72.50%
   (145 missing Pokemon out of 200 unique in set)

```

### (Optional) API Key

The script works without an API key, but to avoid rate limits, it is highly recommended to get a free key at [dev.pokemontcg.io](https://dev.pokemontcg.io/) and paste it into the `API_KEY` variable inside `optimizer.py`.

---
## 💡 Pro Tips & Resources

**1. Use Visual Placeholders**
Having physical placeholders in your empty binder pockets makes the visual tracking much easier and the whole process much more satisfying. I found [Myllection](https://www.myllection.com/en) on Reddit (shoutout to the unknown creator!). If you don't want to print them yourself, I've uploaded two PDFs to this repository (`pokedex.pdf` and `pokedex-with-images.pdf`). They go from #1 to #1025, plus alternative forms (numbered 10001+). If you are collecting something else, feel free to use different placeholders; these are just a recommendation!

**2. Custom Text Lists**
If you want to generate your own CSV list from scratch instead of using my template, the [Pokémon Database Text List Generator](https://pokemondb.net/tools/text-list) is a fantastic tool (also found on Reddit).

**3. Protect Your Cards**
I cannot stress this enough: **DO NOT use O-ring or D-ring binders**. As you turn the pages, the rings will eventually dent and ruin your cards. Always use ringless, side-loading Zip Folios. Additionally, always use penny sleeves. Put every single card in a sleeve before it goes into the binder. Your collection will thank you in the long run.

**4. Your Collection, Your Rules**
Do you want all Commons or Holos? Your call. Do you want all EX or V cards? Go for it. Do you want to suffer and collect only Illustration Rares (IR/SIR)? That's your choice! Huge shoutout to [@bamfies](https://www.youtube.com/@bamfies/shorts) on YouTube, who is doing this exact challenge with SIRs and inspired me to start my own collection.

**5. Stick to a Budget**
Whether it's a weekly or monthly budget, stick to it. This is a secondary hobby; it's a marathon, not a sprint. There's no need to rush. You *could* just buy every single missing card online at once, but that takes away the thrill of the hunt and the joy of pack-opening!

**6. Plan for Regional Forms**
Decide early on if you want to include Alolan, Galarian, Hisuian, or Paldean forms in your main binder. Some collectors put them right next to their original counterpart (e.g., Alolan Vulpix right next to Kanto Vulpix), while others dedicate a separate section at the end of the binder. Plan your pocket spaces before you start putting cards in!

---

## ❓ Frequently Asked Questions (FAQ)

**1. The Python script closes immediately when I double-click it. What do I do?**
If you are on Windows, double-clicking a `.py` file might run it and close the window instantly before you can read the results. To fix this, open your Command Prompt (CMD) or Terminal, navigate to the folder where the script is located, and run it by typing: `python optimizer.py`.

**2. The script shows "Server timeout (Error 504)". Is it broken?**
Not at all! The Pokémon TCG API is fantastic but occasionally experiences micro-timeouts. The script is designed to automatically wait 5 seconds and retry. Just let it run! If it fails completely, the API might be under maintenance; try again in a few minutes.

**3. Do I *really* need an API Key?**
You can run the script completely anonymously without a key. However, the API enforces rate limits for anonymous users. If you see an `Error 429 (Too Many Requests)`, the script will pause for 10 seconds. Getting a free API key at [dev.pokemontcg.io](https://dev.pokemontcg.io/) makes the data fetching significantly faster and removes these interruptions.

**4. Does the algorithm account for card rarity (Holo, EX, Illustration Rare)?**
No. This optimizer is strictly designed for a "National Dex" challenge, meaning the goal is simply to get *at least one* of every Pokémon. It treats a Common Bulbasaur and a Secret Rare Bulbasaur as the exact same "hit" to fill your binder slot. 

**5. Why shouldn't I buy whole booster boxes of the same set?**
Math! Modern sets have around 150-250 unique cards. The first 10 packs you open will give you almost entirely new Pokémon. By pack 20, you will be pulling 90% duplicates. Rotating your purchases across different expansions is the cheapest way to build a National Dex.

## ⚠️ Disclaimer & Community

This project was originally created for my own personal use, but I thought it would be a fun idea to share it! Keep in mind that the algorithm might not be flawless and the math might not be 100% perfect.

Please feel free to help out by submitting improvements, leaving comments, opening pull requests, or even just sharing your own collection progress and binder photos. We are all in this challenge together!
