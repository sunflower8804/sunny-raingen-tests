import os
from copy import copy

import pygame
import ujson

from scripts.game_structure.game_essentials import game


class Sprites:
    cat_tints = {}
    white_patches_tints = {}
    clan_symbols = []

    def __init__(self):
        """Class that handles and hold all spritesheets. 
        Size is normally automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.symbol_dict = None
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None

        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading Tints")
        #If you want less white patches, place hashtags below!
        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading White Patches Tints")

        #If you want less white patches, place hashtages above and remove below!
        #try:
            #with open("sprites/dicts/white_patches_lesstint.json", 'r') as read_file:
                #self.white_patches_tints = ujson.loads(read_file.read())
        #except IOError:
            #print("ERROR: Reading White Patches Less Tints")
        #If you want less white patches, remove hashtags above!

    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7,
                   no_index=False):  # pos = ex. (2, 3), no single pixels

        """
        Divide sprites on a spritesheet into groups of sprites that are easily accessible
        :param spritesheet: Name of spritesheet file
        :param pos: (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites
        :param name: Name of group being made
        :param sprites_x: default 3, number of sprites horizontally
        :param sprites_y: default 3, number of sprites vertically
        :param no_index: default False, set True if sprite name does not require cat pose index
        """

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                if no_index:
                    full_name = f"{name}"
                else:
                    full_name = f"{name}{i}"

                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )

                except ValueError:
                    # Fallback for non-existent sprites
                    print(f"WARNING: nonexistent sprite - {full_name}")
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite

                self.sprites[full_name] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart  # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50  # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and "
                  f"do a search for 'if width / 3 == height / 7:'")

        del width, height  # unneeded

        for x in [
            'lineart', 'lineartdf', 'lineartdead',
            'eyes', 'eyes2', 'skin', 'gilltongue',
            'scars', 'missingscars',
            'medcatherbs', 'moreaccs',
            'collars', 'bellcollars', 'bowcollars', 'nyloncollars', 'rwlizards', 'drones', 'muddypaws', 'herbs2',
            'singlecolours', 'speckledcolours', 'tabbycolours', 'bengalcolours', 'marbledcolours',
            'rosettecolours', 'smokecolours', 'tickedcolours', 'mackerelcolours', 'classiccolours',
            'sokokecolours', 'agouticolours', 'singlestripecolours', 'maskedcolours', 'bananacolours',
            'centipedecolours', 'collaredcolours', 'concolours', 'gravelcolours', 'cyanlizardcolours',
            'slimemoldcolours', 'lanterncolours', 'vulturecolours', 'lizardcolours', 'leviathancolours',
            'fluffycolours', 'amoebacolours', 'seaslugcolours', 'yeekcolours', 'raineyes', 'raineyes2',
            'shadersnewwhite', 'lightingnew',
            'whitepatches', 'tortiepatchesmasks',
            'fademask', 'fadestarclan', 'fadedarkforest',
            'symbols'
        ]:
            if 'lineart' in x and game.config['fun']['april_fools']:
                self.spritesheet(f"sprites/aprilfools{x}.png", x)
            else:
                self.spritesheet(f"sprites/{x}.png", x)

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        for a, i in enumerate(
                ['YELLOW', 'AMBER', 'HAZEL', 'PALEGREEN', 'GREEN', 'BLUE', 
                'DARKBLUE', 'GREY', 'CYAN', 'EMERALD', 'HEATHERBLUE', 'SUNLITICE']):
            self.make_group('eyes', (a, 0), f'eyes{i}')
            self.make_group('eyes2', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['COPPER', 'SAGE', 'COBALT', 'PALEBLUE', 'BRONZE', 'SILVER',
                'PALEYELLOW', 'GOLD', 'GREENYELLOW', 'RED', 'PURPLE', 'MAUVE']):
            self.make_group('eyes', (a, 1), f'eyes{i}')
            self.make_group('eyes2', (a, 1), f'eyes2{i}')
        #rain's eyes
        for a, i in enumerate(
                ['ELECTRICBLUE', 'VIOLET', 'PINK', 'SNOW', 'ORANGE', 'CREAM', 'SEAFOAM', 'CRIMSON', 'NAVY', 'VOIDGOLD', 'COOLBROWN', 'PLUM']):
            self.make_group('raineyes', (a, 0), f'eyes{i}')
            self.make_group('raineyes2', (a, 0), f'eyes2{i}')
        for a, i in enumerate(
                ['INDIGO', 'LILAC']):
            self.make_group('raineyes', (a, 1), f'eyes{i}')
            self.make_group('raineyes2', (a, 1), f'eyes2{i}')

        # white patches
        for a, i in enumerate(['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO',
            'MOON', 'PHANTOM', 'POWDER', 'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE']):
            self.make_group('whitepatches', (a, 0), f'white{i}')
        for a, i in enumerate(['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL', 
            'LIGHTSONG', 'VITILIGO', 'BLACKSTAR', 'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL']):
            self.make_group('whitepatches', (a, 1), f'white{i}')
        # ryos white patches
        for a, i in enumerate(['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO',
            'PAWS', 'MITAINE', 'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD']):
            self.make_group('whitepatches', (a, 2), f'white{i}')
        for a, i in enumerate(['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY',
            'FAROFA', 'DAMIEN', 'MISTER', 'BELLY', 'TAILTIP', 'TOES', 'TOPCOVER']):
            self.make_group('whitepatches', (a, 3), f'white{i}')
        for a, i in enumerate(
                ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW',
                'PANTS', 'REVERSEPANTS', 'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW']):
            self.make_group('whitepatches', (a, 4), f'white{i}')
        # beejeans white patches + perrio's point marks, painted, and heart2 + anju's new marks + key's blackstar
        for a, i in enumerate(['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT',
            'MAO', 'LUNA', 'CHESTSPECK', 'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER']):
            self.make_group('whitepatches', (a, 5), f'white{i}')
        # acorn's white patches + ryos' bub + fable lovebug + frankie trixie
        for a, i in enumerate(['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART',
            'SPARROW', 'VEST', 'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE']):
            self.make_group('whitepatches', (a, 6), f'white{i}')
        # acorn's white patches: the sequel
        for a, i in enumerate(['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE',
            'FADEBELLY', 'FRONT', 'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS']):
            self.make_group('whitepatches', (a, 7), f'white{i}')
        for a, i in enumerate(['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR',
            'BUSTER', 'SMOKEY', 'HAWKBLAZE', 'CAKE', 'ROSINA', 'PRINCESS']):
            self.make_group('whitepatches', (a, 8), f'white{i}')
        for a, i in enumerate(['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE']):
            self.make_group('whitepatches', (a, 9), 'white' + i)

        # single (solid)
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('singlecolours', (a, 0), f'single{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('singlecolours', (a, 1), f'single{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('singlecolours', (a, 2), f'single{i}')
        # tabby
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('tabbycolours', (a, 0), f'tabby{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('tabbycolours', (a, 1), f'tabby{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('tabbycolours', (a, 2), f'tabby{i}')
        # marbled
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('marbledcolours', (a, 0), f'marbled{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('marbledcolours', (a, 1), f'marbled{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('marbledcolours', (a, 2), f'marbled{i}')
        # rosette
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('rosettecolours', (a, 0), f'rosette{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('rosettecolours', (a, 1), f'rosette{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('rosettecolours', (a, 2), f'rosette{i}')
        # smoke
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('smokecolours', (a, 0), f'smoke{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('smokecolours', (a, 1), f'smoke{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('smokecolours', (a, 2), f'smoke{i}')
        # ticked
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('tickedcolours', (a, 0), f'ticked{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('tickedcolours', (a, 1), f'ticked{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('tickedcolours', (a, 2), f'ticked{i}')
        # speckled
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('speckledcolours', (a, 0), f'speckled{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('speckledcolours', (a, 1), f'speckled{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('speckledcolours', (a, 2), f'speckled{i}')
        # bengal
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('bengalcolours', (a, 0), f'bengal{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('bengalcolours', (a, 1), f'bengal{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('bengalcolours', (a, 2), f'bengal{i}')
        # mackerel
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('mackerelcolours', (a, 0), f'mackerel{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('mackerelcolours', (a, 1), f'mackerel{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('mackerelcolours', (a, 2), f'mackerel{i}')
        # classic
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('classiccolours', (a, 0), f'classic{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('classiccolours', (a, 1), f'classic{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('classiccolours', (a, 2), f'classic{i}')
        # sokoke
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('sokokecolours', (a, 0), f'sokoke{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('sokokecolours', (a, 1), f'sokoke{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('sokokecolours', (a, 2), f'sokoke{i}')
        # agouti
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('agouticolours', (a, 0), f'agouti{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('agouticolours', (a, 1), f'agouti{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('agouticolours', (a, 2), f'agouti{i}')
        # singlestripe
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('singlestripecolours', (a, 0), f'singlestripe{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('singlestripecolours', (a, 1), f'singlestripe{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('singlestripecolours', (a, 2), f'singlestripe{i}')
        # masked tabby
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('maskedcolours', (a, 0), f'masked{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('maskedcolours', (a, 1), f'masked{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('maskedcolours', (a, 2), f'masked{i}')
        # gravel
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('gravelcolours', (a, 0), f'gravel{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('gravelcolours', (a, 1), f'gravel{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('gravelcolours', (a, 2), f'gravel{i}')
        # collared
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('collaredcolours', (a, 0), f'collared{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('collaredcolours', (a, 1), f'collared{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('collaredcolours', (a, 2), f'collared{i}')
        # slimemold
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('slimemoldcolours', (a, 0), f'slimemold{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('slimemoldcolours', (a, 1), f'slimemold{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('slimemoldcolours', (a, 2), f'slimemold{i}')
        # cyan lizard
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('cyanlizardcolours', (a, 0), f'cyanlizard{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('cyanlizardcolours', (a, 1), f'cyanlizard{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('cyanlizardcolours', (a, 2), f'cyanlizard{i}')
        # vulture
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('vulturecolours', (a, 0), f'vulture{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('vulturecolours', (a, 1), f'vulture{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('vulturecolours', (a, 2), f'vulture{i}')
        # banana
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('bananacolours', (a, 0), f'banana{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('bananacolours', (a, 1), f'banana{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('bananacolours', (a, 2), f'banana{i}')
        # centipede
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('centipedecolours', (a, 0), f'centipede{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('centipedecolours', (a, 1), f'centipede{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('centipedecolours', (a, 2), f'centipede{i}')
        # conductor
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('concolours', (a, 0), f'conductor{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('concolours', (a, 1), f'conductor{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('concolours', (a, 2), f'conductor{i}')
        # lizard
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('lizardcolours', (a, 0), f'lizard{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('lizardcolours', (a, 1), f'lizard{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('lizardcolours', (a, 2), f'lizard{i}')
        # lantern
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('lanterncolours', (a, 0), f'lantern{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('lanterncolours', (a, 1), f'lantern{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('lanterncolours', (a, 2), f'lantern{i}')
        # leviathan
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('leviathancolours', (a, 0), f'leviathan{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('leviathancolours', (a, 1), f'leviathan{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('leviathancolours', (a, 2), f'leviathan{i}')
        # fluffy
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('fluffycolours', (a, 0), f'fluffy{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('fluffycolours', (a, 1), f'fluffy{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('fluffycolours', (a, 2), f'fluffy{i}')
        # amoeba
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('amoebacolours', (a, 0), f'amoeba{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('amoebacolours', (a, 1), f'amoeba{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('amoebacolours', (a, 2), f'amoeba{i}')
        # seaslug
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('seaslugcolours', (a, 0), f'seaslug{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('seaslugcolours', (a, 1), f'seaslug{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('seaslugcolours', (a, 2), f'seaslug{i}')
        # yeekpelt
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('yeekcolours', (a, 0), f'yeek{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('yeekcolours', (a, 1), f'yeek{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('yeekcolours', (a, 2), f'yeek{i}')

        # new new torties
        for a, i in enumerate(['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE']):
            self.make_group('tortiepatchesmasks', (a, 0), f"tortiemask{i}")
        for a, i in enumerate(['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL', 'GRUMPYFACE']):
            self.make_group('tortiepatchesmasks', (a, 1), f"tortiemask{i}")
        for a, i in enumerate(['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE']):
            self.make_group('tortiepatchesmasks', (a, 2), f"tortiemask{i}")
        for a, i in enumerate(['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY']):
            self.make_group('tortiepatchesmasks', (a, 3), f"tortiemask{i}")
        for a, i in enumerate(['SHILOH', 'FRECKLED', 'HEARTBEAT']):
            self.make_group('tortiepatchesmasks', (a, 4), f"tortiemask{i}")

        # torties adjusted for raingen
        #for a, i in enumerate(['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH']):
            #self.make_group('tortiepatchesmasks', (a, 0), f"tortiemask{i}")
        #for a, i in enumerate(['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP']):
            #self.make_group('tortiepatchesmasks', (a, 1), f"tortiemask{i}")
        #for a, i in enumerate(['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE']):
            #self.make_group('tortiepatchesmasks', (a, 2), f"tortiemask{i}")
        #for a, i in enumerate(['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL']):
            #self.make_group('tortiepatchesmasks', (a, 3), f"tortiemask{i}")

        # SKINS
        for a, i in enumerate(['BLACK', 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN', "RED"]):
            self.make_group('skin', (a, 0), f"skin{i}")
        for a, i in enumerate(['DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH']):
            self.make_group('skin', (a, 1), f"skin{i}")
        for a, i in enumerate(['DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE']):
            self.make_group('skin', (a, 2), f"skin{i}")
        # Gills, Tongues, Quills
        for a, i in enumerate(['PINKGILLS', 'BLUEGILLS', 'REDGILLS', 'LIMEGILLS', 'YELLOWGILLS', 'WHITEGILLS']):
            self.make_group('gilltongue', (a, 0), f"skin{i}")
        for a, i in enumerate(['RAINBOWGILLS', 'FUCHSIATONGUE', 'PASTELTONGUE', 'KOBITONGUE', 'REDTONGUE', 'GREYTONGUE']):
            self.make_group('gilltongue', (a, 1), f"skin{i}")
        for a, i in enumerate(['ORANGETONGUE', 'WHITESPOTS', 'BLACKSPOTS', 'MIXSPOTS', 'RAINBOWSPOTS']):
            self.make_group('gilltongue', (a, 2), f"skin{i}")
        for a, i in enumerate(['WHITETENNA', 'REDTENNA', 'PINKTENNA', 'ORANGETENNA', 'YELLOWTENNA', 'BLUETENNA']):
            self.make_group('gilltongue', (a, 3), f"skin{i}")
        for a, i in enumerate(['GREENTENNA', 'WHITEGLOWSPOTS', 'REDGLOWSPOTS', 'PINKGLOWSPOTS', 'ORANGEGLOWSPOTS', 'YELLOWGLOWSPOTS']):
            self.make_group('gilltongue', (a, 4), f"skin{i}")
        for a, i in enumerate(['BLUEGLOWSPOTS', 'GREENGLOWSPOTS']):
            self.make_group('gilltongue', (a, 5), f"skin{i}")

        self.load_scars()
        self.load_symbols()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """

        # Define scars
        scars_data = [
            ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
             "BOTHBLIND", "BURNPAWS", "BURNTAIL"],
            ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE", "FROSTFACE", "FROSTTAIL",
             "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"],
            ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE", "LEGBITE",
             "NECKBITE", "FACE"],
            ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]
        ]

        # define missing parts
        missing_parts_data = [
            ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW"]
        ]

        # scars 
        for row, scars in enumerate(scars_data):
            for col, scar in enumerate(scars):
                self.make_group('scars', (col, row), f'scars{scar}')

        # missing parts
        for row, missing_parts in enumerate(missing_parts_data):
            for col, missing_part in enumerate(missing_parts):
                self.make_group('missingscars', (col, row), f'scars{missing_part}')

        # accessories
        medcatherbs_data = [
            ["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "LAUREL"],
            ["BLUEBELLS", "NETTLE", "POPPY", "LAVENDER", "HERBS", "PETALS"],
            [],  # Empty row because this is the wild data, except dry herbs.
            ["OAK LEAVES", "CATMINT", "MAPLE SEED", "JUNIPER"]
        ]

        wild_data = [
            ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "MOTH WINGS", "CICADA WINGS"]
        ]

        collars_data = [
            ["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"],
            ["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"],
            ["PINK", "PURPLE", "MULTI", "INDIGO"]
        ]

        bellcollars_data = [
            ["CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL", "LIMEBELL"],
            ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"],
            ["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]
        ]

        bowcollars_data = [
            ["CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW", "LIMEBOW"],
            ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"],
            ["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]
        ]

        nyloncollars_data = [
            ["CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON", "LIMENYLON"],
            ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"],
            ["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]
        ]
        drones_data = [
            ["CRIMSONDRONE", "BLUEDRONE", "YELLOWDRONE", "CYANDRONE", "REDDRONE", "LIMEDRONE"],
            ["GREENDRONE", "RAINBOWDRONE", "BLACKDRONE", "SPIKESDRONE", "WHITEDRONE"],
            ["PINKDRONE", "PURPLEDRONE", "MULTIDRONE", "INDIGODRONE"]
        ]
        rwlizards_data = [
            ["BLUESKY", "BLUESEA", "PINKMAGENTA", "PINKPURPLE", "GREENEMERALD", "GREENLIME", "WHITEHIDDEN", "WHITEREVEALED"], 
            ["BLACKNEUTRAL", "BLACKALERT", "YELLOWORANGE", "YELLOWLEMON", "REDTOMATO", "CYANBLUE", "CYANGREEN"],
            ["ALBISALAFUSHIA", "ALBISALARED", "MELASALARED", "MELASALAFUSHIA", "MELASALAPURPLE"]
        ]
        muddypaws_data = [
            ["MUDDYPAWS"]
        ]
        herbs2_data = [
            ["SPEAR", "PEARLEAR", "KARMAFLOWER", "LILCENTI", "PEARLNECK", "REDBATNIP"], 
            ["LILFLY","BATNIP", "FLASHFRUIT", "REDFLASHFRUIT", "GREENKELP", "REDKELP"], 
            ["VULTMASK", "KINGMASK", "SCAVMASK", "TREESEED", "GLOWSTONE", "BROWNKELP"], 
            ["LILBEETLE", "EXPLOSPEAR", "GREENDRAGFLY", "BLUEDRAGFLY"]
        ]
        moreaccs_data = [
            ["MOUSEBLUE", "MOUSEYEL", "MOUSEPINK", "MOUSERED", "BATFLY", "BLUEFRUIT"], 
            ["INVEGG", "VOIDSPAWN", "GRAPPLE", "EMPTYBAG", "HERBSBAG", "REDARMOR"], 
            ["VULTGRUB", "YEEKRED", "YEEKBLUE"]
        ]
        drones_data = [
            ["CRIMSONDRONE", "BLUEDRONE", "YELLOWDRONE", "CYANDRONE", "REDDRONE", "LIMEDRONE"],
            ["GREENDRONE", "RAINBOWDRONE", "BLACKDRONE", "SPIKESDRONE", "WHITEDRONE"],
            ["PINKDRONE", "PURPLEDRONE", "MULTIDRONE", "INDIGODRONE"]
        ]

        # medcatherbs
        for row, herbs in enumerate(medcatherbs_data):
            for col, herb in enumerate(herbs):
                self.make_group('medcatherbs', (col, row), f'acc_herbs{herb}')
        self.make_group('medcatherbs', (5, 2), 'acc_herbsDRY HERBS')

        # wild
        for row, wilds in enumerate(wild_data):
            for col, wild in enumerate(wilds):
                self.make_group('medcatherbs', (col, 2), f'acc_wild{wild}')

        # collars
        for row, collars in enumerate(collars_data):
            for col, collar in enumerate(collars):
                self.make_group('collars', (col, row), f'collars{collar}')

        # bellcollars
        for row, bellcollars in enumerate(bellcollars_data):
            for col, bellcollar in enumerate(bellcollars):
                self.make_group('bellcollars', (col, row), f'collars{bellcollar}')

        # bowcollars
        for row, bowcollars in enumerate(bowcollars_data):
            for col, bowcollar in enumerate(bowcollars):
                self.make_group('bowcollars', (col, row), f'collars{bowcollar}')

        # nyloncollars
        for row, nyloncollars in enumerate(nyloncollars_data):
            for col, nyloncollar in enumerate(nyloncollars):
                self.make_group('nyloncollars', (col, row), f'collars{nyloncollar}')
        # rw lizards     
        for a, i in enumerate(
                ["BLUESKY", "BLUESEA", "PINKMAGENTA", "PINKPURPLE", "GREENEMERALD", "GREENLIME", "WHITEHIDDEN", "WHITEREVEALED", "BLACKNEUTRAL", "BLACKALERT"]):
            self.make_group('rwlizards', (a, 0), f'lizards{i}')
        for a, i in enumerate(["YELLOWORANGE", "YELLOWLEMON", "REDTOMATO", "CYANBLUE", "CYANGREEN", "ALBISALAFUSHIA", "ALBISALARED", "MELASALARED", "MELASALAFUSHIA", "MELASALAPURPLE"]):
            self.make_group('rwlizards', (a, 1), f'lizards{i}')

        # drones
        for row, drones in enumerate(drones_data):
            for col, drone in enumerate(drones):
                self.make_group('drones', (col, row), f'collars{drone}')

        #muddy paws
        for row, muddypaws in enumerate(muddypaws_data):
            for col, muddypaws in enumerate(muddypaws):
                self.make_group('muddypaws', (col, row), f'muddypaws{muddypaws}')

        #herbs 2
        for row, herbs2 in enumerate(herbs2_data):
            for col, herbs2 in enumerate(herbs2):
                self.make_group('herbs2', (col, row), f'herbs2{herbs2}')
                
        #more accs
        for row, moreaccs in enumerate(moreaccs_data):
            for col, moreaccs in enumerate(moreaccs):
                self.make_group('moreaccs', (col, row), f'moreaccs{moreaccs}')

    def load_symbols(self):
        """
        loads clan symbols
        """

        if os.path.exists('resources/dicts/clan_symbols.json'):
            with open('resources/dicts/clan_symbols.json') as read_file:
                self.symbol_dict = ujson.loads(read_file.read())

        # U and X omitted from letter list due to having no prefixes
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "V", "W", "Y", "Z"]

        # sprite names will format as "symbol{PREFIX}{INDEX}", ex. "symbolSPRING0"
        y_pos = 1
        for letter in letters:
            for i, symbol in enumerate([symbol for symbol in self.symbol_dict if
                                        letter in symbol and self.symbol_dict[symbol]["variants"]]):
                x_mod = 0
                for variant_index in range(self.symbol_dict[symbol]["variants"]):
                    x_mod += variant_index
                    self.clan_symbols.append(f"symbol{symbol.upper()}{variant_index}")
                    self.make_group('symbols',
                                    (i + x_mod, y_pos),
                                    f"symbol{symbol.upper()}{variant_index}",
                                    sprites_x=1, sprites_y=1, no_index=True)

            y_pos += 1

    def dark_mode_symbol(self, symbol):
        """Change the color of the symbol to dark mode, then return it
        :param Surface symbol: The clan symbol to convert"""
        dark_mode_symbol = copy(symbol)
        var = pygame.PixelArray(dark_mode_symbol)
        var.replace((87, 76, 45), (239, 229, 206))
        del var
        # dark mode color (239, 229, 206)
        # debug hot pink (255, 105, 180)

        return dark_mode_symbol

# CREATE INSTANCE
sprites = Sprites()
