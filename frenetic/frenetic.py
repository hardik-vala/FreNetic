"""
A very simple API for the WOLF French WordNet: http://alpage.inria.fr/~sagot/wolf-en.html.
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import xml.etree.cElementTree as et

from collections import defaultdict


# POS constants.
ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'


class Synset(object):
    """
    Synset, complete with Id, list of literals, definition, list of usages, POS, and list of hypernyms (if any).
    """

    def __init__(self, sid, literals, defn, usages, pos):
        self._sid = sid
        self._literals = literals
        self._defn = defn
        self._usages = usages
        self._pos = pos

        self._hypernyms = None

    def sid(self):
        return self._sid

    def literals(self):
        return self._literals

    def defn(self):
        return self._defn

    def usages(self):
        return self._usages

    def pos(self):
        return self._pos

    def hypernyms(self):
        return self._hypernyms

    def __eq__(self, other):
        if isinstance(other, Synset):
            return self._sid == other._sid

        return False

    def __str__(self):
        s = ("Synset(Id: %s, Literals: %s, Def.: %s, Usages: %s, POS: %s" %
             (self._sid, str(self._literals), self._defn, str(self._usages), self._pos))

        return s + (", Hypernyms: %s" % str([h._sid for h in self._hypernyms]) if self._hypernyms else "") + ")"


class FreNetic(object):
    """
    French WordNet, i.e. WOLF, container.
    """

    # Tag names in .xml dump of WOLF.
    _SYNSET_TAG_NAME = "SYNSET"
    _ILR_TAG_NAME = "ILR"
    _ID_TAG_NAME = "ID"
    _LIT_TAG_NAME = "LITERAL"
    _DEF_TAG_NAME = "DEF"
    _USAGE_TAG_NAME = "USAGE"
    _POS_TAG_NAME = "POS"

    # Signifier of the hypernyms relation.
    _HYPERNYM_TYPE = "hypernym"

    # Denotes empty literals.
    _EMPTY_LIT = "_EMPTY_"

    def __init__(self, path):
        """
        :param path: Path to WOLF .xml dump.
        """

        self._synsets = {}
        self._literals = defaultdict(list)

        hypernym_ids = {}
        tree = et.parse(path)
        for synset_el in tree.iter(FreNetic._SYNSET_TAG_NAME):
            sid = synset_el.find(FreNetic._ID_TAG_NAME).text

            literals = [lit_el.text for lit_el in synset_el.iter(FreNetic._LIT_TAG_NAME)
                        if lit_el.text != FreNetic._EMPTY_LIT]

            defn = synset_el.find(FreNetic._DEF_TAG_NAME).text
            usages = [usage_el.text for usage_el in synset_el.iter(FreNetic._USAGE_TAG_NAME)]
            pos = synset_el.find(FreNetic._POS_TAG_NAME).text

            self._synsets[sid] = Synset(sid, literals, defn, usages, pos)

            for lit in literals:
                self._literals[lit].append(self._synsets[sid])

            hypernym_ids[sid] = [ilr_el.text for ilr_el in synset_el.iter(FreNetic._ILR_TAG_NAME)
                                 if ilr_el.get('type') == FreNetic._HYPERNYM_TYPE]

        for sid, synset in self._synsets.iteritems():
            synset._hypernyms = [self._synsets[hid] for hid in hypernym_ids[sid]]

    def ids(self):
        """
        Returns all synset Id's.

        :return: List of all synset Id's.
        """

        return self._synsets.keys()

    def count_synsets(self):
        """
        Returns the # of synsets.

        :return: # of sysnets.
        """

        return len(self._synsets)

    def synset(self, sid):
        """
        Returns the synset corresponding to the given Id, returning None if it doesn't exist.

        :param sid: Synset Id.
        :return: Corresponding synset if it exists, None otherwise.
        """

        if sid in self._synsets:
            return self._synsets[sid]

        return None

    def synsets(self, lit, pos=None):
        """
        Returns the synsets corresponding to the given literal, returning None if none exist.

        :param lit: Literal.
        :param pos: Optional POS tag to filter final synsets.
        :return: List of corresponding synsets, if they exist, None otherwise.
        """

        if lit in self._literals:
            synsets = self._literals[lit]
            if pos:
                synsets = [syn for syn in synsets if syn.pos() == pos]
            return synsets

        return None
