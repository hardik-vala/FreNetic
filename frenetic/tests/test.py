# -*- coding: utf-8 -*-

import os
import random

from unittest import TestCase, main

from frenetic import *


class FreNeticTest(TestCase):

    fwn = FreNetic(os.path.join("frenetic", "data", "wolf-1.0b4.xml"))
    synset_ids = fwn.ids()

    entity_synset = fwn.synset("eng-30-00001740-n")

    def test_synset_count(self):
        self.assertEqual(117658, self.fwn.count_synsets())

    def test_rand_synset_1(self):
        random.seed(461328)
        synset = self.fwn.synset(random.choice(list(self.synset_ids)))

        self.assertEqual("eng-30-06592421-n", synset.sid())
        self.assertListEqual([], synset.literals())
        self.assertEqual("concept album compiling a performer's work or work supporting some worthy cause",
                         synset.defn())
        self.assertListEqual([], synset.usages())
        self.assertIsNone(synset.bcs())
        self.assertEqual(NOUN, synset.pos())

        self.assertListEqual(["eng-30-06592078-n"], [hyp.sid() for hyp in synset.hypernyms()])
        self.assertListEqual([], [hyp.sid() for hyp in synset.inst_hypernyms()])

    def test_rand_synset_2(self):
        random.seed(7317)
        synset = self.fwn.synset(random.choice(list(self.synset_ids)))

        self.assertEqual("eng-30-05351968-n", synset.sid())
        lit = Literal("artère mésentérique inférieure", "0/1:enwikipedia;gwa2012(0.84520285155182772741)")
        self.assertListEqual([lit], synset.literals())
        self.assertEqual("artère amenant du sang oxygéné au tube digestif", synset.defn())
        self.assertListEqual([], synset.usages())
        self.assertIsNone(synset.bcs())
        self.assertEqual(NOUN, synset.pos())

        self.assertListEqual(["eng-30-05351746-n"], [hyp.sid() for hyp in synset.hypernyms()])
        self.assertListEqual([], [hyp.sid() for hyp in synset.inst_hypernyms()])

    def test_rand_synset_3(self):
        sid = "eng-30-00001740-a"
        synset = self.fwn.synset(sid)

        self.assertEqual("eng-30-00001740-a", synset.sid())
        lit = Literal("comptable", "2/2:fr.csbgen,fr.csen")
        self.assertListEqual([lit], synset.literals())
        defn = "(usually followed by `to') having the necessary means or skill or know-how or authority to do something"
        self.assertEqual(defn, synset.defn())
        self.assertListEqual(["able to swim", "she was able to program her computer",
                              "we were at last able to buy a car", "able to get a grant for the project"],
                             synset.usages())
        self.assertEqual(3, synset.bcs())
        self.assertEqual(ADJ, synset.pos())

        self.assertListEqual([], [hyp.sid() for hyp in synset.hypernyms()])
        self.assertListEqual([], [hyp.sid() for hyp in synset.inst_hypernyms()])

    def test_rand_synset_4(self):
        # Soleil.
        sid = "eng-30-09450163-n"
        synset = self.fwn.synset(sid)

        self.assertEqual("eng-30-09450163-n", synset.sid())
        lit = Literal("soleil", "gwa2012(0.35996127512235881474);lrec12mllexwn(2.490)")
        self.assertListEqual([lit], synset.literals())
        defn = "the star that is the source of light and heat for the planets in the solar system"
        self.assertEqual(defn, synset.defn())
        self.assertListEqual(["the sun contains 99.85% of the mass in the solar system",
                              "the Earth revolves around the Sun"],
                             synset.usages())
        self.assertIsNone(synset.bcs())
        self.assertEqual(NOUN, synset.pos())

        self.assertListEqual(["eng-30-09444100-n"], [hyp.sid() for hyp in synset.hypernyms()])
        self.assertListEqual(["eng-30-09444100-n"], [hyp.sid() for hyp in synset.inst_hypernyms()])

    def test_lex_span(self):
        lex_span = "chien"
        synsets = self.fwn.synsets(lex_span)

        self.assertListEqual(["eng-30-02084071-n", "eng-30-02084732-n", "eng-30-02087551-n", "eng-30-02710044-n",
                              "eng-30-03901548-n", "eng-30-10023039-n", "eng-30-10114209-n"],
                             [syn.sid() for syn in synsets])

    def test_lex_span_with_pos(self):
        lex_span = "moteur"

        asynsets = self.fwn.synsets(lex_span, pos=ADJ)
        self.assertListEqual(["eng-30-00324481-a", "eng-30-00334245-a"], [syn.sid() for syn in asynsets])

        nsynsets = self.fwn.synsets(lex_span, pos=NOUN)
        self.assertListEqual(["eng-30-00572489-n", "eng-30-03287733-n", "eng-30-03789946-n", "eng-30-09359631-n",
                              "eng-30-11417561-n"], [syn.sid() for syn in nsynsets])

        vsynsets = self.fwn.synsets(lex_span, pos=VERB)
        self.assertListEqual([], [syn.sid() for syn in vsynsets])

    def test_non_ascii_lex_span(self):
        lex_span = "mère"
        synsets = self.fwn.synsets(lex_span)

        self.assertListEqual(["eng-30-01323493-n", "eng-30-10332385-n", "eng-30-10332861-n", "eng-30-10332953-n"],
                             [syn.sid() for syn in synsets])

    def get_hypernym_path_to_entity(self, synset):
        def get_hypernym_path_to_entity_helper(synset, hypernyms):
            for hypernym in synset.hypernyms():
                if hypernym != self.entity_synset:
                    hypernyms.append(hypernym)
                    get_hypernym_path_to_entity_helper(hypernym, hypernyms)

        hypernyms = [synset]
        get_hypernym_path_to_entity_helper(synset, hypernyms)
        return hypernyms

    def test_hypernym_path_to_entity(self):
        # A synset of 'soleil'.
        synset = self.fwn.synset("eng-30-09450163-n")

        self.assertListEqual(["eng-30-09450163-n", "eng-30-09444100-n", "eng-30-09239740-n", "eng-30-00019128-n",
                              "eng-30-00003553-n", "eng-30-00002684-n", "eng-30-00001930-n"],
                              [syn.sid() for syn in self.get_hypernym_path_to_entity(synset)])


if __name__ == '__main__':
    main()
