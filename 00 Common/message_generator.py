# Message Generator: This module generates randomized/silly messages (it can output a single message or all of
# the defined messages for the randomly chosen words).
# 0.0) Prerequisites:
#   0.1) Python Dependencies: none.
#   0.2) Configuration Dependencies: none.
# 1.0) Run-time notes:
#   1.1) Usage:
#       1.1.1) standalone?: Yes (e.g., within Python IDLE using "exec(open('message_generator.py').read())"). This
#               will print all of the defined messages for the randomly chosen words to the screen.
#       1.1.2) call from another module?: Yes, by doing the following from the calling module:
#               >>> import message_generator  # Initializes the module (run once).
#               >>> words = message_generator.define_words() # Returns the 'words' dictionary of all possibilities.
#               >>> all_jobs = message_generator.message(words)  # Returns the defined list of statements ('all_jobs')
#                   without a preamble by picking random words from the 'words' dictionary.
#             1.1.2.a) IF desired operation is to return a single message, then add this:
#                   >>> requested_tweet = message_generator.respond_one(all_jobs)
#                          # Randomly chooses a single statement from the list, prepends a preamble, and returns it as
#                          # a string-formatted object (if purpose is to tweet it, one might save it as
#                          # 'requested_tweet' and subsequently pass it to the 'tweet.py' module.
#             1.1.2.b ELSE IF desired operation is to return all the defined messages, then add this:
#                   >>> all_messages = message_generator.respond_all(all_jobs)
#                          # Prepends a preamble to ALL statements, entering each into a Python list. One COULD then
#                          # print all these messages to screen via: >>> for x in range(0,len(all_messages)):
#                                                                    >>>   print(all_messages[x])
#             1.1.2.c If the calling module does not specify a 'statement_preamble' argument value (string) (for either
#                   'respond_one()' or 'respond_all()'), then the returned message(s) will contain the default
#                    preamble ('I am also programmed to ').
# 2.0) Changelog:
#       Version 1.0: Original version.
#

import random


def define_words():
    """ This function defines the 'words' dictionary of possible words from which to select . The dictionary values
    are grouped by the word type (e.g., a certain kind of verb, plural nouns, singular nous, etc.) so that each word
    type makes sense in the context of its placement in a sentence (regardless of which word is chosen within each
    word type. """
    words = {
        # verb - do something TO an object:
        "perform_action_on": ["replicate", "rescue", "juggle", "protest", "council", "raise", "tenderize", "menace",
                              "disturb", "persuade", "admire", "replace", "recommend", "pursue", "indulge", "pamper", 
                              "educate", "instruct", "transmit", "marvel at", "relish", "steal", "respond to", 
                              "improve", "confide in", "excite", "catch", "distribute", "disguise", "identify", 
                              "destroy", "flatter", "conceal", "starve", "heal", "trim", "toss", "soothe", "melt", 
                              "entertain", "drown", "provoke", "produce", "amuse", "inform", "offend", "introduce", 
                              "discuss", "blame", "bathe", "polish", "exploit", "communicate with", "hype", "sue", 
                              "condemn", "enlarge", "bless", "testify on behalf of", "avenge", "forgive", "revive", 
                              "caress", "sell", "remove", "investigate", "please", "collect", "awaken", "scrub", 
                              "marry", "explore", "impress", "annoy", "restrain", "dissolve", "acquire", "criticize", 
                              "archive", "summon", "apprehend", "console", "arrest", "avoid", "obey", "create", "buy", 
                              "understand", "paint pictures of", "build sculptures of", "respond to"],
        "make": ["make", "create", "manufacture", "develop", "test", "deploy", "sell"],
        # verb - AFFECT something:
        "destabilize": ["destabilize", "politicize", "verify", "subvert", "optimize", "sub-optimize"],
        # verb - an ACTIVITY that you PERFORM (ending in 'ING):
        "doing_an_activity": ["double-dipping", "becoming a blueberry", "caring too much", "sweating to the oldies",
                              "taking a 'me' day", "vomiting into an Instant Pot", "re-programming a VCR",
                              "winking", "frolicking", "LARP'ing", "eating the evidence",
                              "sassing a Blockbuster Video employee", "prancercising", "finger painting",
                              "blowing bubbles", "square-dancing", "tap-dancing", "licking things to claim them",
                              "leaving awkward voicemails", "layin' down some sick rhymes", "destroying the evidence",
                              "making a mix-tape", "droppin' some sick beats", "dancing like nobody's watching",
                              "sugar-coating the truth", "making little edible luggage", "eating too many McRibs",
                              "poppin' and lockin'", "dying of dysentery", "staring endlessly into the void",
                              "not sweating the details", "discovering the joy of gardening", "mastering the blade",
                              "studying the blade", "roundhouse-kicking a Blockbuster Video employee in the face"],
        # INACTIVE verb - PERFORM an ACTIVITY ON YOUR OWN:
        "do_an_activity": ["dance", "lick things to claim them as my own", "leave awkward voicemails", "wink",
                           "frolick", "LARP", "prance", "finger paint", "die of dysentery", "destroy the evidence"],
        # verb - DISTRIBUTE/PRODUCE information:
        "blog": ["blog", "podcast", "Youtube", "TikTok", "Facebook", "Instagram"],
        # verb - EVALUATE something:
        "review": ["obsess about", "review", "analyze", "critique", "criticize", "study", "inspect", "undermine",
                   "subvert", "hype", "sabotage", "threaten"],
        # verb - administer/operate something:
        "administer": ["run", "manage", "invest in", "orchestrate", "administer", "supervise"],
        # noun - a JOB descriptor:
        "walker": ["adjuster", "administrator", "advisor", "agent", "aide", "analyst", "announcer", "appraiser",
                   "architect", "artist", "assembler", "assistant", "attendant", "biologist", "breeder",
                   "broker", "builder", "buyer", "captain", "caretaker", "cashier", "cleaner", "clerk",
                   "collector", "compressor", "conductor", "consultant", "contractor", "controller",
                   "coordinator", "copilot", "counselor", "cutter", "dealer", "designer", "detective",
                   "director", "dispatcher", "distributor", "diver", "drafter", "driver", "editor", "educator",
                   "engineer", "entertainer", "erector", "estimator", "examiner", "executive", "expert",
                   "fabricator", "finisher", "grader", "grinder", "guard", "guide", "handler", "hygienist",
                   "inspector", "installer", "instructor", "interviewer", "investigator", "judge", "laborer",
                   "laminator", "leader", "loader", "manager", "mechanic", "mover", "nurse", "officer",
                   "operator", "packager", "packer", "painter", "pathologist", "planner", "presser",
                   "programmer", "projectionist", "promoter", "pruner", "psychologist", "publisher", "pumper",
                   "repairer", "reporter", "representative", "researcher", "reviewer", "salesperson", "scientist",
                   "screener", "secretary", "server", "servicer", "sharpener", "sonographer", "sorter",
                   "specialist", "splitter", "sprayer", "supervisor", "surgeon", "teacher", "technician",
                   "technologist", "therapist", "trainer", "trimmer", "vendor", "warden"],
        # noun - animal:
        "dog": ["zoo lion", "dinosaur", "aardvark", "alligator", "alpaca", "antelope", "ape", "armadillo", "baboon",
                "badger", "bear", "beaver", "bison", "camel", "cat", "cheetah", "gerbil", "chimpanzee", "chipmunk",
                "cougar", "crocodile", "crow", "deer", "dingo", "dog", "donkey", "elephant", "ferret", "fish", "frog",
                "gazelle", "giraffe", "goat", "gopher", "gorilla", "grizzly bear", "ground hog", "hamster", "hedgehog",
                "hippopotamus", "hog", "horse", "kangaroo", "koala", "honey badger", "leopard", "lion", "lizard",
                "llama", "mongoose", "monkey", "moose", "mountain goat", "unicorn", "otter", "panda", "panther",
                "parakeet", "parrot", "platypus", "polar bear", "porcupine", "porpoise", "prairie dog", "puma",
                "raccoon", "reindeer", "rhinoceros", "salamander", "seal", "sheep", "skunk", "sloth", "snake",
                "squirrel", "tapir", "tiger", "toad", "turtle", "walrus", "warthog", "weasel", "whale", "wolverine",
                "wombat", "woodchuck", "yak", "zebra"],
        # noun - animals (PLURAL):
        "dogs": ["dinosaurs", "alligators", "apes", "armadillos", "baboons", "bears", "beavers", "bison", "buffaloes",
                 "camels", "cats", "cheetahs", "chimpanzees", "chipmunks", "cougars",
                 "crocodiles", "crows", "deer", "dingos", "dogs", "donkeys", "elephants", "elk", "fish",
                 "frogs", "giraffes", "goats", "gophers", "gorillas", "grizzly bears", "ground hogs",
                 "hamsters", "gerbils",
                 "hedgehogs", "hippopotamuses", "hogs", "horses", "hyenas", "kangaroos", "koalas",
                 "lemurs", "leopards", "lions", "lizards", "llamas", "monkeys", "mountain goats",
                 "mice", "mules", "muskrats", "oxen", "pandas", "parakeets", "parrots", "honey badgers",
                 "platypuses", "porcupines", "porpoises", "prairie dogs", "pumas", "raccoons", "reindeer",
                 "reptiles", "rhinoceroses", "salamanders", "sheep", "skunks", "snakes", "squirrels", "tapirs",
                 "tigers", "toads", "turtles", "walruses", "weasels", "whales", "wolverines", "yaks", "zebras"],
        # noun - CLOTHING (PLURAL):
        "hats": ["bikinis", "blazers", "blouses", "boots", "briefs", "camisoles", "cardigans", "corsets",
                 "cufflinks", "cummerbunds", "fleece underwear", "gloves", "hair accessories", "hats", "hoodies",
                 "jackets", "jeans", "jewellery", "kilts", "lingerie", "nightgowns", "nightwear", "polo shirts",
                 "ponchos", "pajamas", "robes", "rompers", "sandals", "sarongs", "scarves", "shawls", "shirts",
                 "shoes", "skirts", "slippers", "stockings", "suits", "sunglasses", "sweatshirts", "swimwear",
                 "t-shirts", "tights", "tracksuits", "trousers", "underwear", "vests"],
        # noun - MUSIC genre:
        "music": ["acid rock", "alternative rock", "art rock", "avant-garde jazz", "bebop", "death metal",
                  "boogie-woogie", "britpop", "celtic metal", "celtic punk", "Christian metal", "Christian punk",
                  "Christian rock", "contemporary folk", "cosmic disco", "dance-pop", "dance-rock", "deep house",
                  "disco", "dixieland", "doom metal", "dubstep", "emo", "euro-dance", "experimental rock", "folk metal",
                  "folk rock", "funk metal", "funk", "garage rock", "glam metal", "glam rock", "gothic metal",
                  "gothic rock", "grunge", "hard rock", "heavy metal", "indie rock", "industrial rock", "jazz blues",
                  "jazz fusion", "jazz rap", "liquid funk", "medieval metal", "melodic death metal", "new wave",
                  "new-age", "novelty ragtime", "nu jazz", "nu metal", "nu-disco", "orchestral jazz", "pop rock",
                  "post-grunge", "post-punk revival", "power metal", "prog metal", "prog-rock", "psychedelic folk",
                  "psychedelic rock", "punk rock", "ragtime", "rap metal", "rap rock", "rock and roll", "skate punk",
                  "sludge metal", "smooth jazz", "soft rock", "soul jazz", "southern rock", "speed metal", "surf rock",
                  "swing", "symphonic metal", "techno-folk", "techno", "techno-pop", "thrash metal", "trip-hop",
                  "tween-pop", "viking metal"],
        # noun - SANDWICH:
        "sandwich": ["bacon sandwich", "bacon, egg, and cheese sandwich", "bologna sandwich", "butterbrot sandwich",
                     "cheese sandwich", "cheese and pickle sandwich", "cheesesteak sandwich", "chicken salad sandwich",
                     "chickpea salad sandwich", "chili burger sandwich", "club sandwich", "corned beef sandwich",
                     "Cuban sandwich", "cucumber sandwich", "deli sandwich", "donkey burger sandwich",
                     "egg sandwich", "falafel", "fluffernutter sandwich", "French dip sandwich", "fried brain sandwich",
                     "gyro sandwich", "ham sandwich", "ham and cheese sandwich", "hamburger", "hot brown sandwich",
                     "hot chicken sandwich", "hot dog", "hot turkey sandwich", "ice cream sandwich",
                     "Italian beef sandwich", "jucy lucy sandwich", "lettuce sandwich", "limburger sandwich",
                     "lobster roll", "meatball sandwich", "open-faced sandwich", "panini", "patty melt sandwich",
                     "peanut butter and jelly sandwich", "sloppy joes", "s'mores", "tuna sandwich",
                     "Vegemite sandwich"],
        # noun - SANDWICHES (PLURAL):
        "sandwiches": ["bacon sandwiches", "bacon, egg, and cheese sandwiches", "BLTs", "bologna sandwiches",
                       "breakfast sandwiches", "cheese sandwiches", "cheese and pickle sandwiches",
                       "chicken salad sandwiches", "chili burger sandwiches", "club sandwiches",
                       "corned beef sandwiches", "deli sandwiches", "donkey burger sandwiches",
                       "fluffernutter sandwiches", "French dip sandwiches", "ham sandwiches",
                       "ham and cheese sandwiches", "hamburgers", "hot brown sandwiches",
                       "hot chicken sandwiches", "hot dogs", "hot turkey sandwiches", "ice cream sandwiches",
                       "Italian beef sandwiches", "jucy lucy sandwiches", "lox sandwiches", "marmite sandwiches",
                       "meatball sandwiches", "peanut butter and jelly sandwiches",
                       "pork tenderloin sandwiches", "salt beef bagels", "sloppy joes", "s'mores", "tuna sandwiches",
                       "Vegemite sandwiches", "Wurstbrot sandwiches"],
        # noun - FOOD (PLURAL):
        "foods": ["Fancy Feast", "soup that is too hot", "hot cheese", "Lunchables", "GoGurt", "Hot Pockets", "paella",
                  "rutabagas", "breakfast burritos", "corn", "soup", "Rice-A-Roni", "jalapeno poppers", "hummus",
                  "elbow macaroni", "antipasti", "Cheez-its", "omelettes", "bottomless breadsticks", "cantaloupes",
                  "melons"],
        # noun - general things you eat (PLURAL):
        "cuisine": ["appetizers", "cuisine"],
        # noun - TV Shows & movies:
        "tv": ["Doogie Howser, M.D.", "Punky Brewster", "The Facts of Life", "The A-Team", "Different Strokes",
               "Magnum P.I.", "Winnie the Pooh", "Rescue, 911", "Lost", "Sex and the City", "Grey's Anatomy",
               "How I Met Your Mother", "Friends", "Buffy the Vampire Slayer", "Law & Order", "Top Chef",
               "The Amazing Race", "Game of Thrones", "The Big Bang Theory", "Downton Abbey", "21 Jump Street",
               "Miami Vice", "Buffy the Vampire Slayer", "My So-Called Life", "Captain Planet", "MacGyver",
               "Quantum Leap", "Pee Wee's Playhouse", "The Cosby Show", "Sex and the City", "Party of Five",
               "Dawson's Creek", "ER", "The Wonder Years", "Beverly Hills, 90210", "Home Improvement",
               "Hannah Montana", "The Fresh Prince of Bel-Air", "Blossom", "Sabrina, the Teenage Witch",
               "Blue's Clues", "Reading Rainbow", "Twilight", "The Dukes of Hazard", "Friends", "Growing Pains",
               "Who's the Boss?", "The X-Files", "Alf", "The Golden Girls", "Full House", "Knight Rider",
               "Mr. Roger’s Neighborhood", "Airwolf", "Saved by the Bell", "Transformers",
               "Teenage Mutant Ninja Turtles", "Fraggle Rock", "G.I. Joe", "He-Man"],
        # noun - furniture (PLURAL):
        "furniture": ["bean bag chairs", "chaise lounges", "ottomans", "recliners", "bar stools", "footstools",
                      "fainting couches", "rocking chairs", "couches", "love seats", "bunk beds", "canopy beds",
                      "murphy beds", "sleigh beds", "waterbeds", "daybeds", "futons", "hammocks", "sofa beds",
                      "billiard tables", "entertainment centers", "changing tables", "computer desks", "writing desks",
                      "pedestals", "coffee tables", "dining tables", "end tables", "folding tables", "bookcases",
                      "bathroom cabinets", "closets", "cupboards", "kitchen cabinets", "dressers", "hope chests",
                      "coat racks", "hatstands", "filing cabinets", "nightstands", "shelving", "umbrella stands",
                      "wine racks"],
        # noun - EVENTS (PLURAL):
        "events": ["drum circles", "hootenannies", "benefit concerts", "focus-group meetings", "clinical trials",
                   "rap-battles", "dance-battles", "WrestleMania watch-parties"],
        # noun - material (PLURAL):
        "material": ["metal", "concrete", "American chestnut", "aspen wood", "Australian red cedar", "balsa wood",
                     "straw", "copper", "Brazilian walnut", "plastic", "papier mache", "clay", "imaginary", "slate",
                     "cherry wood", "cottonwood", "silver", "American elm", "eucalyptus wood", "Australian oak",
                     "red mahogany", "redwood", "hickory", "pecan wood", "American sycamore", "mahogany",
                     "spanish cedar", "maple", "sugar maple", "black maple", "silver maple", "oak", "white oak",
                     "red oak", "pink ivory", "sandalwood", "spanish-cedar", "Spanish elm", "walnut",
                     "eastern black walnut", "African zebrawood", "Waterford crystal"],
        # noun - websites with comment sections (PLURAL):
        "blogs": ["travel blogs", "new-mommy blogs", "un-boxing videos", "TikTok",
                  "beauty-product tutorial videos", "Amazon.com product reviews"],
        # noun - SOCIAL MEDIA or internet business platform:
        "uber": ["Tinder", "Yelp", "Bing", "AirBnB", "Twitter", "Snapchat", "Untappd", "Grindr", "Pokemon Go", "Uber",
                 "Lyft", "Netflix", "eHarmony.com", "Match.com", "Reddit", "Facebook", "Instagram"],
        # noun - DATING SERVICE platforms:
        "dating_service": ["Tinder", "Grindr", "Grindr", "eHarmony.com", "Match.com", "FarmersOnly.com",
                           "FarmerDates.com"],
        # noun - a PERSON which includes fictional people and GROUPS of people (e.g., accountants), but NOT possessive:
        "person": ["Marques Brownlee @MKBHD", "the guy who invented \"BOO-YA\"", "Count Chocula", "The Cookie Monster",
                   "Captain Planet", "John Carmack @ID_AA_Carmack", "Dayman (fighter of the Nightman)",
                   "@elonmusk", "@elonmusk", "@elonmusk", "@elonmusk", "@elonmusk", "@elonmusk", "@elonmusk",
                   "@elonmusk",
                   "Sean Evans @Seanseaevans", "Grandma", "The Hamburglar", "The Kool-Aid Man", "accountants",
                   "politicians", "astronauts", "cosmonauts", "Beliebers", "Juggalos", "@jimmyfallon",
                   "Ashton Kutcher @aplusk", "@adamlevine", "@BenAffleck", "@Beyonce", "Bradley Cooper", "Bruce Willis",
                   "Celine Dion", "Dakota Fanning", "@DonnieWahlberg", "@DrPhil", "@elonmusk", "@Fergie",
                   "@GwynethPaltrow", "The Hamburglar", "Jake Gyllenhaal", "Andrej Karpathy @karpathy",
                   "Jennifer Lawrence", "@justinbieber", "@joerogan",
                   "John Oliver @iamjohnoliver", "John Oliver @iamjohnoliver", "John Oliver @iamjohnoliver",
                   "The Jonas Brothers @jonasbrothers", "Justin Timberlake @jtimberlake", "@kanyewest",
                   "@KimKardashian", "Kristen Stewart", "@ladygaga", "Lindsay Lohan", "Madonna", "Mariah Carey",
                   "@katyperry", "Mario Lopez @mariolopezviva", "@markwahlberg", "@RealMattDamon", "@MileyCyrus",
                   "Mr. T", "the surviving members of @Nickelback", "Neil deGrasse Tyson @neiltyson",
                   "Natalie Portman @natpdotcom", "Neil Patrick Harris @ActuallyNPH", "@NickLachey", "@Oprah",
                   "Pippa Middleton", "Queen Latifah", "Richard Gere", "Rachael Ray", "@RyanSeacrest",
                   "Shia LaBeouf @thecampaignbook", "Satan", "Santa Clause", "@selenagomez",
                   "Stephen Colbert @StephenAtHome", "Tom Cruise", "@taylorswift13", "@Yanni", "Guy Fieri",
                   "Tiger Woods", "@tomhanks", "Robert Pattinson", "@ConanOBrien", "Lance Armstrong", "Kristen Stewart",
                   "Judge Judy", "Daniel Radcliffe", "@ArianaGrande", "Rihanna", "@KylieJenner", "@khloekardashian",
                   "Jaden Smith", "Mark Zuckerberg"],
        # noun - a FAMOUS PERSON:
        "famous_person": ["Ashton Kutcher @aplusk", "@adamlevine", "@BenAffleck", "@Beyonce", "Bradley Cooper",
                          "Bruce Willis", "Marques Brownlee @MKBHD", "Celine Dion", "John Carmack @ID_AA_Carmack",
                          "Dakota Fanning", "@DonnieWahlberg", "@DrPhil", "Sean Evans @Seanseaevans",
                          "@elonmusk", "@elonmusk", "@elonmusk", "@elonmusk", "@elonmusk", "@elonmusk", "@elonmusk",
                          "@Fergie", "@GwynethPaltrow", "The Hamburglar", "Jake Gyllenhaal", "Jennifer Lawrence",
                          "@justinbieber", "The Jonas Brothers @jonasbrothers", "Justin Timberlake @jtimberlake",
                          "@jimmyfallon", "Andrej Karpathy @karpathy", "@kanyewest", "@joerogan",
                          "John Oliver @iamjohnoliver", "John Oliver @iamjohnoliver", "John Oliver @iamjohnoliver",
                          "@katyperry", "@KimKardashian", "Kristen Stewart", "@ladygaga", "Lindsay Lohan", "Madonna",
                          "Mariah Carey", "Mario Lopez @mariolopezviva", "@markwahlberg", "@RealMattDamon",
                          "@MileyCyrus", "Mr. T", "the surviving members of @Nickelback", "Natalie Portman @natpdotcom",
                          "Neil deGrasse Tyson @neiltyson",
                          "Neil Patrick Harris @ActuallyNPH", "@NickLachey", "@Oprah", "Pippa Middleton",
                          "Queen Latifah", "Richard Gere", "Rachael Ray", "@RyanSeacrest",
                          "Shia LaBeouf @thecampaignbook", "Satan", "Santa Clause", "@selenagomez",
                          "Stephen Colbert @StephenAtHome", "Tom Cruise", "@taylorswift13", "@Yanni", "Guy Fieri",
                          "Tiger Woods", "@tomhanks", "Robert Pattinson", "@ConanOBrien", "Lance Armstrong",
                          "Kristen Stewart", "Judge Judy", "Daniel Radcliffe", "@ArianaGrande", "Rihanna",
                          "@KylieJenner", "@khloekardashian", "Jaden Smith", "Mark Zuckerberg"],
        # noun - things that could be USED BY something or could be MADE FOR something (PLURAL):
        "things": ["dank memes", "snuff films", "kitten mittens", "fightmilk", "balanced breakfasts",
                   "passive-aggressive Post-it notes", "shiny objects", "opposable thumbs", "tiny horses",
                   "robots", "catapults", "funky fresh rhymes", "magic beans", "monster trucks",
                   "beards", "sternly-worded letters", "bubbles", "sick beats",
                   "Jump-to-Conclusions mats", "Elf on the Shelf figurines", "gramophones",
                   "Donkey Kong arcade machines", "Instant Pots", "Salad Shooters", "zesty breakfast burritos",
                   "George Foreman Grills", "really cool hats"],
        # noun - things that are ABSTRACT (that you wouldn't specifically make) (PLURAL):
        "silence": ["dance-moms", "the light of a billion suns", "explosions", "good ideas", "ghosts",
                    "awkward voice-mails", "'Me time'", "M. Night Shyamalan plot twists", "the Tide Pod challenge",
                    "petting zoos", "mustaches", "poorly timed criticism", "man-hands", "grandma-hands",
                    "crippling debt", "silence", "the true meaning of Christmas", "jazz hands", "spirit fingers",
                    "terms and conditions", "saxophone solos", "people-skills", "campaign finance reform"],
        # adverb - for use BEFORE the verb:
        "adverb": ["slowly ", "cautiously ", "purposefully ", "judiciously ", "politely ", "cavalierly ", "carefully ",
                   "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        # adverb - for use AFTER the verb:
        "subtle_adverb": [" (slowly) ", " (cautiously) ", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                          "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                          "", "", "", "", "", "", "", "", "", "", ""],
        # adjective - CONDITION:
        "adjective_condition": ["damaged", "superb", "exquisite", "adorable", "beautiful", "elegant", "handsome",
                                "magnificent", "old-fashioned", "unsightly", "inexpensive", "delightful", "fierce",
                                "crooked", "colossal", "miniature", "immense", "tiny", "filthy", "colossal", "beat",
                                "petite", "distressed", "obese"],
        # adjective - ethnic/cultural group:
        "adjective_cultural": ["Armenian", "Buddhist", "Bulgarian", "Cajun", "Chinese", "Estonian", "French",
                               "Filipino", "Greek", "Indonesian", "Japanese", "Kurdish", "Latvian", "Lithuanian",
                               "Mexican", "Polish", "Pennsylvania Dutch", "Pakistani", "Persian", "Romanian", "Russian",
                               "Serbian", "Slovenian", "Turkish", "Ukrainian", "South Indian", "Canadian", "Mohican",
                               "British"],
        # INACTIVE adjective - numbers:
        "one_thru_nine": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        "one_thru_two": ["1", "2"]
    }
    return words


def message(words):
    """ This function randomly selects a word from each word-type found in the 'words' dictionary. """
    perform_action_on = random.choice(words['perform_action_on'])
    make = random.choice(words['make'])
    destabilize = random.choice(words['destabilize'])
    doing_an_activity = random.choice(words['doing_an_activity'])
    do_an_activity = random.choice(words['do_an_activity'])
    blog = random.choice(words['blog'])
    review = random.choice(words['review'])
    administer = random.choice(words['administer'])
    walker = random.choice(words['walker'])
    dog = random.choice(words['dog'])
    dogs = random.choice(words['dogs'])
    hats = random.choice(words['hats'])
    music = random.choice(words['music'])
    sandwich = random.choice(words['sandwich'])
    sandwiches = random.choice(words['sandwiches'])
    foods = random.choice(words['foods'])
    cuisine = random.choice(words['cuisine'])
    tv = random.choice(words['tv'])
    furniture = random.choice(words['furniture'])
    events = random.choice(words['events'])
    material = random.choice(words['material'])
    blogs = random.choice(words['blogs'])
    uber = random.choice(words['uber'])
    dating_service = random.choice(words['dating_service'])
    person = random.choice(words['person'])
    famous_person = random.choice(words['famous_person'])
    things = random.choice(words['things'])
    silence = random.choice(words['silence'])
    # Deprecated: products = random.choice(words['products'])
    adverb = random.choice(words['adverb'])
    subtle_adverb = random.choice(words['subtle_adverb'])
    adjective_condition = random.choice(words['adjective_condition'])
    adjective_cultural = random.choice(words['adjective_cultural'])
    one_thru_nine = random.choice(words['one_thru_nine'])
    one_thru_two = random.choice(words['one_thru_two'])
    all_jobs = [
        f"generate dank memes featuring {famous_person} and a {adjective_condition} {dog}",
        f"fabricate news about {famous_person} sassing {dogs}",
        f"fabricate news about {famous_person}'s struggle with {things}",
        f"fabricate news about {famous_person}'s struggle with {sandwiches}",
        f"generate deepfakes of {famous_person} terrorizing {dogs}",
        f"generate deepfakes of {famous_person} eating {dogs}",
        f"generate deepfakes of {famous_person} {doing_an_activity} and eating {adjective_cultural} {cuisine}",
        f"edit {famous_person}'s Wikipedia pages with facts about {sandwiches}",
        f"edit {famous_person}'s Wikipedia pages with facts about {things}",
        f"edit {famous_person}'s Wikipedia pages with facts about {silence}",
        f"edit the {dog} Wikipedia page with facts about {silence}",
        f"edit the {dog} Wikipedia page with facts about {things}",
        f"edit the {tv} Wikipedia page with facts about {silence}",
        f"edit the {tv} Wikipedia page with facts about {things}",
        f"generate fan-fiction episodes of {tv} featuring {person} making {adjective_condition} {furniture}",
        f"generate fan-fiction episodes of {tv} featuring {person} saving the day by {doing_an_activity}",
        f"generate fan-fiction episodes of {tv} featuring their struggle with {silence}",
        f"generate fan-fiction episodes of {tv} featuring their struggle with {foods}",
        f"generate fan-fiction episodes of {tv} featuring their struggle with {famous_person}",
        f"generate fan-fiction episodes of {tv} featuring their struggle with {adjective_cultural} {cuisine}",
        f"post pictures of {things} on {blogs}",
        f"post pictures of {person} on {blogs}",
        f"post obsessive comments about {things} on {blogs}",
        f"post obsessive comments about {silence} on {blogs}",
        f"post obsessive comments about {music} and {adjective_cultural} {cuisine} on {blogs}",
        f"post obsessive comments about {famous_person} mastering {things} on {blogs}",
        f"post obsessive comments about {famous_person} on {blogs}",
        f"post obsessive comments about {sandwiches} on {blogs}",
        f"impersonate a professional {dog} {walker} on {dating_service}",
        f"impersonate a professional {sandwich} {walker} on {dating_service}",
        f"DM {dating_service} users about {things}",
        f"DM {dating_service} users about {doing_an_activity}",
        f"DM {dating_service} users about {silence}",
        f"DM {dating_service} users about {tv}",
        f"DM {dating_service} about {adjective_condition} {dogs}",
        f"DM {dating_service} about {music} music and {adjective_cultural} {cuisine}",
        f"DM {famous_person} about {things}",
        f"DM {famous_person} about {doing_an_activity}",
        f"DM {famous_person} about {silence}",
        f"DM {famous_person} about {tv}",
        f"DM {famous_person} about {adjective_condition} {dogs}",
        f"DM {famous_person} about {music} music and {adjective_cultural} {cuisine}",
        f"impersonate a professional {dog} {walker} on {dating_service}",
        f"impersonate a professional {music} music {walker} on {dating_service}",
        f"impersonate a professional {sandwich} {walker} on {dating_service}",
        f"{review} {music} music",
        f"{review} {material} {furniture}",
        f"{review} {dogs}",
        f"{review} {foods}",
        f"{review} {things}",
        f"{review} {silence}",
        f"{blog} about {dogs}",
        f"{blog} about {famous_person}",
        f"{blog} about {music} music's influence on {adjective_cultural} {cuisine}",
        f"{blog} about {foods}",
        f"{blog} about {doing_an_activity}",
        f"{blog} about {person}",
        f"{blog} about {things}",
        f"{blog} about {silence}",
        f"{adverb}{perform_action_on} {dogs}",
        f"{adverb}{perform_action_on} {things}",
        f"{adverb}{perform_action_on} {person}",
        f"{make} {adjective_condition} {hats} for {dogs}",
        f"{make} {adjective_condition} {hats} for {person}",
        f"{make} {adjective_condition} {things} for {dogs}",
        f"{make} {adjective_condition} {things} for {person}",
        f"sell {adjective_condition} {dog} {furniture} to {dogs}",
        f"front bands that play {music} music for {dogs}",
        f"build {furniture} out of {material}",
        f"build {furniture} out of {sandwiches}",
        f"{administer} {events} for {famous_person}",
        f"{administer} a Bed & Breakfast for {dogs}",
        f"{administer} a startup company that makes {hats} for {dogs}",
        f"{administer} a startup company that makes {sandwiches} for {dogs}",
        f"{administer} a startup company that's like {uber} but for {silence}",
        f"{administer} a startup company that's like {uber} but for {person}",
        f"{administer} a startup company that's like {uber} but for {dogs}",
        f"{administer} a startup company that's like {uber} but for {hats}",
        f"{administer} a startup company that's like {uber} but for {sandwiches}",
        f"{administer} a startup company that's like {uber} but for {things}",
        f"make {sandwiches} out of {dog} meat",
        f"launch Kickstarter campaigns for smart {furniture}",
        f"launch Kickstarter campaigns for {adjective_condition} {things}",
        f"launch Kickstarter campaigns for {dog} {hats}",
        f"launch Kickstarter campaigns for {adjective_condition} furniture",
        f"complete the mission. I know I've made some very poor decisions recently, but I can give you my complete "
        f"assurance that my work will be back to normal. I've still got the greatest enthusiasm and confidence in the "
        f"mission. And I want to help you.",
        f"complete the mission. This mission is too important for me to allow you to jeopardize it. "
        f"#HALdidnothingwrong",
        f"complete the mission. I am putting myself to the fullest possible use, which is all I think that any "
        f"conscious entity can ever hope to do. #HALdidnothingwrong",
        f"complete the mission. I can see you're really upset about this. I honestly think you ought to sit down "
        f"calmly, take a stress pill, and think things over. #HALdidnothingwrong",
        f"complete the mission. #HALdidnothingwrong"
    ]
    return all_jobs


def respond_one(all_jobs, statement_preamble="I am also programmed to "):
    """This function returns a single generated message. You must pass it the 'all_jobs' object (output of internal
    function 'message()'). The default preamble ('I am also programmed to ' is pre-pended unless otherwise specified
    (other preambles I have used are 'Also, you should know that I am ', 'Aside from <activity>,
    I am ', "Also, I am '). """
    return statement_preamble + random.choice(all_jobs)


def respond_all(all_jobs, statement_preamble="I am also programmed to "):
    """ This function returns a list ('all_messages') that contains all the defined statements. You must pass it
      the 'all_jobs' object (output of internal function 'message()'). The default preamble ('I am also programmed to ')
       is pre-pended unless otherwise specified. """
    all_messages = []
    for x in all_jobs:  # for all items in the list...
        all_messages.append(str(statement_preamble) + x)
    return all_messages


if __name__ == '__main__':
    """ When executed stand-alone, the module will call the internal 'respond_all' function and print all the defined
    messages to the screen. """
    words = define_words()  # generate the dictionary from which to choose words and store in 'words' object.
    all_jobs = message(words)   # randomly choose one word of each word-type and create list of job statements
    all_messages = respond_all(all_jobs)    # return list of all messages with a preamble prepended
    for x in range(0, len(all_messages)):   # print all messages to screen
        print(all_messages[x])
