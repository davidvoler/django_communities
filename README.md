Django Communities
==================
THIS PACKAGE IS IN DEVELOPMENT STAGE


A single site takes care of multiple communities and relationship between communities. 

* Managing multiple communities in a single site
* Handling community relationship 
* Separating in community permission
* Easily creating new communities without the need to install a new site
* Community admin manages community's  users 


Usage example 1 - Time Bank
---------------------------
Information about time banking can be found here
http://en.wikipedia.org/wiki/Time_banking

We have a site serving 3 time banking communities, A, B and C.
Each user is member of one of the communities and can trade services only with the members of her community. 
For this scenario we could simply have a separate installation for each community.

But if communities A and B have trust relationship with each other so members from A can trade SOME services with members from community B
At the same time community B has relationship with community C

To summarize the community relationship
A -> B
B -> A,C
C -> B  



Usage example 2 - Vacation flat/house exchange
---------------------------
A site for house exchange that is community based people in a single community know and trust each other but unfortunately they 
live in the same city, so exchanging the house for vacation makes little sense, the solution is to create a trust relationship 
with a remote community.
Members from community in Paris and a Community in Rome create a maintain a trust relationship

