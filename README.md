# MTGA (Magic: the Gathering Arena) Bot

__Goal:__ Create a bot that can AFK MTGA, play many games of ranked

## Implementation

__Deck:__ Mono R Cavalcade, [Decklist](https://www.mtggoldfish.com/deck/7984890#paper)

__Gameplay:__ Play cards in hand from left to right. Pass through phases. All attack in combat.

__"Seeing" the game:__ Parse MTGA logs to get game info. Use Scryfall API for card lookup.

__Interacting with the game:__ Use KBM controller Python library.

## Notes for use

- Must start parser after MTGA
- Mouse is mapped to specific pixels, only works on 1920x1080 screens
