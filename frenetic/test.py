# -*- coding: utf-8 -*-

import os
import random

from unittest import TestCase, main

from frenetic import *


class FreNeticTest(TestCase):

    fwn = FreNetic(os.path.join("..", "wolf-1.0b4.xml"))
    synset_ids = fwn.ids()

    def test_synset_count(self):
        self.assertEqual(117658, self.fwn.count_synsets())

    def test_rand_synset_1(self):
        random.seed(461328)
        synset = self.fwn.synset(random.choice(self.synset_ids))

        self.assertEqual("eng-30-06592421-n", synset.sid())
        self.assertListEqual([], synset.literals())
        self.assertEqual("concept album compiling a performer's work or work supporting some worthy cause",
                         synset.defn())
        self.assertListEqual([], synset.usages())
        self.assertEqual(NOUN, synset.pos())

        self.assertListEqual(["eng-30-06592078-n"], [hyp.sid() for hyp in synset.hypernyms()])

    def test_rand_synset_2(self):
        random.seed(7317)
        synset = self.fwn.synset(random.choice(self.synset_ids))

        self.assertEqual("eng-30-05351968-n", synset.sid())
        self.assertListEqual(["artère mésentérique inférieure"], synset.literals())
        self.assertEqual("artère amenant du sang oxygéné au tube digestif", synset.defn())
        self.assertListEqual([], synset.usages())
        self.assertEqual(NOUN, synset.pos())

        self.assertListEqual(["eng-30-05351746-n"], [hyp.sid() for hyp in synset.hypernyms()])

    def test_literal(self):
        lit = "chien"
        synsets = self.fwn.synsets(lit)

        self.assertListEqual(["eng-30-02084071-n", "eng-30-02084732-n", "eng-30-02087551-n", "eng-30-02710044-n",
                              "eng-30-03901548-n", "eng-30-10023039-n", "eng-30-10114209-n"],
                             [syn.sid() for syn in synsets])

    def test_literal_with_pos(self):
        lit = "moteur"

        asynsets = self.fwn.synsets(lit, pos=ADJ)
        self.assertListEqual(["eng-30-00324481-a", "eng-30-00334245-a"], [syn.sid() for syn in asynsets])

        nsynsets = self.fwn.synsets(lit, pos=NOUN)
        self.assertListEqual(["eng-30-00572489-n", "eng-30-03287733-n", "eng-30-03789946-n", "eng-30-09359631-n",
                              "eng-30-11417561-n"], [syn.sid() for syn in nsynsets])

        vsynsets = self.fwn.synsets(lit, pos=VERB)
        self.assertListEqual([], [syn.sid() for syn in vsynsets])

if __name__ == '__main__':
    main()
