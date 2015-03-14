# Proj-Database

*Verslagen*: https://docs.google.com/document/d/1ki_IN-m4fuHY4OC_5kxvkX_DA_bjRzRzxaXyVwK_U7U/edit?usp=sharing

*Rapporten*: https://docs.google.com/document/d/1W6QZ2xWvDjR6qZk_nehCUpembAu1taAY9zwFEGXAxBI/edit?usp=sharing

*Presentatie 19/03*: https://docs.google.com/presentation/d/1DEd9rOgII9WZ557w4kw79BITjUtxEz39w26bUIXU8ks/edit?usp=sharing

*Database model*: https://drive.draw.io/#G0BzFlD8HmM6i9OXh6amc2b1NWUlE

## Useful git setting
Zoda we ni constant die merge branch commits krijgen.
```sh
$ git config --global branch.autosetuprebase always
In de repo ook:
$ git config branch.master.rebase true
```

## Tech
###Django
###mySQL
```sh
# Installeer pip3
$ sudo apt-get install python3-pip
# Installeer PyMySQL
$ sudo pip3 install PyMySQL
```
###Zurb foundation styling
###code mirror / ace

## Git voor dummies
Ik dacht ik maak even een klein overzichtje voor iedereen met de handigste git commands, ook voor mezelf da ik ni heel den tijd moet gaan zoeken op het internet voor de juiste commands...
Het idee van die branches is da ge een aantal "feature branches" maakt waarin telkens een apart feature of ding wordt geimplementeerd en als da feature af is wordt die branch gemerged met de master. Het voordeel hiervan is da de master branch in principe altijd werkt en er dus enkel werkende en geteste features bij gemerged mogen worden.

###### Setup
**git init** voor een nieuwe lokale git repository.
**git remote add `naam` `source`** voor een nieuwe remote waarmee ge de online repository aanspreekt.
```
$ git init
Initialised empty Git repository in /home/sten/Documents/TA_Example/.git/
$ git remote add origin https://github.com/Mari3/ProjectT-A.git
```

**NIEUW: git clone 'url'** voor een lokale kopie van de repo.

###### Verkrijgen van de meest recente bestanden
In een nieuwe lokale repo eerst en vooral **git fetch `remote`** om de hele remote repo binnen te halen. Er worden dan nieuwe branches aangemaakt lokaal met de naam remote/branchnaam.
```
$ git fetch origin
...
From https://github.com/Mari3/ProjectT-A
 * [new branch]      MSSC       -> origin/MSSC
 * [new branch]      State_ID   -> origin/State_ID
 * [new branch]      TFA_Sten   -> origin/TFA_Sten
 * [new branch]      master     -> origin/master
```

**NIEUW: git pull** voor fetch + merge (fetch alleen gebruikt ge amper)

Ge kunt dan gaan kijken in een van die branches met **git checkout `naam`**.
```
$ git checkout State_ID 
Branch State_ID set up to track remote branch State_ID from origin.
Switched to a new branch 'State_ID'
```

###### Branches aanmaken
Als ge zelf een nieuwe branch wilt aanmaken is dat meestal om voort te bouwen op een bestaande branch, vaak de master. Dus om een branch te maken en daar ineens alles van een andere in te steken gebruikt ge **git checkout -b `nieuwe_naam` `basis`**. git checkout om een branch te bekijken en de parameter b om die tegelijkertijd aan te maken.
```
$ git checkout -b Test_Feature
Switched to a new branch 'Test_Feature'
```

###### Add/Commit
Ik denk dat iedereen dit principe wel kent, elke file die ge modified moet ge adden aan de huidige situatie en om een snapshot te maken van die situatie doet ge een commit. Commits zijn handig omda ge zo de voortgang van het project kunt volgen aan de hand van de commit messages (lees: schrijf descriptieve commit messages :grinning:) (emojis op Github ftw).

**NIEUW: Lijstje van nuttige emojis die ge vanvoor aan u commit message kunt zetten**

- :art:`:art:` when improving the format/structure of the code
- :racehorse:`:racehorse:` when improving performance
- :non-potable_water:`:non-potable_water:` when plugging memory leaks
- :memo:`:memo:` when writing docs
- :bug:`:bug:` when fixing a bug
- :fire:`:fire:` when removing code or files
- :lock:`:lock:` when dealing with security

Er zijn hierbij 3 belangrijke commands: **git status** om te kijken welke veranderingen nog niet geadd zijn of welke klaar zijn voor een commit en welke files er niet getracked zijn.
Dan **git add `file(s)`** om veranderingen in files toe te voegen. Varianten hierop zijn:
```
$ git add .
```
Voegt alle files in de current directory toe, dit gebruikte best ni omda er vaak veel files zijn die niet in github moeten zitten: .o .d onderandere en bv heel de eclipse project rotzooi :stuck_out_tongue:
```
$ git add -u
```
Dit is een betere variant en voegt alle files toe die veranderd zijn en al getracked waren. Dan moet ge enkel nog git add file gebruiken als ge specifiek nieuwe files toevoegd aan het project

Daarna doet ge best een git status om er zeker van de zijn dat al die files ready zijn om te committen met **git commit**. Als ge git commit zo gebruikt opent de terminal de default text editor, in veel gevallen Vi(m) om de commit message in te schrijven.

Een commit message in Vim scrijven kan nog wel handig zijn om een uitgebreid bericht te schrijven omdat de eerste lijn als short message wordt behandeld en alles na 1 lege lijn als uitgebreide commit message toegevoegd wordt, handig als er wa meer uitleg nodig is bij de commit.

**NIEUW: Gebruik die extra uitleg dan ook als da nuttig is (waarom die change, wa zijn de gevolgen, etc)**

###### Updates pushen
Na een aantal commits hebt ge meestal al een wel een presentabel deel van u feature af en kunt ge het pushen naar github met **git push `remote` `naam`**. Hierbij is `naam` de naam van u branch die ge wilt pushen op de remote branch met dezelfde naam. Dan wordt heel die branch met al zijn commit geschiedenis gepusht naar de remote. Als 'origin' de naam is van u remote kunt ge ook **git push** gebruiken, dan is de remote als default origin en de branch naam de branch waar ge momenteel in zit. 
Ge kunt ook **git push -u `remote`**, en dan wordt de remote branch op `remote` de default branch waarnaar gepusht wordt, dus dan kunt ge de volgende keren gewoon **git push** runnen.
Moest het zijn da ge u branch wilt pushen en nen andere naam geven op de remote kunt ge **git push `remote` `lokale_branch`:`remote branch`** gebruiken.

```
$ git push origin Test_Feature
// is gelijk aan git push als ge in Test_Feature zit
```

**NIEUW: als ge de repo binnen gehaald hebt me git clone is die remote automatisch tracking gemaakt en kunt ge direct git pull/push zonder argumenten**

###### Mergen
Als u feature uiteindelijk klaar is kunt ge het mergen met de master of een andere branch. Dan kunt ge best het volgende doen: Eerst pusht ge u branch nog eens met **git push** om er zeker van te zijn dat de remote kopie up to date is. Dan gaat ge naar de lokale kopie van de branch waarin ge u feature wilt mergen **git checkout `branch`**. Dan doet ge best **git pull `remote`** eerst om er zeker te zijn da de lokale kopie up to date is met de remote kopie. Dan **git pull --no-ff `remote` `branch`** om u branch in deze te mergen. git pull doet eigenlijk een git fetch en git merge in 1. Dus eerst fetcht git `branch` van de remote en dan wordt er een merge gedaan van die fetch in de current branch. De --no-ff staat voor no fast-forward, zo wordt er altijd een merge commit aangemaakt en is het gemakkelijker te volgen wat er is gebeurt met de verschillende branches. En dan ten slotte een **git push** om de lokale branch master te pushen naar de remote branch master.
```
$ git fetch origin
$ git checkout master
$ git pull
$ git pull --no-ff origin Test_Feature
$ git push
```

**NIEUW: Best via github pull request mergen. Zo ziet ge direct of er merge conflicten zijn en kan iedereen nog commentaar geven**

###### NIEUW: Resetten
`git reset args paths`
- args: --hard om alle code te resetten, --soft om enkel de HEAD pointer te verplaatsen zonder code aan te passen.
- paths: HEAD voor de laatste commit, HEAD~k voor de k'de laatste commit. Kan ook een commit hash zijn (`git log` voor een lijst met commits, enkel eerste 7 chars nodig)
```
$ git reset --hard HEAD
Reset code naar laatste commit
$ git reset --hard HEAD~2
Undo 2 commits
```
