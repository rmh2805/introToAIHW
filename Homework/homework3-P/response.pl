/*====================<Facts>====================*/
male(george).
male(spencer).
male(philip).
male(charles).
male(mark).
male(andrew).
male(edward).
male(william).
male(harry).
male(peter).
male(eugine).
male(james).

female(mum).
female(kydd).
female(elizabeth).
female(margaret).
female(diana).
female(anne).
female(sarah).
female(sophie).
female(zara).
female(beatrice).
female(louise).

isSpouse(george,mum).
isSpouse(spencer,kydd).
isSpouse(elizabeth,philip).
isSpouse(diana,charles).
isSpouse(anne,mark).
isSpouse(andrew,sarah).
isSpouse(edward,sophie).

areParents(george,mum,elizabeth).
areParents(george,mum,margaret).
areParents(spencer,kydd,diana).
areParents(elizabeth,philip,charles).
areParents(elizabeth,philip,anne).
areParents(elizabeth,philip,andrew).
areParents(elizabeth,philip,edward).
areParents(diana,charles,william).
areParents(diana,charles,harry).
areParents(anne,mark,peter).
areParents(anne,mark,zara).
areParents(andrew,sarah,beatrice).
areParents(andrew,sarah,eugine).
areParents(edward,sophie,louise).
areParents(edward,sophie,james).

/*====================<Rules>====================*/
spouse(X,Y)     :- isSpouse(X,Y);isSpouse(Y,X).
parents(X,Y,Z)  :- areParents(X,Y,Z);areParents(Y,X,Z).

parent(X,Y) :- parents(X,_,Y).
child(X,Y)  :- parent(Y,X).

grandchild(X,Y) :- child(X,Z),child(Z,Y).
grandparent(X,Y) :- grandchild(Y,X).

greatgrandparent(X,Y) :- parent(X,Z), grandparent(Z,Y).
greatgrandchild(X,Y) :- greatgrandparent(Y,X).

ancestor(X,Y) :- parent(X,Y).
ancestor(X,Y) :- parent(Z,Y),ancestor(X,Z).
descendant(X,Y) :- ancestor(Y,X).

sibling(X,Y) :- child(X,Z), child(Y,Z), X \= Y.
brother(X,Y) :- sibling(X,Y), male(X).
sister(X,Y)  :- sibling(X,Y), female(X).

son(X,Y) :- child(X,Y), male(X).
daughter(X,Y) :- child(X,Y), female(X).

firstCousin(X,Y) :- parent(A,X), parent(P,Y), sibling(A,P).

husband(X,Y) :- spouse(X,Y),male(X).
wife(X,Y) :- spouse(X,Y),female(X).

siblingInLaw(X,Y) :- spouse(X,S),sibling(S,Y).
siblingInLaw(X,Y) :- sibling(X,S),spouse(S,Y).

sisterInLaw(X,Y) :- siblingInLaw(X,Y),female(X).
brotherInLaw(X,Y) :- siblingInLaw(X,Y),male(X).

isAuncle(X,Y) :- sibling(X,S), ancestor(S,Y).
auncle(X,Y) :- isAuncle(X,Y).
auncle(X,Y) :- spouse(X,S), isAuncle(S,Y).

uncle(X,Y) :- auncle(X,Y), male(X).
aunt(X,Y) :- auncle(X,Y), female(X).
