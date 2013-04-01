#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 et :
#
# Author:
#  Nirbheek Chauhan <nirbheek.chauhan@gmail.com>
# License:
#  CC BY-SA
#  http://creativecommons.org/licenses/by-sa/3.0/
#
# *A* mapping from Devanagari Unicode to Bharati Braille
# 
# References and resources used:
# * http://acharya.iitm.ac.in/disabilities/bh_brl.php
# * http://acharya.iitm.ac.in/cgi-bin/brcell_disp.pl?sanskrit
# * http://acharya.iitm.ac.in/demos/br_transcription.php
# * http://www.unicode.org/charts/PDF/U0900.pdf
# * http://libbraille.org/translator.php?table=hindi
#   ^ adds halanths at arbitrary places
# * http://rishida.net/scripts/uniview/
# * http://en.wikipedia.org/wiki/Braille_patterns

###################################
# Fun facts about Bharati Braille #
###################################
# * No conjuncts or ligatures — there isn't enough space in the braille charset
# * All scripts are mapped to the same braille characters. As a result,
#   multi-language documents are practically impossible to parse.
# * The selection of vowels and consonants is pretty arbitrary and incomplete.
# * The conversion is quite lossy. Several characters are "compressed" into each
#   other. For example:
#   0906 (आ) and 093E (ा) are represented by 281C (⠜) 
#   0915 (क) and 0958 (क़) are represented by 2805 (⠅)
#   This is kind of lame, but oh well.
# * In unicode, half-forms are denoted by suffixing consonants with a halanth.
#   In bharati braille, half-forms are denoted by prefixing consonants with a 
#   halanth.
# * Vowels that sound the same (or even "similar"!) use the same symbol
# * Matras are denoted by their "full forms", as shown in the comment about
#   lossy conversion above.
# * Unicode braille has 8 dots (⣿). We use the top 6 (⠿), which are the 
#   original 6 braille dots. If you see the lower two dots being used by this
#   convertor or anywhere else, it's wrong!
# * There is little sense in all this. Linguists are now crying.


#################################################
# Devanagari Unicode to Bharati Braille Mapping #
#################################################

# This is used for the "halanth-reversal". See below.
halanth = "⠈"

## Priority characters: Converted in the first pass.
# These are written in unicode as conjuncts, but they have their own Bharati 
# Braille characters. Hence they must be converted *first*; otherwise we'll 
# get an expanded form in the Braille.
braille_to_devanagari_priority = {
    # क्ष = क ् ष
     "⠟": ("क्ष",),
    # ज्ञ = ज ् ञ
     "⠱": ("ज्ञ",),
}

## "Normal" characters: All other characters which are converted directly.
# The exception is the Halanth which needs to be converted from a character 
# suffix to a character prefix during conversion.
# We call this the "halanth-reversal"
braille_to_devanagari = {
## Special characters
     "⠈": ("्",), # Halant
     "⠂": (",",), # Comma (swalp-viraam)
     "⠆": (";",), # Semi-colon (ardh-viraam)
     "⠒": (":",), # Colon (apurn-viraam)
    # TODO: Hyphens and dashes, pg 32
    # "⠂": ("ऽ",), # Avagraha (same as comma, wtf?)
    # ॥ has no mapping, so we stick it in here
     "⠲": ("।", "॥"),
     "⠖": ("!",), # Exclamation point (udgar-chinh)
     "⠦": ("?",), # Question mark (prashn-chinh)
     # TODO: ASCII quotes missing.
      "⠦": ('“',), # Opening double quote (Sadharan avataran chinh)
      "⠴": ('”',), # Closing double quote (Sadharan avataran chinh)
      "⠠⠦": ('‘',), # Opening single quote (Aantariya avataran chinh)
      "⠴⠄": ('’',), # Closing single quote (Aantariya avataran chinh)
      "⠶": ("(", ")"), # Round brackets (Koshthak)
      "⠠⠶": ("[",), # Opening square bracket (Koshthak)
      "⠶⠄": ("]",), # Closing square bracket (Koshthak)
      "⠠⠠⠠": ("…",), # Ellipsis
      "⠔⠔": ("*",), # Asterisk
## Numerals (ASCII and Devanagari)
      "⠼⠁": ("1",  "१"),  # 1
      "⠼⠃": ("2",  "२"),  # 2
      "⠼⠉": ("3",  "३"),  # 3
      "⠼⠙": ("4",  "४"),  # 4
      "⠼⠑": ("5",  "५"),  # 5
      "⠼⠋": ("6",  "६"),  # 6
      "⠼⠛": ("7",  "७"),  # 7
      "⠼⠓": ("8",  "८"),  # 8
      "⠼⠊": ("9",  "९"),  # 9
      "⠼⠚": ("0",  "०"),  # 0
      # TODO: Commas between numbers like 1,500,000 are different (pg 36)
      # TODO: More numbers shit on pg 36
      # TODO: Fractions, pg 37
      # TODO: Decimals, pg 38
## Math symbols
      "⠬": ("+", ), # + (plus sign)
      "⠤": ("−", ), # − (minus sign)
      "⠈⠡": ("×", ), # × (multiplication sign)
      "⠨⠌": ("÷", ), # ÷ (division sign)
      "⠨⠅": ("=", ), # = (equal sign)
      "⠈⠴⠅": ("%", ), # % (percentage sign)
      # TODO: Number symbol when using math signs (pg 39)
## "Vowels"
     "⠠": ("ः",),  # Visarg
     "⠰": ("ं",), # Anusvar
     "⠄": ("ँ",), # Chandrabindu
     "⠁": ("अ",),
     "⠜": ("आ", "ा" ),
     "⠊": ("इ", "ि"),
     "⠔": ("ई", "ी"),
     "⠥": ("उ", "ु"),
     "⠳": ("ऊ", "ू"),
    # ॠ and ॄ have no mapping, so they're lumped here
     "⠐⠗": ("ॠ", "ऋ", "ृ", "ॄ"),
     "⠢": ("ऍ", "ॅ"), # Parichhed
    # ऎ and ॆ have no mapping, so they're lumped here
     "⠑": ("ऎ", "ए", "ॆ", "े",),
     "⠌": ("ऐ", "ै"),
     "⠭": ("ऑ",),
    # ऒ and ॊ have no mapping, so they're lumped here
     "⠕": ("ऒ", "ओ", "ॊ", "ो"),
     "⠪": ("औ", "ौ"),
## "Consonants"
     "⠅": ("क", "क़"),
     "⠨": ("ख", "ख़"),
     "⠛": ("ग", "ग़"),
     "⠣": ("घ",),
     "⠬": ("ङ",),
     "⠉": ("च",),
     "⠡": ("छ",),
    # Yes. This is not a mistake. JA and ZA are the same.
     "⠚": ("ज", "ज़"),
     "⠴": ("झ",),
     "⠒": ("ञ",),
     "⠾": ("ट",),
     "⠺": ("ठ",),
     "⠫": ("ड",),
     "⠿": ("ढ",),
     "⠼": ("ण",),
     "⠞": ("त",),
     "⠹": ("थ",),
     "⠙": ("द",),
     "⠮": ("ध",),
     "⠝": ("न", "ऩ"),
     "⠏": ("प",),
     "⠖": ("फ", "फ़"),
     "⠃": ("ब",),
     "⠘": ("भ",),
     "⠍": ("म",),
     "⠽": ("य", "य़",),
     "⠗": ("र", "ऱ"),
     "⠇": ("ल",),
     "⠸": ("ळ", "ऴ"),
     "⠧": ("व",),
     "⠩": ("श",),
     "⠯": ("ष",),
     "⠎": ("स",),
     "⠓": ("ह",),
 ## Nuktaa stuff
# Nuktaa characters assigned separate symbols
     "⠻": ("ड़",),
     "⠐⠻": ("ढ़",),
}

## Devanagari characters that have no mapping.
# This isn't used anywhere yet. It exists only for documentation.
_without_mapping = [
    # Characters which could be shoved somewhere else, just not sure where:
    ("ऄ", "ॲ", "ऌ", "ॡ", "ॢ", "ॣ", "ॻ", "ॼ", "ॾ", "ॿ", "ॽ", "०", "१", "२", "३",
     "४", "५", "६", "७", "८", "९"),
    # Characters without any mappings which can't be lumped anywhere else:
    ("ऀ", "ऺ", "ऻ", "़", "ॎ", "ॏ", "ॐ", "॑", "॒", "॓", "॔", "ॕ", "ॖ", "ॗ", "॰",
     "ॱ", "ॳ", "ॴ", "ॵ", "ॶ", "ॷ", "ॹ", "ॺ",),
    # Devanagari Extended; definitely no mappings:
    ("꣠", "꣡", "꣢", "꣣", "꣤", "꣥", "꣦", "꣧", "꣨", "꣩", "꣪", "꣫", "꣬", "꣭", "꣮",
     "꣯", "꣰", "꣱", ",ꣲ", "ꣳ", "ꣴ", "ꣵ", "ꣶ", "ꣷ", "꣸", "꣹", "꣺", "ꣻ"),
    # Vedic Extensions; definitely no mappings:
    ("᳐", "᳑", "᳒", "᳓", "᳔", "᳕", "᳖", "᳗", "᳘", "᳙", "᳚", "᳛", "᳜", "᳝", "᳞",
     "᳟", "᳠", "᳡", "᳢", "᳣", "᳤", "᳥", "᳦", "᳧", "᳨", "ᳩ", "ᳪ", "ᳫ", "ᳬ", "᳭",
     "ᳮ", "ᳯ", "ᳰ", "ᳱ", "ᳲ", "ᳳ", "᳴", "ᳵ", "ᳶ"),
]
