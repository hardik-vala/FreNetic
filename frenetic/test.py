import os
import random

from unittest import TestCase, main

from frenetic import *


class FreNeticTest(TestCase):

    fwn = FreNetic(os.path.join("..", "wolf-1.0b4.xml"))
    synset_ids = fwn.ids()

    random.seed(461328)

    def test_synset_count(self):
        self.assertEqual(117658, self.fwn.count_synsets())

    def test_rand_synset_1(self):
        synset = self.fwn.synset(random.choice(self.synset_ids))

        self.assertEqual("eng-30-06592421-n", synset.sid())
        self.assertListEqual([], synset.literals())
        self.assertEqual("concept album compiling a performer's work or work supporting some worthy cause",
                         synset.defn())
        self.assertListEqual([], synset.usages())
        self.assertEqual(NOUN, synset.pos())

        self.assertListEqual(["eng-30-06592078-n"], [hyp.sid() for hyp in synset.hypernyms()])

    def test_rand_synset_2(self):
        random.choice(self.synset_ids)
        synset = self.fwn.synset(random.choice(self.synset_ids))

        self.assertEqual("eng-30-03651947-n", synset.sid())
        self.assertListEqual([], synset.literals())
        self.assertEqual("(nautical) plumb line for determining depth", synset.defn())
        self.assertListEqual([], synset.usages())
        self.assertEqual(NOUN, synset.pos())

        self.assertListEqual(["eng-30-03969627-n"], [hyp.sid() for hyp in synset.hypernyms()])


if __name__ == '__main__':
    main()
