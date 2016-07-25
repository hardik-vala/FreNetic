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


if __name__ == '__main__':
    main()
