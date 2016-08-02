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
Synset(Id: eng-30-00001740-n, Literals: [entité (96/4:fr.csen,fr.rocsen,fr.roen,enwikipedia;gwa2012(0.86013904790866246852);lrec12mllexwn(1.548);ManVal2012OK)], Def.: concept formulant la catégorisation et l'identique des choses de notre environnement, Usages: [], POS: n)
```

Or retrieve the synsets corresponding to a particular word.

```
>>> synsets = fwn.synsets("chien")
>>> nsynsets = fwn.synsets("chien", pos=NOUN) # Condition on a particular POS tag (ADJ, ADJ_SAT, ADV, NOUN, or VERB)
```

Given a synset,

```
synset = fwn.synset("eng-30-00001740-n")
```

you can do the following,

```
>>> synset.sid() #Id
'eng-30-00001740-n'
>>> synset.literals() # Literals
[entité (96/4:fr.csen,fr.rocsen,fr.roen,enwikipedia;gwa2012(0.86013904790866246852);lrec12mllexwn(1.548);ManVal2012OK)]
>>> synset.defn() # Definition
u"concept formulant la cat\xe9gorisation et l'identique des choses de notre environnement"
>>> synset.usages() # Usages
[]
>>> synset.bcs()
2
>>> synset.pos() # POS tag
'n'
>>> synset.hypernyms() # List of it's direct hypernyms
[]
```

## Resources

* [WOLF's official page on Benoît Sagot's homepage](http://alpage.inria.fr/~sagot/wolf-en.html)
* [Open Multilingual Wordnet](http://compling.hss.ntu.edu.sg/omw/)
