> 📝 Ce fichier `README.md` est une copie du dépôt original [ProjetPythonM2_2025](https://github.com/JuvignyEnsta/ProjetPythonM2_2025), qui décrit le projet à réaliser.

# Le jeu de la vie et sa généralisation

##  Requis pour le projet

Afin que le projet se déroule dans de bonnes conditions, il faudra s'assurer que sur l'ordinateur sur lequel vous travaillez, vous ayez :

- `python 3` : pas de sous-version minimale requise 
- `numpy`    : Idem, pas de version spécifique requise
- `scipy`    : Idem
- `pygame`   : Version majeure 2 requise, mais pas de sous-version minimale requise

##  Avant de commencer

Ce projet est très largement inspiré d'une vidéo de David Louapre (Science étonnante) : "LENIA : Une nouvelle forme de vie mathématique !" disponible sur Youtube et des articles suivants :

- Chan, B.W.C (2018) : Lenia-Biology of artificial life. arXiv preprint 
- Plantec E., Hamon G., Etcheverry M. Oudeyer, P.Y., Moulin-Frier C. and Chan, B.W.C (2022) : Flow Lenia Mass convertion for the study of virtual creatures in continuous cellular automata, arXiv preprint

On peut trouver un code sur jupyter écrit par David Louapre à partir de sa chaîne Youtube, mais il est vivement conseillé de programmer par soi-même et surtout de bien comprendre les concepts qui seront introduits dans ce projet ! De plus, on verra à la fin du projet qu'une erreur s'est glissée dans l'analyse de David Louapre et on obtiendra par cette analyse un résultat bien plus intéressant !

## Présentation du jeu de la vie

Le jeu de la vie est un **automate cellulaire** inventé en 1970 par le mathématicien J.H Conway (1937-2020).
Le but de J.H. Conway avec ce jeu était de démontrer qu'à partir de règles très simples, il était possible d'engendrer de la complexité. On démontra plus tard que le jeu de la vie est également une machine de Turing, c'est à dire qu'il est
théoriquement possible de "programmer" ce jeu pour faire fonctionner n'importe quel algorithme fonctionnant avec un ordinateur
classique. Et de fait, des logiciels comme Golly (installable sous Ubuntu ou Android par le gestionnaire de paquet adéquat ou sinon téléchargeable sur internet (<https://sourceforge.net/projects/golly>)) proposent des états initiaux pour la grille permettant d'effectuer des calculs et de les afficher sur la représentation de la grille ou encore qui permet de simuler le jeu de la vie 
lui même.

Le jeu de la vie est représentée par une grille cartésienne en deux dimensions infinie dont chaque "case" représente
une cellule qui ne peut prendre que deux valeurs : 0 (morte) ou 1 (vivante). C'est donc un *automate cellulaire* à état fini.
Dans les faits, on se limitera à une grille cartésienne finie (la mémoire de l'ordinateur étant fini).

Le principe du jeu de la vie est le suivant :

- On initialise la grille cartésienne avec des cellules mortes (0) ou vivantes (1)
- On effectue ensuite des itérations (qu'on peut voir comme une avance en temps discrète) en appliquant les règles suivantes à chaque itération :
  - Une cellule vivante avec moins de deux cellules voisines vivantes meurt ( sous-population )
  - Une cellule vivante avec deux ou trois cellules voisines vivantes reste vivante
  - Une cellule vivante avec plus de trois cellules voisines vivantes meurt ( sur-population )
  - Une cellule morte avec exactement trois cellules voisines vivantes devient vivante ( reproduction )
- Les itérations ne s'arrêteront qu'à la demande de l'utilisateur

Dans le cadre du projet, on considérera que les grilles finies utilisées définissent un "tore" dans chaque direction, c'est à dire qu'une cellule la plus en haut a parmi ses voisines la cellule la plus en bas dans sa colonne  et qu'une cellule la plus à gauche aura parmi ses voisines la cellule la plus à droite sur la même ligne de la grille cartésienne.

Un programme "naïf" est donné avec ce projet :`basic_scalar_life_game.py`.

## Travaux à effectuer pour ce projet

Pour chaque étape de ce projet, on conservera le fichier python répondant à cette étape.

### 1. Comprendre, exécuter et analyser le code naïf

Dans un premier temps, nous allons nous contenter de comprendre et de s'assurer que le programme naïf s'exécute correctement sur votre machine.

Lors de l'exécution, mesurez le temps pris pour chaque itération du jeu de la vie, en particulier avec le motif initial `glider_gun`. Pouvez-vous expliquer le temps mesurer ?

### 2. Première optimisation du jeu de la vie

- Vectoriser le calcul du nombre de voisin par cellule en
  utilisant l'instruction `sum` de `python 3` et la fonction `roll` de numpy
- A partir du tableau donnant le nombre de voisins, mettez à jour à l'aide d'une expression vectorielle les cellules de l'automate.
- Observer le temps pris pour calculer chaque itération sur le motif initial `glider_gun`. Calculer le gain obtenu par rapport à la version naïve.

### 3. Seconde optimisation du jeu de la vie en vue d'une généralisation

Nous allons maintenant nous intéresser à une autre optimisation possible afin de pouvoir généraliser le jeu de la vie. L'idée, assez naturelle, est de compter le nombre de voisins pour une cellule à l'aide d'une fonction de convolution discrète :

Soit $G$ un grille cartésienne de dimension $H\times W$ dont chaque cellule, notée $g_{ij}$, se trouvant sur la ligne $i$ et la colonne $j$ peut prendre les valeurs $1$ si vivante ou $0$ si morte. Soit $\mathcal{C}$ une convolution discrète représentée par une matrice de dimension $2.N_{i}+1\times 2.N_{j}+1$ dont les cœfficients réels sont notés $c_{ij}$ avec $-N_{i}< i < +N_{i}$ et $-N_{j} < j < +N_{j}$.

L'opération de convolution discrète centrée sur une cellule $g_{ij}$ est définie comme :

$$
s_{ij} = \sum_{i=-N_{i}+1}^{N_{i}-1}\sum_{j=-N_{j}+1}^{+N_{j}-1} c_{ij}.g_{ij}
$$

En choisissant

$$
C = \left(
  \begin{array}{ccc}
  1 & 1 & 1 \\
  1 & 0 & 1 \\
  1 & 1 & 1
  \end{array}
\right)
$$

on voit facilement que cette convolution revient à calculer le nombre de cellules voisines vivantes autour d'une cellule $g_{ij}$.

En utilisant la fonction `convolve2d` proposée dans le sous-module `signal` de `scipy`, écrire un jeu de la vie optimisé.

Regarder le temps de calcul pour chaque nouvelle génération, et comparer avec la solution précédente.

Cette version va nous permettre de pouvoir établir de nouvelles règles pour le jeu de la vie en prenant en compte des degrès de voisinages plus grands que le simple voisinage immédiat pour une cellule.

### 4. Un petit pas vers Lenia

L'idée ici est toujours de simuler le jeu de la vie, mais on va essayer de prendre un point de vue continue pour le calcul de la prochaine génération, et non discrète comme dans l'étape précédente.

Nous allons pour cela créer une fonction continue qui prendra en entrée le nombre de cellules vivantes (voisinage d'une cellule donnée) et rendra une valeur dans l'intervalle $[-1;1]$.

On va définir cette fonction dans un premier temps comme une fonction $h$ continue linéaire par morceau qui prendra les valeurs suivantes ($x$ ici étant le nombre de voisins pour une cellule donnée):

$$
\begin{array}{llcl}
h : & \mathbb{Z} &  \longrightarrow & [-1;1] \\
    & \textrm{tel que} & & \\
h(x) = -1 & \textrm{pour} & x\leq 1 \\
h(x) = 0  & \textrm{pour} & x = 2 \\
h(x) = 1  & \textrm{pour} & x = 3 \\
h(x) = -1 & \textrm{pour} & x \geq 4
\end{array}
$$

On rajoutera cette valeur à la valeur de la cellule pour laquelle $x$ a été évalué dont la valeur sera ramenée à 0 ou 1 à l'aide d'un
`max` et un `min` ( qu'on simplifiera en utilisant la fonction `clip` proposée par `numpy`).

A l'aide de quelques exemples, assurez-vous qu'on retrouve bien les règles du jeu initial !

Mettez en œuvre cette modification et mesurez le temps pris pour le calcul.

### 5. Lenia, version naïve

Nous allons changer et généraliser plusieurs choses par rapport au jeu de la vie :

- L'espace est considéré comme continu, mais discrétisé avec un certain pas d'espace par une grille cartésienne. Pour plus de commodité, on va définir la métrique euclidienne en fonction du nombre de pixels $r$ dans la direction $Ox$ (ou $Oy$) nécessaire pour représenter une distance unité.
- Un élément carré $C_{i,j}$  de l'espace discrétisé sera appelé **élément** du maillage cartésien.
- Le temps est également considéré comme continue et discrétisé avec un pas de temps $dt$
- Au centre de chaque élément du maillage d'espace, on associé une valeur $V_{i,j}$ scalaire continue comprise entre zéro et un qu'on nommera **vitalité** dont la valeur vaut zéro si aucune "cellule" vivante n'occupe une partie de cet élément, un si une cellule bien vivante occupe complètement cet élément, et une valeur intermédiaire si la cellule occupe une partie de cet élément.
- On définit comme **énergie** $E_{i,j}$ le résultat d'une convolution prenant en considération un élément du maillage et calculant en fonction de la vitalité de cet élément et des éléments proches (dont la distance est inférieure à un).
- On va définir une fonction d'**accroissement** $G$ qui en fonction de l'énergie calculé pour un élément $C_{i,j}$ et ses voisins calcule la nouvelle vitalité $V_{i,j}$ de $C_{i,j}$ pour le pas de temps suivant par la formule $V_{i,j} \leftarrow V_{i,j} + dt.G(i,j)$

Dans cette partie (et les suivantes), on va choisir :

- Pour convolution, la discrétisation d'une fonction gaussienne dépendant de la distance $d$ (d'une cellule aux autres cellules) :

$$
  g_{\mu,\sigma}(d) = e^{-\frac{1}{2}\left(\frac{d-\mu}{\sigma}\right)^{2}}
$$

  Afin que l'étendue de la convolution ne soit pas "infinie", on coupera la convolution dès que la distance est supérieur à un (pas d'interaction entre deux cellules si la distance est supérieure à un)

- Pour fonction d'accroissement $G$ un filtre gaussien centré en zéro avec pour paramètre par défaut $\mu=0.15$ et $\sigma=0.015$ :

$$
  g^{c}_{\mu,\sigma}(x) = -1 + 2.e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^{2}}
$$

Dans un premier temps, pour valeurs initiales pour la vitalité, on se contentera de prendre une fonction gaussienne centrée sur la grille avec une valeur de $r=36$ puis considéré pour le reste de la simulation une valeur de $r=13$.

Dans un second temps, nous allons voir une créature curieuse proche de la méduse : l'`orbium` :

```python
N = 256
M = int(np.ceil((16*N)/9))

orbium = np.array([[0,0,0,0,0,0,0.1,0.14,0.1,0,0,0.03,0.03,0,0,0.3,0,0,0,0], [0,0,0,0,0,0.08,0.24,0.3,0.3,0.18,0.14,0.15,0.16,0.15,0.09,0.2,0,0,0,0], [0,0,0,0,0,0.15,0.34,0.44,0.46,0.38,0.18,0.14,0.11,0.13,0.19,0.18,0.45,0,0,0], [0,0,0,0,0.06,0.13,0.39,0.5,0.5,0.37,0.06,0,0,0,0.02,0.16,0.68,0,0,0], [0,0,0,0.11,0.17,0.17,0.33,0.4,0.38,0.28,0.14,0,0,0,0,0,0.18,0.42,0,0], [0,0,0.09,0.18,0.13,0.06,0.08,0.26,0.32,0.32,0.27,0,0,0,0,0,0,0.82,0,0], [0.27,0,0.16,0.12,0,0,0,0.25,0.38,0.44,0.45,0.34,0,0,0,0,0,0.22,0.17,0], [0,0.07,0.2,0.02,0,0,0,0.31,0.48,0.57,0.6,0.57,0,0,0,0,0,0,0.49,0], [0,0.59,0.19,0,0,0,0,0.2,0.57,0.69,0.76,0.76,0.49,0,0,0,0,0,0.36,0], [0,0.58,0.19,0,0,0,0,0,0.67,0.83,0.9,0.92,0.87,0.12,0,0,0,0,0.22,0.07], [0,0,0.46,0,0,0,0,0,0.7,0.93,1,1,1,0.61,0,0,0,0,0.18,0.11], [0,0,0.82,0,0,0,0,0,0.47,1,1,0.98,1,0.96,0.27,0,0,0,0.19,0.1], [0,0,0.46,0,0,0,0,0,0.25,1,1,0.84,0.92,0.97,0.54,0.14,0.04,0.1,0.21,0.05], [0,0,0,0.4,0,0,0,0,0.09,0.8,1,0.82,0.8,0.85,0.63,0.31,0.18,0.19,0.2,0.01], [0,0,0,0.36,0.1,0,0,0,0.05,0.54,0.86,0.79,0.74,0.72,0.6,0.39,0.28,0.24,0.13,0], [0,0,0,0.01,0.3,0.07,0,0,0.08,0.36,0.64,0.7,0.64,0.6,0.51,0.39,0.29,0.19,0.04,0], [0,0,0,0,0.1,0.24,0.14,0.1,0.15,0.29,0.45,0.53,0.52,0.46,0.4,0.31,0.21,0.08,0,0], [0,0,0,0,0,0.08,0.21,0.21,0.22,0.29,0.36,0.39,0.37,0.33,0.26,0.18,0.09,0,0,0], [0,0,0,0,0,0,0.03,0.13,0.19,0.22,0.24,0.24,0.23,0.18,0.13,0.05,0,0,0,0], [0,0,0,0,0,0,0,0,0.02,0.06,0.08,0.09,0.07,0.05,0.01,0,0,0,0,0]])
cells = np.zeros((N,M))
pos_x = M//6
pos_y = N//6
cells[pos_x:(pos_x + orbium.shape[1]), pos_y:(pos_y + orbium.shape[0])] = orbium.T
```

en utilisant les mêmes paramètres dans la simulation.

Notez encore une fois le temps de calcul pour chaque itération. Expliquez le temps de calcul pour chaque itération trouvé.

### 6. Accélération de Lenia

Si on regarde le temps pris à l'intérieur du calcul de chaque itération, on trouvera que le temps pris par la convolution est près de 1000 fois plus long que le temps pris par la fonction d'accroissement ! Il est donc clair que nous devons nous concentré en priorité sur un moyen d'accélérer notre simulation de Lenia !

Le moyen le plus naturel et le plus efficace est de passer par une transformation de fourier rapide (complexité $\log_{2}(N)$) de notre convolution en utilisant un théorème qui nous dit que si les deux fonctions convolées sont $L_{1}$ (ce qui est notre cas ici), alors la transformée de fourier de la convolution est le produit des transformées de fourier des deux fonctions :

$$
\textrm{Si}\,\, f,g\in L_{1}(\Omega),\,\,\textrm{alors}\,\,T_{f}(f\star g) = T_{f}(f).T_{f}(g)
$$

En utilisant cette transformation, on calculera l'énergie sur chaque élément du maillage en utilisant la transformation de fourier inverse.

Pour programmer cela, on utilisera la transformée de fourier en 2D `fft2` proposée dans le sous-module `fft` de numpy. Afin de centrer la transformée de fourier pour la convolution, on utilisera `fft.fftshift` qui permet de centrer les fréquences autour de zéro.

On testera dans un premier temps l'accélération avec l'`orbium` vu dans la section précédente.

### 7. Utilisation d'un noyau multi-anneaux

Afin de trouver des formes plus complexes, nous allons maintenant prendre un noyau de convolution plus complexe qui prendra la forme d'une somme de plusieurs gaussiennes ayant chacun un support différent (où la fonction est non nulle) en forme d'anneau :

- La première gaussienne sera définie comme :

$$
\begin{cases}
g_{1}(r) & = & 0,5.e^{-\frac{1}{2}\left(\frac{r-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[0;1\right[ \\
g_{1}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

- La deuxième gaussienne sera définie comme :

$$
\begin{cases}
g_{2}(r) & = & e^{-\frac{1}{2}\left(\frac{(r\mod 1)-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[ +1; +2\right[ \\
g_{2}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

- Et enfin une troisième gaussienne définie comme : 

$$
\begin{cases}
g_{3}(r) & = & 0,667.e^{-\frac{1}{2}\left(\frac{(r\mod 1)-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[ +2; +3\right[ \\
g_{3}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

Notons que la première gausienne prenant ses valeurs dans $[0;0.5]$ fournira une énergie négative, donc à baisser la vitalité des cellules (rappelons que pour calculer le taux de croissance (l'énergie fournie), on multiplie la valeur calculée par la convolution par deux puis on retrance un) tandis que la troisième gaussienne aura uniquement cette tendance (statistiquement deux fois sur trois) à fournir une énergie négative (permettant de nettoyer devant un front de cellule remplie de vitalité). Quant à la seconde gaussienne, on retrouve la gaussienne traditionnelle permettant d'être proche d'un jeu de la vie pour le comportement.

On testera ce nouveau noyau avec le pattern initial suivant appelé "*hydrogeminium*" :

```python
N = 256
M = int(np.ceil((16*N)/9))

hydrogeminium = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.02,0.03,0.04,0.04,0.04,0.03,0.02,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0.1,0.16,0.2,0.23,0.25,0.24,0.21,0.18,0.14,0.1,0.07,0.03,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.09,0.2,0.33,0.44,0.52,0.56,0.58,0.55,0.51,0.44,0.37,0.3,0.23,0.16,0.08,0.01,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13,0.29,0.45,0.6,0.75,0.85,0.9,0.91,0.88,0.82,0.74,0.64,0.55,0.46,0.36,0.25,0.12,0.03,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14,0.38,0.6,0.78,0.93,1.0,1.0,1.0,1.0,1.0,1.0,0.99,0.89,0.78,0.67,0.56,0.44,0.3,0.15,0.04,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08,0.39,0.74,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.98,0.85,0.74,0.62,0.47,0.3,0.14,0.03,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.32,0.76,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.88,0.75,0.61,0.45,0.27,0.11,0.01,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.35,0.83,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.88,0.73,0.57,0.38,0.19,0.05,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.99,1.0,1.0,1.0,1.0,0.99,1.0,1.0,1.0,1.0,1.0,1.0,0.85,0.67,0.47,0.27,0.11,0.01], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.55,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.93,0.83,0.79,0.84,0.88,0.89,0.9,0.93,0.98,1.0,1.0,1.0,1.0,0.98,0.79,0.57,0.34,0.15,0.03], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.47,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.9,0.72,0.54,0.44,0.48,0.6,0.7,0.76,0.82,0.91,0.99,1.0,1.0,1.0,1.0,0.91,0.67,0.41,0.19,0.05], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.27,0.99,1.0,1.0,1.0,1.0,0.9,0.71,0.65,0.55,0.38,0.2,0.14,0.21,0.36,0.52,0.64,0.73,0.84,0.95,1.0,1.0,1.0,1.0,1.0,0.78,0.49,0.24,0.07], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14,0.63,0.96,1.0,1.0,1.0,0.84,0.17,0,0,0,0,0,0,0,0.13,0.35,0.51,0.64,0.77,0.91,0.99,1.0,1.0,1.0,1.0,0.88,0.58,0.29,0.09], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07,0.38,0.72,0.95,1.0,1.0,1.0,0.22,0,0,0,0,0,0,0,0,0,0.11,0.33,0.5,0.67,0.86,0.99,1.0,1.0,1.0,1.0,0.95,0.64,0.33,0.1], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.32,0.49,0.71,0.93,1.0,1.0,1.0,0.56,0,0,0,0,0,0,0,0,0,0,0,0.1,0.31,0.52,0.79,0.98,1.0,1.0,1.0,1.0,0.98,0.67,0.35,0.11], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.6,0.83,0.98,1.0,1.0,0.68,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15,0.38,0.71,0.97,1.0,1.0,1.0,1.0,0.97,0.67,0.35,0.11], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.51,0.96,1.0,1.0,0.18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09,0.34,0.68,0.95,1.0,1.0,1.0,1.0,0.91,0.61,0.32,0.1], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13,0.56,0.99,1.0,1.0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.17,0.45,0.76,0.96,1.0,1.0,1.0,1.0,0.82,0.52,0.26,0.07], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.33,0.7,0.94,1.0,1.0,0.44,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.33,0.68,0.91,0.99,1.0,1.0,1.0,1.0,0.71,0.42,0.19,0.03], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.53,0.89,1.0,1.0,1.0,0.8,0.43,0.04,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.47,0.86,1.0,1.0,1.0,1.0,1.0,0.95,0.58,0.32,0.12,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.77,0.99,1.0,0.97,0.58,0.41,0.33,0.18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.54,0.95,1.0,1.0,1.0,1.0,1.0,0.8,0.44,0.21,0.06,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.39,0.83,1.0,1.0,0.55,0.11,0.05,0.15,0.22,0.06,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.58,0.99,1.0,1.0,1.0,1.0,1.0,0.59,0.29,0.11,0.01,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0.55,0.81,0.86,0.97,1.0,1.0,0.5,0,0,0.01,0.09,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26,0.78,1.0,1.0,1.0,1.0,1.0,0.66,0.35,0.13,0.03,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.33,1.0,1.0,1.0,1.0,1.0,1.0,0.93,0.11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.23,0.73,0.95,1.0,1.0,1.0,1.0,1.0,0.62,0.35,0.12,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.51,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.72,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.56,0.25,0.09,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12,0.38,1.0,1.0,1.0,0.66,0.08,0.55,1.0,1.0,1.0,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0,0.35,1.0,1.0,1.0,1.0,1.0,1.0,0.67,0.12,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.6,1.0,1.0,1.0,1.0,1.0,1.0,0.49,0,0,0.87,1.0,0.88,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.0,1.0,1.0,1.0,1.0,1.0,0.7,0.07,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.04,0.21,0.48,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0,0,0.04,0.42,0.26,0,0,0,0,0,0,0,0,0,0.12,0.21,0.34,0.58,1.0,1.0,1.0,0.99,0.97,0.99,0.46,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.5,1.0,1.0,1.0,1.0,0.96,0,0.31,1.0,1.0,1.0,0.53,0,0,0,0,0,0,0,0,0.2,0.21,0,0,0,0.27,1.0,1.0,1.0,1.0,1.0,1.0,0.87,0.52,0.01,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.84,1.0,1.0,1.0,1.0,1.0,0,0,0,0.83,1.0,1.0,0.52,0,0,0,0,0,0,0,0.26,0.82,0.59,0.02,0,0,0.46,1.0,1.0,1.0,1.0,1.0,0.9,0.55,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0.39,0.99,1.0,1.0,1.0,1.0,0.78,0.04,0,0,0,0.93,0.92,0,0,0,0,0,0,0,0,0.69,1.0,1.0,0.36,0,0,1.0,1.0,0.65,0.66,0.97,0.87,0.54,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.55,0.75,0.59,0.74,1.0,1.0,0,0,0.75,0.71,0.18,0,0,0,0,0,0,0,0,0,0,0.29,0,0,0.45,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.47,0.39,0.71,0.25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.69,0.81,0.8,0.92,1.0,0.13,0,0,0.13,0.94,0.58,0,0,0,0,0,0,0,0,0,1.0,1.0,0.34,0,0.04,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.63,0.85,0.9,0.98,1.0,0.09,0,0,0.02,1.0,0.64,0,0,0,0,0,0,0,0,0.59,1.0,1.0,0.84,0,0,1.0,1.0,1.0,1.0,1.0,1.0,0.64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.64,0.65,0.67,1.0,1.0,0.21,0.01,0,0.04,0.02,0,0,0,0,0,0,0,0,0,0.69,1.0,1.0,1.0,0.29,0.37,1.0,1.0,0.6,0.63,1.0,0.84,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.44,0.73,0.73,0.85,1.0,0.97,0.23,0.05,0,0,0,0,0,0,0,0,0.06,0,0,0,0.97,1.0,1.0,1.0,1.0,1.0,1.0,0.33,0.24,0.67,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0.12,0.55,0.9,0.9,1.0,1.0,1.0,0.43,0.04,0,0,0,0,0,0,0,0.31,0.54,0,0,0,0.88,1.0,1.0,1.0,1.0,1.0,1.0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0.29,0.71,1.0,1.0,1.0,1.0,0.79,0.28,0,0,0,0,0,0,0,0,0.4,0.77,0.54,0,0,0.87,1.0,1.0,1.0,1.0,1.0,0.31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0.16,0.27,0.41,0.72,0.99,1.0,1.0,0.82,0.42,0.09,0,0,0,0,0,0,0,0,0.1,0.55,0.58,0.58,0.77,0.99,1.0,1.0,1.0,1.0,0.63,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0.31,0.48,0.45,0.46,0.63,0.88,1.0,0.83,0.59,0.28,0.06,0,0,0,0,0,0,0,0,0,0.32,0.7,0.95,1.0,1.0,1.0,1.0,0.7,0.58,0.12,0.04,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0.23,0.54,0.53,0.48,0.57,0.59,0.65,0.63,0.55,0.35,0.13,0.03,0.02,0.09,0.74,1.0,0.09,0,0,0,0.32,0.86,1.0,1.0,1.0,1.0,0.57,0.44,0.31,0.16,0.01,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0.31,0.45,0.31,0.18,0.28,0.39,0.47,0.54,0.5,0.35,0.2,0.16,0.28,0.75,1.0,0.42,0.01,0,0,0.6,1.0,1.0,1.0,1.0,0.51,0.29,0.09,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0.14,0.3,0.4,0.54,0.71,0.74,0.65,0.49,0.35,0.27,0.47,0.6,0.6,0.72,0.98,1.0,1.0,1.0,1.0,0.65,0.33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0.06,0.33,0.53,0.69,0.94,0.99,1.0,0.84,0.41,0.16,0.15,0.96,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.73,0.13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0.42,0.86,0.98,0.98,0.99,1.0,0.94,0.63,0.32,0.62,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.65,0.23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0.07,0.62,0.95,1.0,1.0,0.99,0.98,0.99,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.98,0.14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0.03,0.46,0.89,1.0,1.0,0.97,0.83,0.75,0.81,0.94,1.0,1.0,1.0,1.0,0.99,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0.14,0.57,0.88,0.93,0.81,0.58,0.45,0.48,0.64,0.86,0.97,0.99,0.99,0.42,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.23,0.45,0.47,0.39,0.29,0.19,0.2,0.46,0.28,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0.08,0.22,0.24,0.15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0.07,0.22,0.14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

cells = np.zeros((N,M))
pos_x, pos_y = 70, 10
cells[pos_x:pos_x + hydrogeminium.shape[0], pos_y:pos_y + hydrogeminium.shape[1]] = hydrogeminium
```

Pour la distance euclidienne, on prendra $r=18$ pour l'hydrogenium
et pour la fonction de croissance on prendra  $\mu = 0.26$ et $\sigma = 0.036$.

### 8. Généralisation de la fonction de croissance

Toujours dans le soucis de généraliser, nous allons généraliser la fonction de croissance en la décomposant en $n$ fonctions de croissances $g_{i}$ qui utiliseront chacune une convolution $K_{i}$ différente. Ces fonctions $g_{i}$ utiliseront chacune une fonction gaussienne dont les paramètres $\mu_{i}$ et $\sigma_{i}$ seront différentes pour chaque $g_{i}$.

La fonction de croissance finale sera simplement la moyenne de ces fonctions de croissance.

Comme dans l'exemple précédent, les convolutions seront définies par une somme de gaussiennes ayant pour support des anneaux concentriques (le nombre d'anneau peut varier selon les convolutions).

Pour toutes les convolutions, on prend $\mu = 0.5$ et $\sigma = 0.15$.

#### Première convolution

Cette convolution sera composée de trois anneaux concentriques :

- *Première gaussienne* :  

$$
\begin{cases}
g_{1}(r) & = & e^{-\frac{1}{2}\left(\frac{r-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[0;1\right[\\
g_{1}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

- *Seconde gaussienne* : 

$$
\begin{cases}
g_{2}(r) & = & \frac{5}{12}.e^{-\frac{1}{2}\left(\frac{(r\mod 1)-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[1;2\right[\\
g_{2}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

- *Troisième gaussienne* : 

$$
\begin{cases}
g_{3}(r) & = & \frac{2}{3}.e^{-\frac{1}{2}\left(\frac{(r\mod 1)-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[2;3\right[\\
g_{3}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

#### Deuxième convolution

Cette convolution sera composée de deux anneaux concentriques :

- *Première gaussienne* : 

$$
\begin{cases}
g_{1}(r) & = & \frac{1}{12}.e^{-\frac{1}{2}\left(\frac{r-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[0;1\right[\\
g_{1}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

- *Seconde gaussienne* : 

$$
\begin{cases}
g_{2}(r) & = & e^{-\frac{1}{2}\left(\frac{(r\mod 1)-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[1;2\right[\\
g_{2}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

#### Troisième convolution

Cette convolution sera composée que d'un seul anneau :

$$
\begin{cases}
g_{1}(r) & = & e^{-\frac{1}{2}\left(\frac{r-\mu}{\sigma}\right)^{2}}\,\,\textrm{pour}\,\,r\in\left[0;1\right[\\
g_{1}(r) & = & 0\,\,\textrm{sinon}
\end{cases}
$$

#### Fonction de croissance

La fonction de croissance quant à elle est la moyenne de plusieurs fonctions de croissance qui sont toutes des gaussiennes dont les paramètres $\mu$ et $\sigma$  varient :

- *Première fonction de croissance* : $\mu = 0,156$ et $\sigma = 0,0118$
- *Deuxième fonction de croissance* : $\mu = 0,193$ et $\sigma = 0,049$
- *Troisième fonction de croissance* : $\mu = 0,342$ et $\sigma = 0,0891$

Pour le test, on prendra leav pattern initial suivant :

```python
N = 128
M = int(np.ceil((16*N)/9))

fish = np.array([[0,0,0,0,0,0,0,0,0,0,0,0.06,0.1,0.04,0.02,0.01,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.15,0.37,0.5,0.44,0.19,0.23,0.3,0.23,0.15,0.01,0,0,0,0], [0,0,0,0,0,0,0.32,0.78,0.26,0,0.11,0.11,0.1,0.08,0.18,0.16,0.17,0.24,0.09,0,0,0], [0,0,0,0,0.45,0.16,0,0,0,0,0,0.15,0.15,0.16,0.15,0.1,0.09,0.21,0.24,0.12,0,0], [0,0,0,0.1,0,0,0,0,0,0,0,0.17,0.39,0.43,0.34,0.25,0.15,0.16,0.15,0.25,0.03,0], [0,0.15,0.06,0,0,0,0,0,0,0,0.24,0.72,0.92,0.85,0.61,0.47,0.39,0.27,0.12,0.18,0.17,0], [0,0.08,0,0,0,0,0,0,0,0,1.0,1.0,1.0,1.0,0.73,0.6,0.56,0.31,0.12,0.15,0.24,0.01], [0,0.16,0,0,0,0,0,0,0,0.76,1.0,1.0,1.0,1.0,0.76,0.72,0.65,0.39,0.1,0.17,0.24,0.05], [0,0.05,0,0,0,0,0,0,0.21,0.83,1.0,1.0,1.0,1.0,0.86,0.85,0.76,0.36,0.17,0.13,0.21,0.07], [0,0.05,0,0,0.02,0,0,0,0.4,0.91,1.0,1.0,1.0,1.0,1.0,0.95,0.79,0.36,0.21,0.09,0.18,0.04], [0.06,0.08,0,0.18,0.21,0.1,0.03,0.38,0.92,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.64,0.31,0.12,0.07,0.25,0], [0.05,0.12,0.27,0.4,0.34,0.42,0.93,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.97,0.33,0.16,0.05,0.1,0.26,0], [0,0.25,0.21,0.39,0.99,1.0,1.0,1.0,1.0,1.0,1.0,0.86,0.89,0.94,0.83,0.13,0,0,0.04,0.21,0.18,0], [0,0.06,0.29,0.63,0.84,0.97,1.0,1.0,1.0,0.96,0.46,0.33,0.36,0,0,0,0,0,0.03,0.35,0,0], [0,0,0.13,0.22,0.59,0.85,0.99,1.0,0.98,0.25,0,0,0,0,0,0,0,0,0.34,0.14,0,0], [0,0,0,0,0.33,0.7,0.95,0.8,0.33,0.11,0,0,0,0,0,0,0,0.11,0.26,0,0,0], [0,0,0,0,0.16,0.56,0.52,0.51,0.4,0.18,0.01,0,0,0,0,0,0,0.42,0,0,0,0], [0,0,0,0,0.01,0,0.33,0.47,0.33,0.05,0,0,0,0,0,0,0.35,0,0,0,0,0], [0,0,0,0,0,0.26,0.32,0.13,0,0,0,0,0,0,0,0.34,0,0,0,0,0,0], [0,0,0,0,0,0.22,0.25,0.03,0,0,0,0,0,0,0.46,0,0,0,0,0,0,0], [0,0,0,0,0,0,0.09,0.2,0.22,0.23,0.23,0.22,0.3,0.3,0,0,0,0,0,0,0,0]])

cells = np.zeros((N,M))
pos_x, pos_y = 100, 100
cells[pos_x:pos_x + fish.shape[0], pos_y:pos_y + fish.shape[1]] = fish
```

avec la distance euclidienne définie avec $r=10$.


### 9. Généralisation à des canaux couleurs multiples

Enfin, pour finir, nous allons généraliser à plusieurs canaux de couleur (Rouge, Vert et Bleu). Les cellules contiendront donc trois valeurs pour la vitalité.

Les convolutions se feront inter-canaux. C'est à dire qu'une convolution pourra s'appliquer à un canal $i$. Chaque convolution seront des convolutions multi-anneaux comme dans la section précédente.

La fonction de croissance sera quant à elle une combinaison de plusieurs fonctions de croissance, chaque fonction ayant ses propres paramètres $\mu$ et $\sigma$ pour la fonction gaussienne et sera appliquée à un canal *destination* sous la forme d'une somme pondérée.

Les différentes convolutions et fonctions de croissance sont définis au travers de la liste de dictionnaire suivant :

```python 
kernels = [
  {"b":[1],"m":0.272,"s":0.0595,"h":0.138,"r":0.91,"c0":0,"c1":0},
  {"b":[1],"m":0.349,"s":0.1585,"h":0.48,"r":0.62,"c0":0,"c1":0},
  {"b":[1,1/4],"m":0.2,"s":0.0332,"h":0.284,"r":0.5,"c0":0,"c1":0},
  {"b":[0,1],"m":0.114,"s":0.0528,"h":0.256,"r":0.97,"c0":1,"c1":1},
  {"b":[1],"m":0.447,"s":0.0777,"h":0.5,"r":0.72,"c0":1,"c1":1},
  {"b":[5/6,1],"m":0.247,"s":0.0342,"h":0.622,"r":0.8,"c0":1,"c1":1},
  {"b":[1],"m":0.21,"s":0.0617,"h":0.35,"r":0.96,"c0":2,"c1":2},
  {"b":[1],"m":0.462,"s":0.1192,"h":0.218,"r":0.56,"c0":2,"c1":2},
  {"b":[1],"m":0.446,"s":0.1793,"h":0.556,"r":0.78,"c0":2,"c1":2},
  {"b":[11/12,1],"m":0.327,"s":0.1408,"h":0.344,"r":0.79,"c0":0,"c1":1},
  {"b":[3/4,1],"m":0.476,"s":0.0995,"h":0.456,"r":0.5,"c0":0,"c1":2},
  {"b":[11/12,1],"m":0.379,"s":0.0697,"h":0.67,"r":0.72,"c0":1,"c1":0},
  {"b":[1],"m":0.262,"s":0.0877,"h":0.42,"r":0.68,"c0":1,"c1":2},
  {"b":[1/6,1,0],"m":0.412,"s":0.1101,"h":0.43,"r":0.82,"c0":2,"c1":0},
  {"b":[1],"m":0.201,"s":0.0786,"h":0.278,"r":0.82,"c0":2,"c1":1}]
R = 12 # Pour la distance euclidienne en nombre de pixels
```

où ```b``` sont les rayons des différents anneaux composant la convolution, ```r``` le rayon d'action unité de la convolution (premier anneau rayon ```r.R```, deuxième anneau rayon ```2r.R```, etc.), ```m``` la valeur de $\mu$ pour la fonction de croissance associée à cette convolution, ```s``` la valeur de $\sigma$ pour la fonction de croissance associée à cette convolution, ```h``` le cœfficient de pondération pour la fonction de croissance, ```c0``` le canal (0 = Rouge, 1 = Vert, 2 = Bleu) sur lequel on applique la convolution, ```c1``` le canal (même code que pour ```c0```) sur lequel on rajoute la contribution pondérée de la fonction de croissance.

Pour le pattern initial, on prendra le pattern suivant :

```python
N = 128
M = int(np.ceil((16*N)/9))

aquarium = [[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.49,1.0,0,0.03,0.49,0.49,0.28,0.16,0.03,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0.6,0.47,0.31,0.58,0.51,0.35,0.28,0.22,0,0,0,0,0], [0,0,0,0,0,0,0.15,0.32,0.17,0.61,0.97,0.29,0.67,0.59,0.88,1.0,0.92,0.8,0.61,0.42,0.19,0,0,0], [0,0,0,0,0,0,0,0.25,0.64,0.26,0.92,0.04,0.24,0.97,1.0,1.0,1.0,1.0,0.97,0.71,0.33,0.12,0,0], [0,0,0,0,0,0,0,0.38,0.84,0.99,0.78,0.67,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.95,0.62,0.37,0,0], [0,0,0,0,0.04,0.11,0,0.69,0.75,0.75,0.91,1.0,1.0,0.89,1.0,1.0,1.0,1.0,1.0,1.0,0.81,0.42,0.07,0], [0,0,0,0,0.44,0.63,0.04,0,0,0,0.11,0.14,0,0.05,0.64,1.0,1.0,1.0,1.0,1.0,0.92,0.56,0.23,0], [0,0,0,0,0.11,0.36,0.35,0.2,0,0,0,0,0,0,0.63,1.0,1.0,1.0,1.0,1.0,0.96,0.49,0.26,0], [0,0,0,0,0,0.4,0.37,0.18,0,0,0,0,0,0.04,0.41,0.52,0.67,0.82,1.0,1.0,0.91,0.4,0.23,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0.05,0.45,0.89,1.0,0.66,0.35,0.09,0], [0,0,0.22,0,0,0,0.05,0.36,0.6,0.13,0.02,0.04,0.24,0.34,0.1,0,0.04,0.62,1.0,1.0,0.44,0.25,0,0], [0,0,0,0.43,0.53,0.58,0.78,0.9,0.96,1.0,1.0,1.0,1.0,0.71,0.46,0.51,0.81,1.0,1.0,0.93,0.19,0.06,0,0], [0,0,0,0,0.23,0.26,0.37,0.51,0.71,0.89,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.42,0.06,0,0,0], [0,0,0,0,0.03,0,0,0.11,0.35,0.62,0.81,0.93,1.0,1.0,1.0,1.0,1.0,0.64,0.15,0,0,0,0,0], [0,0,0,0,0,0,0.06,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0.05,0.09,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
  [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02,0.28,0.42,0.44,0.34,0.18,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.34,1.0,1.0,1.0,1.0,1.0,0.91,0.52,0.14,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.17,0.75,1.0,1.0,1.0,1.0,1.0,1.0,0.93,0.35,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22,0.92,1.0,1.0,1.0,1.0,1.0,1.0,0.59,0.09], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.75,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.71,0.16], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.67,0.83,0.85,1.0,1.0,1.0,1.0,1.0,1.0,0.68,0.17], [0,0,0,0,0,0,0,0,0,0,0,0,0.21,0.04,0.12,0.58,0.95,1.0,1.0,1.0,1.0,1.0,0.57,0.13], [0,0,0,0,0,0,0,0,0,0,0,0.07,0,0,0,0.2,0.64,0.96,1.0,1.0,1.0,0.9,0.24,0.01], [0,0,0,0,0,0,0,0,0,0,0.13,0.29,0,0,0,0.25,0.9,1.0,1.0,1.0,1.0,0.45,0.05,0], [0,0,0,0,0,0,0,0,0,0,0.13,0.31,0.07,0,0.46,0.96,1.0,1.0,1.0,1.0,0.51,0.12,0,0], [0,0,0,0,0,0,0,0,0.26,0.82,1.0,0.95,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.3,0.05,0,0,0], [0,0,0,0,0,0,0,0,0.28,0.74,1.0,0.95,0.87,1.0,1.0,1.0,1.0,1.0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.07,0.69,1.0,1.0,1.0,1.0,1.0,0.96,0.25,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0.4,0.72,0.9,0.83,0.7,0.56,0.43,0.14,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
  [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.04,0.25,0.37,0.44,0.37,0.24,0.11,0.04,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.19,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.75,0.4,0.15,0,0,0,0], [0,0,0,0,0,0,0,0,0.14,0.48,0.83,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.4,0,0,0,0], [0,0,0,0,0,0,0,0,0.62,0.78,0.94,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.64,0,0,0,0], [0,0,0,0,0,0,0,0.02,0.65,0.98,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.78,0,0,0,0], [0,0,0,0,0,0,0,0.15,0.48,0.93,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.79,0.05,0,0,0], [0,0,0,0,0,0,0.33,0.56,0.8,1.0,1.0,1.0,0.37,0.6,0.94,1.0,1.0,1.0,1.0,0.68,0.05,0,0,0], [0,0,0,0,0.35,0.51,0.76,0.89,1.0,1.0,0.72,0.15,0,0.29,0.57,0.69,0.86,1.0,0.92,0.49,0,0,0,0], [0,0,0,0,0,0.38,0.86,1.0,1.0,0.96,0.31,0,0,0,0,0.02,0.2,0.52,0.37,0.11,0,0,0,0], [0,0,0.01,0,0,0.07,0.75,1.0,1.0,1.0,0.48,0.03,0,0,0,0,0,0.18,0.07,0,0,0,0,0], [0,0.11,0.09,0.22,0.15,0.32,0.71,0.94,1.0,1.0,0.97,0.54,0.12,0.02,0,0,0,0,0,0,0,0,0,0], [0.06,0.33,0.47,0.51,0.58,0.77,0.95,1.0,1.0,1.0,1.0,0.62,0.12,0,0,0,0,0,0,0,0,0,0,0], [0.04,0.4,0.69,0.88,0.95,1.0,1.0,1.0,1.0,1.0,0.93,0.68,0.22,0.02,0,0,0.01,0,0,0,0,0,0,0], [0,0.39,0.69,0.91,1.0,1.0,1.0,1.0,1.0,0.85,0.52,0.35,0.24,0.17,0.07,0,0,0,0,0,0,0,0,0], [0,0,0.29,0.82,1.0,1.0,1.0,1.0,1.0,1.0,0.67,0.29,0.02,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.2,0.51,0.77,0.96,0.93,0.71,0.4,0.16,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.08,0.07,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0]]]
aquarium = [np.array(aquarium[c]) for c in range(3)]

cells = np.zeros((N,M,3))
pos_x,pos_y = N//2,M//2
for c in range(3):
    cells[pos_x:pos_x + aquarium[c].shape[0], pos_y:pos_y + aquarium[c].shape[1],c] = aquarium[c]

pos_x,pos_y = N//4,M//4
for c in range(3):
    cells[pos_x:pos_x + aquarium[c].shape[0], pos_y:pos_y + aquarium[c].shape[1],c] = aquarium[c]

pos_x,pos_y = N//2,M//4
for c in range(3):
    cells[pos_x:pos_x + aquarium[c].shape[0], pos_y:pos_y + aquarium[c].shape[1],c] = aquarium[c]

pos_x,pos_y = N//4,M//2
for c in range(3):
    cells[pos_x:pos_x + aquarium[c].shape[0], pos_y:pos_y + aquarium[c].shape[1],c] = aquarium[c]
```

Cet exemple est très intéressant par rapport au pas de temps choisi.
Essayez les trois valeurs suivantes pour le pas de temps :

- $dt = 0.1$ et $dt = 0.2$
- $dt = 0.5$ et $dt = 0.75$
- $dt = 0.235$

Qu'en concluez-vous ?
