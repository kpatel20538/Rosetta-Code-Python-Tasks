# Rosetta Code - Python Tasks
Implementations of Tasks from http://rosettacode.org in Python 3.x 

Quoted from the Rosetta Code Homepage:

*"Rosetta Code is a programming chrestomathy site. The idea is to 
present solutions to the same task in as many different languages as 
possible, to demonstrate how languages are similar and different, and 
to aid a person with a grounding in one approach to a problem in 
learning another. Rosetta Code currently has 827 tasks, 204 draft tasks, 
and is aware of 645 languages, though we do not (and cannot) have 
solutions to every task in every language."*

This purpose of this repository is archive my personal contributions 
to Rosetta Code.

## Tasks Lists
Task Descriptions are quoted from their associated task pages

- [x] [Chaos Game][Chaos Game Task]

  *"Play the Chaos Game using the corners of an equilateral triangle as 
the reference points. Add a starting point at random (preferably 
inside the triangle). Then add the next point halfway between the 
starting point and one of the reference points. This reference point 
is chosen at random. After a sufficient number of iterations, the image 
of a Sierpinski Triangle should emerge."*

  [chaos.py](./finished/chaos.py), [chaos_test.py](./finished/chaos_test.py)

- [x] [Pythagoras Tree][Pythagoras Tree Task]

  *"Construct a Pythagoras tree of order 7 using only vectors 
(no rotation or trig functions)."*
  
  [pythagoras.py](./finished/pythagoras.py), [pythagoras_test.py](./finished/pythagoras_test.py)

- [x] [RPN to Infix Conversion][Parsing RPN to Infix Conversion Task]

  *"Create a program that takes an RPN representation of an expression 
formatted as a space separated sequence of tokens and generates the 
equivalent expression in infix notation."*
  
    [rpninfix.py](./finished/rpninfix.py), [rpninfix_test.py](./finished/rpninfix_test.py)

- [x] [Zeckendorf Arithmetic][Zeckendorf Arithmetic Task]

  *"This task is a total immersion zeckendorf task; using decimal 
numbers will attract serious disapprobation.*

  *The task is to implement addition, subtraction, multiplication, and 
division using Zeckendorf number representation. Optionally provide 
decrement, increment and comparitive operation functions."*

  [zeckendorf.py](./finished/zeckendorf.py), [zeckendorf_test.py](./finished/zeckendorf_test.py)

## Executing Tasks
A Dockerfile is provided to help with preparing/testing tasks

The Docker Image is based on [Alpine Linux][1] ( Specifically 
[python:3-alpine][3] from Docker Hub ), and installs [NumPy][3] and 
[Pillow][4] libraries by default

Note that the following docker commands may need to be change to suite 
the user's OS.
### Build
To build the docker image run the following
```bash
$ cd Rosetta-Code-Python-Tasks/
$ docker build -rm -t rosetta-python .
```
Now all tasks are availible for testing/running
### Test
After building, one can test a specific task by running the following
```bash
$ docker run -ti -v {ABSOULTE_PATH_TO_REPO}/logs:/usr/rosetta/logs 
-v {ABSOULTE_PATH_TO_REPO}/out:/usr/rosetta/out -rm rosetta-python 
unittest tests.{TASKNAME}_test
```

### Run
After building, one can run a specific task by running the following
```bash
$ docker run -ti -v {ABSOULTE_PATH_TO_REPO}/logs:/usr/rosetta/logs 
-v {ABSOULTE_PATH_TO_REPO}/out:/usr/rosetta/out -rm rosetta-python 
tasks.{TASKNAME}
```

[1]: https://alpinelinux.org 
[2]: https://hub.docker.com/_/python/
[3]: http://www.numpy.org
[4]: https://python-pillow.org
[Chaos Game Task]: https://rosettacode.org/wiki/Chaos_game
[Pythagoras Tree Task]: https://rosettacode.org/wiki/Pythagoras_tree
[Parsing RPN to Infix Conversion Task]: https://rosettacode.org/wiki/Parsing/RPN_to_infix_conversion
[Zeckendorf Arithmetic Task]: https://rosettacode.org/wiki/Zeckendorf_arithmetic 
