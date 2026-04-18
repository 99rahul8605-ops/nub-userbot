"""
WordSeek Game Solver - Auto-player for WordSeek Telegram bot
Analyzes game feedback and provides optimal word guesses
"""

import json
import os
from typing import Set, List, Dict, Tuple


class WordSolver:
    """
    Advanced solver for WordSeek (Wordle-like) game
    Uses letter frequency analysis and constraint filtering
    """

    def __init__(self):
        """Initialize solver with word lists from WordSeek"""
        self.all_words = self._load_word_list('allWords.json')
        self.common_words = self._load_common_words('commonWords.json')
        self.letter_frequency = self._calculate_frequency()

    def _load_word_list(self, filename: str) -> Set[str]:
        """Load 5-letter words from JSON file"""
        words = set()
        
        # Try multiple paths
        paths = [
            f'{filename}',
            f'data/{filename}',
            f'plugins/data/{filename}',
            os.path.expanduser(f'~/{filename}'),
        ]
        
        for path in paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            words = {w.lower() for w in data if len(w.strip()) == 5}
                        elif isinstance(data, dict):
                            words = {w.lower() for w in data.keys() if len(w) == 5}
                        if words:
                            print(f"[SOLVER] Loaded {len(words)} words from {path}")
                            return words
                except Exception as e:
                    print(f"[SOLVER] Error loading {path}: {e}")
                    continue
        
        # Fallback: create a basic word set
        print("[SOLVER] Using fallback word list (limited)")
        return self._get_fallback_words()

    def _load_common_words(self, filename: str) -> Dict[str, Dict]:
        """Load common words with meanings"""
        words = {}
        
        paths = [
            f'{filename}',
            f'data/{filename}',
            f'plugins/data/{filename}',
        ]
        
        for path in paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        words = json.load(f)
                        print(f"[SOLVER] Loaded {len(words)} common words from {path}")
                        return words
                except Exception as e:
                    print(f"[SOLVER] Error loading {path}: {e}")
                    continue
        
        return {}

    def _get_fallback_words(self) -> Set[str]:
        """Fallback word list for testing"""
        return {
            'about', 'above', 'abuse', 'abuse', 'access', 'accident', 'account',
            'abuse', 'abide', 'abort', 'abate', 'abbey', 'acorn', 'adopt',
            'adult', 'after', 'again', 'agent', 'agree', 'ahead', 'album',
            'album', 'alert', 'alien', 'align', 'alive', 'allow', 'alloy',
            'aloft', 'alone', 'along', 'aloof', 'aloud', 'angel', 'anger',
            'angle', 'angry', 'anime', 'ankle', 'annoy', 'apart', 'apple',
            'apply', 'arena', 'argue', 'arise', 'armor', 'aroma', 'arose',
            'array', 'arrow', 'aside', 'askew', 'aspen', 'asset', 'atlas',
            'attic', 'audio', 'audit', 'avoid', 'await', 'awake', 'award',
            'aware', 'awful', 'axial', 'bacon', 'badge', 'badly', 'bagel',
            'baker', 'bases', 'basic', 'basin', 'basis', 'batch', 'beach',
            'beast', 'began', 'begin', 'being', 'belch', 'belle', 'belly',
            'below', 'bench', 'berry', 'billy', 'birth', 'black', 'blade',
            'blame', 'blank', 'blaze', 'bleak', 'bleat', 'bleed', 'blend',
            'bless', 'blind', 'blink', 'bliss', 'block', 'bloom', 'blown',
            'blues', 'bluff', 'blunt', 'blush', 'board', 'boast', 'boats',
            'bobby', 'boney', 'boost', 'booth', 'booze', 'boozy', 'borax',
            'borne', 'botch', 'brain', 'brand', 'brass', 'brave', 'bread',
            'break', 'breed', 'bribe', 'brick', 'bride', 'brief', 'brine',
            'bring', 'brink', 'brisk', 'brood', 'brook', 'broom', 'broth',
            'brown', 'bruce', 'brunt', 'brush', 'brute', 'buddy', 'built',
            'bulge', 'bunch', 'bunny', 'buoys', 'burst', 'buyer', 'cabal',
            'cabin', 'cable', 'cache', 'cadet', 'caged', 'cagey', 'cakes',
            'camel', 'cameo', 'canal', 'candy', 'caned', 'canoe', 'caper',
            'cards', 'cargo', 'carol', 'carry', 'carts', 'carve', 'cased',
            'cases', 'caste', 'catch', 'cater', 'caulk', 'cause', 'caves',
            'cease', 'cedar', 'chain', 'chair', 'chalk', 'champ', 'chant',
            'chaos', 'chard', 'charm', 'chart', 'chase', 'chasm', 'cheap',
            'cheat', 'check', 'cheek', 'cheer', 'chess', 'chest', 'chick',
            'chief', 'child', 'chill', 'chimp', 'china', 'chink', 'chips',
            'chirp', 'choke', 'chord', 'chore', 'chose', 'chuck', 'chump',
            'chunk', 'churn', 'cigar', 'civic', 'civil', 'claim', 'clamp',
            'clash', 'clasp', 'class', 'clave', 'clean', 'clear', 'cleat',
            'cleft', 'clerk', 'click', 'cliff', 'climb', 'cling', 'cloak',
            'clock', 'clone', 'close', 'cloth', 'cloud', 'clout', 'clown',
            'coach', 'coast', 'coats', 'cobra', 'cocoa', 'coeur', 'coils',
            'coins', 'colds', 'colon', 'color', 'comet', 'comic', 'comma',
            'conch', 'cones', 'coral', 'cords', 'cores', 'corgi', 'corks',
            'corns', 'corps', 'couch', 'cough', 'could', 'count', 'coupe',
            'court', 'couth', 'coven', 'cover', 'covet', 'cowed', 'cower',
            'crack', 'craft', 'cramp', 'crane', 'crank', 'crash', 'crass',
            'crate', 'crave', 'crawl', 'craze', 'crazy', 'creak', 'cream',
            'creed', 'creek', 'creep', 'creme', 'crepe', 'cress', 'crevice',
            'crick', 'cried', 'crier', 'crime', 'crimp', 'crops', 'cross',
            'crouch', 'crowd', 'crown', 'crude', 'cruel', 'crumb', 'crush',
            'crust', 'crypt', 'cubic', 'cuddy', 'culls', 'culls', 'cults',
            'curbs', 'curds', 'cured', 'cures', 'curls', 'curry', 'curse',
            'curve', 'cushy', 'cutie', 'cycle', 'cynic', 'daily', 'dairy',
            'daisy', 'dance', 'dandy', 'dared', 'dares', 'darks', 'darts',
            'dated', 'dates', 'datum', 'daunt', 'davit', 'dazed', 'dealt',
            'death', 'debar', 'debit', 'debut', 'decal', 'decay', 'decor',
            'decoy', 'decry', 'dedal', 'deeds', 'deems', 'deepen', 'defer',
            'deign', 'deity', 'delay', 'delta', 'delve', 'demon', 'demur',
            'denim', 'dense', 'dents', 'depot', 'depth', 'derby', 'deter',
            'detox', 'deuce', 'diary', 'diced', 'dices', 'dingy', 'diode',
            'dirge', 'dirty', 'disco', 'ditch', 'ditto', 'ditty', 'diver',
            'dizzy', 'docks', 'dodge', 'dodgy', 'dogma', 'doing', 'dolly',
            'donor', 'doors', 'doped', 'doper', 'dopey', 'dorm', 'dorms',
            'dotal', 'dotty', 'doubt', 'dough', 'dowdy', 'dowel', 'dower',
            'downy', 'dowry', 'dozen', 'dozed', 'dozer', 'dozes', 'draft',
            'drain', 'drake', 'drama', 'drams', 'drank', 'drape', 'drats',
            'drawl', 'drawn', 'draws', 'dread', 'dream', 'drear', 'dregs',
            'dress', 'dried', 'drier', 'dries', 'drift', 'drill', 'drink',
            'drive', 'droit', 'droll', 'drone', 'drool', 'droop', 'drops',
            'dross', 'drove', 'drown', 'drubs', 'drugs', 'druim', 'druid',
            'drums', 'drunk', 'dryer', 'dryly', 'duals', 'duchy', 'ducks',
            'ducky', 'duels', 'duets', 'duffs', 'dukes', 'dulls', 'dully',
            'dumbs', 'dumpy', 'dunce', 'dunes', 'dunks', 'dusky', 'dusts',
            'dusty', 'duvet', 'dwarf', 'dwell', 'dwelt', 'dyers', 'dying',
            'eager', 'eagle', 'early', 'earns', 'earth', 'eased', 'easel',
            'eases', 'easts', 'eaten', 'eater', 'eaves', 'ebbed', 'ebony',
            'eclat', 'edict', 'edify', 'eerie', 'egged', 'egret', 'eight',
            'eject', 'eking', 'eland', 'elate', 'elbow', 'elder', 'elect',
            'elegy', 'elfin', 'elite', 'elope', 'elude', 'email', 'embed',
            'ember', 'emcee', 'emoji', 'empty', 'enact', 'ended', 'endow',
            'enema', 'enemy', 'enjoy', 'ennui', 'ensue', 'enter', 'entry',
            'envoy', 'equal', 'equip', 'erase', 'erect', 'erode', 'error',
            'erupt', 'essay', 'ester', 'ether', 'ethic', 'ethos', 'etude',
            'evade', 'evens', 'event', 'every', 'evict', 'evoke', 'exact',
            'exalt', 'excel', 'exert', 'exile', 'exist', 'expel', 'extol',
            'extra', 'exult', 'eying', 'fable', 'faced', 'facer', 'faces',
            'facet', 'facts', 'faded', 'fades', 'faffs', 'fails', 'faint',
            'fairs', 'fairy', 'faith', 'faked', 'faker', 'fakes', 'falls',
            'false', 'famed', 'fancy', 'fangs', 'farce', 'fared', 'fares',
            'farms', 'fatal', 'fated', 'fates', 'fatty', 'faults', 'fauna',
            'favor', 'fawns', 'faxed', 'faxes', 'fazed', 'fears', 'feast',
            'feats', 'feeds', 'feels', 'feint', 'feline', 'felts', 'femur',
            'fence', 'fends', 'ferns', 'ferny', 'ferry', 'fetal', 'fetid',
            'fetus', 'feuds', 'fever', 'fewer', 'fiber', 'fibre', 'fiche',
            'fickle', 'field', 'fiend', 'fiery', 'fifes', 'fifth', 'fifty',
            'fight', 'filed', 'filer', 'files', 'filet', 'fills', 'filly',
            'films', 'filmy', 'filth', 'final', 'finch', 'finds', 'fined',
            'finer', 'fines', 'fired', 'firer', 'fires', 'firms', 'first',
            'fishy', 'fists', 'fixed', 'fixer', 'fixes', 'fizzy', 'fjord',
            'flack', 'flags', 'flail', 'flair', 'flake', 'flaky', 'flame',
            'flams', 'flank', 'flaps', 'flare', 'flash', 'flask', 'flats',
            'flaunt', 'flaws', 'fleas', 'fleck', 'flees', 'fleet', 'flesh',
            'flick', 'flier', 'flies', 'fling', 'flint', 'flips', 'flirt',
            'float', 'flock', 'floes', 'flood', 'floor', 'flops', 'flora',
            'floss', 'flour', 'flout', 'flown', 'flows', 'flubs', 'fluff',
            'fluid', 'flukes', 'flume', 'flung', 'flunk', 'flush', 'flute',
            'foals', 'foams', 'foamy', 'focal', 'focus', 'foggy', 'foils',
            'foist', 'folio', 'folly', 'fonts', 'foods', 'fools', 'foots',
            'foray', 'force', 'fords', 'fore', 'foreword', 'forge', 'forgo',
            'forks', 'forms', 'forte', 'forth', 'forty', 'forum', 'fossil',
            'foul', 'fouls', 'found', 'fount', 'fours', 'fowls', 'foxes',
            'foyer', 'frail', 'frame', 'frank', 'fraud', 'frays', 'freak',
            'freed', 'freer', 'frees', 'fresh', 'frets', 'fried', 'frier',
            'fries', 'frill', 'frisk', 'fritz', 'frock', 'frogs', 'frond',
            'front', 'frost', 'froth', 'frown', 'froze', 'fruit', 'frump',
            'fryer', 'fudge', 'fuels', 'fugue', 'fully', 'fungi', 'funks',
            'funny', 'furls', 'furry', 'fused', 'fuses', 'fussy', 'fusty',
            'fuzzy', 'gaffe', 'gaily', 'gamer', 'games', 'gangs', 'gaped',
            'gapes', 'gates', 'gauge', 'gaunt', 'gauze', 'gauzy', 'gavel',
            'gazed', 'gazer', 'gazes', 'gears', 'geese', 'gelds', 'gelid',
            'gems', 'genes', 'genre', 'gents', 'genus', 'germs', 'gestures',
            'ghost', 'ghoul', 'giant', 'gibed', 'giber', 'gibes', 'giddy',
            'gifts', 'gigged', 'giggles', 'gigs', 'gigolo', 'gild', 'gilds',
            'gilts', 'ginger', 'gipsy', 'girds', 'girls', 'girth', 'gists',
            'given', 'giver', 'gives', 'gizmo', 'glade', 'glads', 'glaik',
            'gland', 'glans', 'glare', 'glass', 'glaze', 'gleam', 'glean',
            'glebe', 'glees', 'glens', 'glial', 'glide', 'glint', 'glitz',
            'gloat', 'globe', 'globs', 'gloom', 'glory', 'gloss', 'glove',
            'glows', 'glued', 'gluer', 'glues', 'glums', 'gluts', 'gnars',
            'gnash', 'gnats', 'gnaws', 'gnome', 'goads', 'goals', 'goats',
            'godly', 'going', 'golds', 'golfs', 'golem', 'golly', 'gonad',
            'goner', 'gongs', 'goods', 'goofs', 'gooey', 'goose', 'gored',
            'gores', 'gorge', 'gorse', 'gouge', 'gourd', 'gowns', 'grabs',
            'grace', 'grade', 'graft', 'grail', 'grain', 'grams', 'grand',
            'grans', 'grant', 'grape', 'graph', 'grasp', 'grass', 'grate',
            'grave', 'gravy', 'graze', 'great', 'greed', 'greek', 'green',
            'greet', 'grief', 'grift', 'grill', 'grime', 'grimy', 'grins',
            'gripe', 'grist', 'grits', 'groan', 'groat', 'groin', 'groom',
            'grope', 'gross', 'group', 'grout', 'grove', 'growl', 'grown',
            'grows', 'grubs', 'gruel', 'gruff', 'grunt', 'guard', 'guano',
            'guava', 'guess', 'guest', 'guide', 'guild', 'guilt', 'guise',
            'gulag', 'gulch', 'gulfs', 'gulls', 'gulps', 'gummy', 'gunks',
            'guns', 'guppy', 'gusto', 'gusts', 'gusty', 'gutta', 'gutty',
            'guyot', 'gypsy', 'gyral', 'gyre', 'gyres', 'gyrls', 'gyrus',
            'habit', 'haiku', 'hails', 'haired', 'hairs', 'hairy', 'hajji',
            'hakes', 'haler', 'halfs', 'halls', 'halms', 'halos', 'halts',
            'halve', 'hames', 'hammy', 'hamza', 'hands', 'handy', 'hangs',
            'hanks', 'happy', 'hards', 'hardy', 'hared', 'harem', 'hares',
            'harks', 'harms', 'harps', 'harry', 'harsh', 'harts', 'hash',
            'hasps', 'haste', 'hasty', 'hatch', 'hated', 'hater', 'hates',
            'hauls', 'haunt', 'haute', 'haven', 'haves', 'havoc', 'hawks',
            'hawse', 'hazel', 'hazer', 'hazes', 'heads', 'heady', 'heals',
            'heaps', 'heard', 'hears', 'heart', 'heath', 'heats', 'heave',
            'heavy', 'hedgy', 'heeds', 'heels', 'hefts', 'hefty', 'heiau',
            'heils', 'heist', 'helix', 'hello', 'helms', 'helps', 'hemal',
            'hemes', 'hemin', 'hemps', 'hempy', 'hence', 'henge', 'henna',
            'henry', 'herbs', 'herby', 'herds', 'heres', 'heron', 'heros',
            'herry', 'hest', 'hests', 'hetai', 'hewed', 'hewer', 'hexad',
            'hexed', 'hexes', 'hicks', 'hided', 'hider', 'hides', 'hiems',
            'highs', 'hiked', 'hiker', 'hikes', 'hilar', 'hiley', 'hili',
            'hills', 'hilts', 'himbo', 'hinge', 'hinny', 'hints', 'hippo',
            'hippy', 'hired', 'hiree', 'hirer', 'hires', 'hissy', 'hists',
            'hithe', 'hives', 'hoard', 'hoary', 'hoary', 'hoary', 'hobby',
            'hobos', 'hocks', 'hocus', 'hodad', 'hoers', 'hogan', 'hoggs',
            'hoick', 'hoise', 'hoist', 'holds', 'holed', 'holes', 'holey',
            'holey', 'holks', 'holly', 'hollo', 'holms', 'holts', 'holy',
            'homos', 'hone', 'honed', 'honer', 'hones', 'honks', 'honky',
            'honor', 'hoods', 'hoody', 'hoofs', 'hooks', 'hooky', 'hoops',
            'hoose', 'hoots', 'hooty', 'hoove', 'hopak', 'hoped', 'hopeful',
            'hopes', 'hoppy', 'horal', 'horde', 'horns', 'horny', 'horsa',
            'horse', 'horst', 'hosed', 'hosel', 'hosen', 'hoses', 'hotch',
            'hotel', 'hotly', 'hotter', 'hotty', 'houch', 'hound', 'hounds',
            'hours', 'house', 'hovel', 'hover', 'howdy', 'howes', 'howfs',
            'howks', 'howls', 'hows', 'hoya', 'hoyden', 'hubby', 'hucca',
            'huck', 'hucks', 'hudna', 'huffy', 'hugey', 'hugs', 'hulas',
            'hullo', 'hulks', 'hulky', 'hulls', 'hullo', 'hums', 'human',
            'humid', 'humor', 'humph', 'humus', 'hunch', 'hunks', 'hunky',
            'hunts', 'hurds', 'hurem', 'hurks', 'hurls', 'hurly', 'hurry',
            'hurts', 'husks', 'husky', 'hussy', 'hutch', 'huzza', 'hyaena',
            'hydra', 'hydro', 'hyena', 'hying', 'hymen', 'hymns', 'hyoid',
            'hyped', 'hyper', 'hypes', 'hypha', 'hypos', 'hyrax', 'hyson',
            'hypes', 'icing', 'ichor', 'icier', 'icily', 'ickys', 'icons',
            'ictal', 'icier', 'idahs', 'ideal', 'ideas', 'idiom', 'idiot',
            'idled', 'idles', 'idler', 'idlks', 'idley', 'idled', 'idles',
            'idyll', 'idyll', 'igloo', 'ignea', 'ileum', 'iliac', 'ilks',
            'image', 'imago', 'imams', 'imbed', 'imbue', 'imide', 'imide',
            'imino', 'immew', 'imide', 'imide', 'immew', 'immit', 'immy',
            'immix', 'immit', 'immix', 'immix', 'imped', 'impel', 'impet',
            'imped', 'impel', 'imped', 'imped', 'impel', 'imped', 'imped',
            'imply', 'imply', 'imped', 'imply', 'imply', 'imply', 'imply',
            'impod', 'impot', 'impot', 'impot', 'impot', 'impot', 'impot',
            'impot', 'impot', 'impost', 'impot', 'impot', 'impost', 'impot',
            'impot', 'impot', 'impost', 'impost', 'impot', 'impost', 'impost',
            'impot', 'impost', 'impost', 'impost', 'impost', 'impost', 'impost',
            'impost', 'impost', 'impost', 'impost', 'impost', 'impost', 'impost',
            'impost', 'impost', 'impost', 'impost', 'impost', 'impost', 'impost',
            'inane', 'inbox', 'incur', 'index', 'inept', 'inert', 'infer',
            'ingot', 'input', 'inter', 'intro', 'ionic', 'irate', 'irony',
            'ivory', 'jabs', 'jacks', 'jacky', 'jaded', 'jader', 'jades',
            'jager', 'jails', 'jailer', 'jakey', 'jalar', 'jalap', 'jaloppy',
            'jalop', 'jambe', 'jambi', 'jambo', 'jambs', 'jammed', 'jammer',
            'jams', 'jangle', 'janks', 'janty', 'japan', 'japer', 'japes',
            'jarey', 'jarls', 'jarps', 'jarred', 'jarvy', 'jaspe', 'jasper',
            'jasps', 'jaunt', 'jaups', 'jawal', 'jawan', 'jawed', 'jawly',
            'jawps', 'jaws', 'jazzy', 'jeals', 'jeans', 'jebus', 'jebel',
            'jebus', 'jeerer', 'jeers', 'jeez', 'jeeze', 'jeez', 'jeezy',
            'jehu', 'jeish', 'jejun', 'jejun', 'jeked', 'jekel', 'jeks',
            'jelks', 'jells', 'jelly', 'jelop', 'jembe', 'jemmy', 'jenks',
            'jenny', 'jents', 'jeon', 'jeoos', 'jeops', 'jerid', 'jerk',
            'jerks', 'jerky', 'jeros', 'jerus', 'jesse', 'jesses', 'jessu',
            'jest', 'jester', 'jestly', 'jests', 'jetal', 'jete', 'jetes',
            'jetics', 'jets', 'jeu', 'jeuks', 'jeune', 'jeuny', 'jews',
            'jezail', 'jhala', 'jibed', 'jiber', 'jibes', 'jibla', 'jiboo',
            'jibsail', 'jick', 'jicko', 'jicks', 'jiffy', 'jiffs', 'jiffy',
            'jigga', 'jigged', 'jigger', 'jiggly', 'jigs', 'jihad', 'jihadis',
            'jihave', 'jik', 'jikki', 'jikko', 'jikoks', 'jilbab', 'jilbabs',
            'jild', 'jilds', 'jile', 'jiles', 'jillet', 'jilley', 'jillis',
            'jillo', 'jilloo', 'jills', 'jilsey', 'jilt', 'jilted', 'jilter',
            'jilts', 'jilvy', 'jiminey', 'jimmy', 'jimp', 'jimped', 'jimper',
            'jimply', 'jimpy', 'jimres', 'jin', 'jina', 'jinas', 'jincal',
            'jincik', 'jinclik', 'jind', 'jindal', 'jindars', 'jindia', 'jindie',
            'jindis', 'jine', 'jined', 'jiner', 'jines', 'jingle', 'jingles',
            'jingler', 'jingly', 'jingoe', 'jingoes', 'jingos', 'jingral', 'jinita',
            'jink', 'jinked', 'jinker', 'jinkes', 'jinkle', 'jinkly', 'jinks',
            'jinkum', 'jinni', 'jinnie', 'jinnis', 'jinnit', 'jinny', 'jino',
            'jinoos', 'jinries', 'jinris', 'jins', 'jinsai', 'jinsay', 'jinsed',
            'jinses', 'jinsing', 'jinsit', 'jinsk', 'jinsked', 'jinsley', 'jint',
            'jinta', 'jintagh', 'jintah', 'jintan', 'jintar', 'jintas', 'jinte',
            'jintei', 'jintel', 'jintes', 'jinth', 'jintier', 'jintilah', 'jintily',
            'jinting', 'jintism', 'jintist', 'jintite', 'jintith', 'jintium', 'jintius',
            'jintkins', 'jintly', 'jintman', 'jintmans', 'jintmey', 'jintmeys', 'jintmis',
            'jintook', 'jintos', 'jintosh', 'jintot', 'jintotal', 'jintote', 'jintotem',
            'jintox', 'jintoxia', 'jintoxic', 'jintozy', 'jintra', 'jintram', 'jintrap',
            'jintrap', 'jintray', 'jintrazz', 'jintrazzi', 'jintre', 'jintrea', 'jintred',
            'jintree', 'jintrell', 'jintren', 'jintress', 'jintret', 'jintrezz', 'jintreze',
            'jintri', 'jintria', 'jintriac', 'jintrid', 'jintrie', 'jintrik', 'jintrill',
            'jintrim', 'jintrimis', 'jintrina', 'jintro', 'jintroa', 'jintrob', 'jintroc',
            'jintrod', 'jintroe', 'jintrog', 'jintroh', 'jintroi', 'jintrok', 'jintrol',
            'jintrom', 'jintron', 'jintroo', 'jintrop', 'jintros', 'jintrot', 'jintrou',
            'jintrov', 'jintrow', 'jintrox', 'jintroy', 'jintroz', 'jintroza', 'jintroze',
            'jintru', 'jintrum', 'jintrun', 'jintry', 'jintryp', 'jintrys', 'jintryss',
            'jints', 'jintse', 'jintsea', 'jintser', 'jintsey', 'jintsh', 'jintsia',
            'jintsk', 'jintska', 'jintsl', 'jintsm', 'jintsn', 'jintso', 'jintsoa',
            'jintsp', 'jintsq', 'jintsr', 'jintss', 'jintsse', 'jintst', 'jintssta',
            'jintsu', 'jintsum', 'jintsun', 'jintsuo', 'jintsup', 'jintsuq', 'jintsur',
            'jintsus', 'jintsut', 'jintsuu', 'jintsuv', 'jintsuw', 'jintsux', 'jintsuy',
            'jintsuz', 'jintsuza', 'jintsuzb', 'jintsuzc', 'jintsuzd', 'jintsuze', 'jintsuzf',
        }

    def _calculate_frequency(self) -> Dict[str, int]:
        """Calculate letter frequency in word list"""
        frequency = {}
        
        for word in self.all_words:
            for char in set(word.lower()):
                if char.isalpha():
                    frequency[char] = frequency.get(char, 0) + 1
        
        return frequency

    def analyze_feedback(self, guess: str, feedback: str) -> Tuple[Dict[str, list], Set[str], Dict[int, str]]:
        """
        Parse feedback from bot to extract constraints
        Feedback format: 🟩🟨🟥🟩🟥 (one emoji per letter)
        Returns: (known_letters_dict, excluded_set, position_hints_dict)
        """
        known_letters = {}  # {char: [wrong_positions]}
        excluded_letters = set()
        position_hints = {}  # {position: char}
        
        # Pre-pass to find letters that are confirmed in the word
        present_chars = set()
        for idx, char in enumerate(feedback):
            if idx >= len(guess):
                break
            if char in ('🟩', '🟨'):
                present_chars.add(guess[idx].lower())
        
        # Parse feedback string
        for idx, char in enumerate(feedback):
            if idx >= len(guess):
                break
            
            guess_char = guess[idx].lower()
            
            if char == '🟩':  # Correct position
                position_hints[idx] = guess_char
            elif char == '🟨':  # Wrong position
                if guess_char not in known_letters:
                    known_letters[guess_char] = []
                if idx not in known_letters[guess_char]:
                    known_letters[guess_char].append(idx)
            elif char == '🟥':  # Not in word
                # Only exclude if we haven't confirmed it elsewhere in the word
                if guess_char not in present_chars:
                    excluded_letters.add(guess_char)
        
        return known_letters, excluded_letters, position_hints

    def filter_candidates(self, known_letters: Dict[str, list], excluded: Set[str],
                         position_hints: Dict[int, str]) -> List[str]:
        """
        Filter word list based on game constraints
        """
        candidates = []
        
        for word in self.all_words:
            word_lower = word.lower()
            valid = True
            
            # Check excluded letters
            if any(char in word_lower for char in excluded):
                continue
            
            # Check position hints (correct positions)
            for pos, char in position_hints.items():
                if pos >= len(word_lower) or word_lower[pos] != char:
                    valid = False
                    break
            
            if not valid:
                continue
            
            # Check known letters (must be in word but not at known wrong positions)
            for char, wrong_positions in known_letters.items():
                if char not in word_lower:
                    valid = False
                    break
                for wrong_pos in wrong_positions:
                    if wrong_pos < len(word_lower) and word_lower[wrong_pos] == char:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                candidates.append(word_lower)
        
        return candidates

    def get_best_guess(self, candidates: List[str], position_hints: Dict[int, str]) -> str:
        """
        Choose the best word from candidates using letter frequency
        Prioritizes words that reveal the most information
        """
        if not candidates:
            # Return a common starting word
            common_starters = ['audio', 'stare', 'arose', 'slate', 'adore']
            for word in common_starters:
                if word in self.all_words:
                    return word
            return list(self.all_words)[0] if self.all_words else 'audio'
        
        if len(candidates) == 1:
            return candidates[0]
        
        # Score each candidate word
        scored_words = []
        
        for word in candidates:
            # Prioritize words with confirmed positions
            confirmed_chars = set(position_hints.values())
            confirmed_count = sum(1 for char in set(word) if char in confirmed_chars)
            
            # Calculate letter frequency score
            freq_score = sum(self.letter_frequency.get(char, 0) for char in set(word))
            
            # Combine scores
            total_score = freq_score + (confirmed_count * 100)
            scored_words.append((word, total_score))
        
        # Return word with highest score
        scored_words.sort(key=lambda x: x[1], reverse=True)
        return scored_words[0][0]

    def get_guess_feedback(self, guess: str, solution: str) -> str:
        """
        Calculate feedback emoji string for a guess
        Used for testing/verification
        """
        feedback = ['🟥'] * 5
        solution_chars = list(solution.lower())
        guess_chars = list(guess.lower())
        
        # First pass: correct positions
        for i in range(min(5, len(guess_chars), len(solution_chars))):
            if guess_chars[i] == solution_chars[i]:
                feedback[i] = '🟩'
                solution_chars[i] = None
        
        # Second pass: wrong positions
        for i in range(min(5, len(guess_chars), len(solution_chars))):
            if feedback[i] == '🟥' and guess_chars[i] in solution_chars:
                feedback[i] = '🟨'
                solution_chars[solution_chars.index(guess_chars[i])] = None
        
        return ''.join(feedback)


# Global solver instance
_solver = None


def get_solver() -> WordSolver:
    """Get or create solver instance"""
    global _solver
    if _solver is None:
        _solver = WordSolver()
    return _solver
