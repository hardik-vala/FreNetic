"""
A very simple API for the WOLF French WordNet: http://alpage.inria.fr/~sagot/wolf-en.html.
"""

import os
import sys

import xml.etree.cElementTree as et

from collections import defaultdict


# POS constants.
ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'


class Literal(object):
    """
    Literal with span and lnote.
    """

    def __init__(self, span, lnote):
        self._span = span
        self._lnote = lnote

    def span(self):
        return self._span

    def lnote(self):
        return self._lnote

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self._span == other._span and self._lnote == other._lnote

        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self._lnote:
            return "%s (%s)" % (self._span, self._lnote)

        return self._span


class Synset(object):
    """
    Synset, complete with Id, list of literals, definition, list of usages, BCS, POS, and list of hypernyms (if any).
    """

    def __init__(self, sid, literals, defn, usages, bcs, pos):
        self._sid = sid
        self._literals = literals
        self._defn = defn
        self._usages = usages
        self._bcs = bcs
        self._pos = pos

        self._hypernyms = None
        self._inst_hypernyms = None

    def sid(self):
        return self._sid

    def literals(self):
        return self._literals

    def defn(self):
        return self._defn

    def usages(self):
        return self._usages

    def bcs(self):
        return self._bcs

    def pos(self):
        return self._pos

    def hypernyms(self):
        return self._hypernyms

    def inst_hypernyms(self):
        return self._inst_hypernyms

    def __eq__(self, other):
        if isinstance(other, Synset):
            return self._sid == other._sid

        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = ("Synset(Id: %s, Literals: %s, Def.: %s, Usages: %s, POS: %s" %
             (self._sid, str(self._literals), self._defn, str(self._usages), self._pos))

        s += (", Hypernyms: %s" % str([h._sid for h in self._hypernyms]) if self._hypernyms else "")
        return s + (", Instance Hypernyms: %s" % str([h._sid for h in self._inst_hypernyms]) if self._inst_hypernyms else "") + ")"


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
    _BCS_TAG_NAME = "BCS"
    _POS_TAG_NAME = "POS"

    # lnote attribute name in .xml dump of WOLF.
    _LNOTE_ATT = "lnote"

    # Signifier of the hypernym relation in .xml dump of WOLF.
    _HYPERNYM_TYPE = "hypernym"
    _INST_HYPERNYM_TYPE = "instance_hypernym"

    # Denotes empty literals in .xml dump of WOLF.
    _EMPTY_LIT = "_EMPTY_"

    def __init__(self, path=None):
        """
        :param path: Path to WOLF .xml dump.
        """
        if path is None:
            path = os.path.join(os.path.dirname(__file__),
                                'data', 'wolf-1.0b4.xml')

        self._synsets = {}
        self._lex_spans = defaultdict(list)

        hypernym_ids, inst_hypernym_ids = {}, {}
        tree = et.parse(path)
        for synset_el in tree.iter(FreNetic._SYNSET_TAG_NAME):
            sid = synset_el.find(FreNetic._ID_TAG_NAME).text.strip()

            literals = []
            for lit_el in synset_el.iter(FreNetic._LIT_TAG_NAME):
                if lit_el.text and lit_el.text.strip() != FreNetic._EMPTY_LIT:
                    span = lit_el.text.strip()
                    lnote = lit_el.get('lnote')
                    literals.append(Literal(span, lnote))

            defn = synset_el.find(FreNetic._DEF_TAG_NAME).text.strip()
            usages = [usage_el.text.strip() for usage_el in synset_el.iter(FreNetic._USAGE_TAG_NAME)]

            bcs_el = synset_el.find(FreNetic._BCS_TAG_NAME)
            bcs = int(bcs_el.text) if bcs_el is not None else None

            pos = synset_el.find(FreNetic._POS_TAG_NAME).text.strip()

            self._synsets[sid] = Synset(sid, literals, defn, usages, bcs, pos)

            for lit in literals:
                self._lex_spans[lit.span()].append(self._synsets[sid])

            hypernym_ids[sid], inst_hypernym_ids[sid] = [], []
            for ilr_el in synset_el.iter(FreNetic._ILR_TAG_NAME):
                if ilr_el.get('type') == FreNetic._HYPERNYM_TYPE:
                    hypernym_ids[sid].append(ilr_el.text.strip())

                if ilr_el.get('type') == FreNetic._INST_HYPERNYM_TYPE:
                    span = ilr_el.text.strip()
                    hypernym_ids[sid].append(span)
                    inst_hypernym_ids[sid].append(span)

        for sid, synset in self._synsets.items():
            synset._hypernyms = [self._synsets[hid] for hid in hypernym_ids[sid]]
            synset._inst_hypernyms = [self._synsets[hid] for hid in inst_hypernym_ids[sid]]

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

    def synsets(self, lex_span, pos=None):
        """
        Returns the synsets corresponding to the given lexical span, returning None if none exist.

        :param lex_span: Lexical span.
        :return: List of corresponding synsets, if they exist, None otherwise.
        """

        if lex_span in self._lex_spans:
            synsets = self._lex_spans[lex_span]
            if pos is not None:
                synsets = [syn for syn in synsets if syn.pos() == pos]
            return synsets
        elif unicode(lex_span) in self._lex_spans:
            synsets = self._lex_spans[unicode(lex_span)]
            if pos is not None:
                synsets = [syn for syn in synsets if syn.pos() == pos]
            return synsets

        return None
