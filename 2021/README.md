# Hearthstone Grandmaster
https://playhearthstone.com/esports/programs/grandmasters

# Assumption
Suppose every match is 50/50

# Links
https://playhearthstone.com/en-us/esports/programs/rules-and-policies

# Improvements from last year
- Automatize
  - Every hour, check standings from https://playhearthstone.com/en-us/esports/standings/
  - ~~Write on https://gall.dcinside.com/mgallery/board/lists?id=pebble when something changed~~
  - Post on Twitter when something changed
- Prettier table

# Techs
- [x] AWS lambda + cron
- [x] HTML parsing
- [x] Simulation
- [x] Chart drawing
- [x] ~~DCInside~~ Twitter API

# TODO
- [ ] Install headless Chrome to AWS lambda instance
- [ ] Cache league result and query less
- [ ] Display rank 1-2, rank 3-6, rank 7-8 somehow (another chart?)
