/*male*/
male(raymond).
male(scott).
male(ben).
male(drew).
male(evan).
male(newbie).
male(dash).

male(matt).
male(gary).
male(jimmy).
male(josh).
male(johnny).
male(ed).
male(henry).

male(larry).
male(dave).
male(paul).
male(john).
male(richard).
male(bob).

male(bumpa).
male(pappi).
male(ray).

/*Female*/
female(mary).
female(maddy).

female(emily).
female(laura).
female(rachel).
female(edsWifeIForgot).
female(sandy).

female(joyce).
female(shiela).
female(bean).
female(debby).
female(dianne).
female(jeanne).

female(meema).
female(nanna).
female(barbra).

/*spouses*/
isSpouse(matt,emily).
isSpouse(laura,gary).
isSpouse(jimmy,rachel).
isSpouse(ed,edsWifeIForgot).
isSpouse(sandy,henry).

isSpouse(paul,joyce).
isSpouse(larry, shiela).
isSpouse(dave,debby).
isSpouse(dianne,richard).
isSpouse(jeanne,bob).

isSpouse(meema,bumpa).
isSpouse(nanna,pappi).
isSpouse(ray,barbra).

/*Parents*/
areParents(matt,emily,raymond).
areParents(matt,emily,scott).
areParents(laura,gary,ben).
areParents(laura,gary,mary).
areParents(jimmy,rachel,evan).
areParents(jimmy,rachel,drew).
areParents(ed,edsWifeIForgot,newbie).
areParents(sandy,henry,maddy).
areParents(sandy,henry,dash).

areParents(joyce,larry,emily).
areParents(joyce,larry,laura).
areParents(joyce,larry,jimmy).
areParents(dave,debby,josh).
areParents(dianne,richard,johnny).
areParents(dianne,richard,ed).
areParents(jeanne,bob,sandy).
areParents(jeanne,bob,matt).

areParents(meema,bumpa,larry).
areParents(meema,bumpa,bean).
areParents(meema,bumpa,dave).
areParents(nanna,pappi,john).
areParents(nanna,pappi,joyce).
areParents(nanna,pappi,dianne).
areParents(ray,barbra,jeanne).
