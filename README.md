# FreNet

Python API for [WOLF](http://alpage.inria.fr/~sagot/wolf-en.html), a free French WordNet.

## Example

First, load WOLF.

```
>>> from frenetic import *
>>> fwn = FreNetic("/path/to/wolf.xml") # Usually takes a few seconds
```

Retrieve a synset with a given Id.

```
>>> fwn.synset("eng-30-00001740-n") # The 'entity' sysnet
Synset(Id: eng-30-00001740-n, Literals: [u'entit\\xe9'], Def.: concept formulant la cat\xc3\xa9gorisation et l'identique des choses de notre environnement, Usages: [], POS: n)
```

Or retrieve the synsets corresponding to a particular word.

```
>>> synsets = fwn.synsets("chien")
>>> nsynsets = fwn.synsets("chien", pos=NOUN) # Condition on a particular POS tag (ADJ, ADJ_SAT, ADV, NOUN, or VERB)
```
