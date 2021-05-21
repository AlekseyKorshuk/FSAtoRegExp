========================
FSA to RegExp Translator
========================

Implement an FSA to RegExp Translator. Given an FSA description in the input.txt (see input file format) your program should output the output.txt containing an error description (see validation errors) or a regular expression that corresponds to the given FSA. The regular expression should be built according to a slightly modified version of the Kleene’s algorithm (see Kleene's algorithm).

Input file format
*****************

states=[s1,s2,...]	// s1 , s2, ... ∈ latin letters, words and numbers

alpha=[a1,a2,...]	// a1 , a2, ... ∈ latin letters, words, numbers and character '_’(underscore)

initial=[s]	// s ∈ states

accepting=[s1,s2,...]	// s1, s2 ∈ states

trans=[s1>a>s2,...]	// s1,s2,...∈ states; a ∈ alpha

Validation result | Errors:
***************************

E0: Input file is malformed

E1: A state 's' is not in the set of states

E2: Some states are disjoint

E3: A transition 'a' is not represented in the alphabet

E4: Initial state is not defined

E5: FSA is nondeterministic

Kleene’s Algorithm
******************

.. |ImageLink| image:: /1.png
.. |ImageLink| image:: /2.png

Denote ∅ as {}

Denote Ɛ as eps


Example 1
*********
input.txt

.. code:: text

      states=[on,off]
      alpha=[turn_on,turn_off]    
      initial=[off]
      accepting=[]
      trans=[off>turn_on>off,on>turn_off>on]
 
output.txt

.. code:: text

      Error:
      E2: Some states are disjoint

Example 2
*********

input.txt

.. code:: text

      states=[0,1]
      alpha=[a,b]
      initial=[0]
      accepting=[1]
      trans=[0>a>0,0>b>1,1>a>1,1>b>1]
      
output.txt

.. code:: text

      ((a|eps)(a|eps)*(b)|(b))(({})(a|eps)*(b)|(a|b|eps))*(({})(a|eps)*(b)|(a|b|eps))|((a|eps)(a|eps)*(b)|(b))

Example 3
*********
input.txt

.. code:: text

      states=[on,off]
      alpha=[turn_on,turn_off]
      initial=[off]
      accepting=[]
      trans=[off>turn_on>on,on>turn_off>off]
      
output.txt

.. code:: text

      {}
