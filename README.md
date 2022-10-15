# **PERF-CONT** [(tp-perfs)](https://helene-coullon.fr/pages/ue-services-fise-22-23/tp-perfs/)

# Partie PERFS

Cette partie vise à tester les performances des différentes API développées précédemment.

## Dockerization

Executer `docker-compose up` dans le dossier services
Publiera 3 copies du service simple movie sous différent paradigme de communication (GraphQL, gRPC, REST)

| Service | Port |
| ------- | ---- |
| REST    | 3001 |
| gRPC    | 3002 |
| GraphQL | 3003 |

## Comment tester ?

Il suffiera une fois les services ouverts de lancer le script `main.py`

# Partie BALANCER

Cette partie vise à utiliser le load balancer du proxy inversé de NGINX pour répartir la charge sur différentes instances du service movie (REST)

## Dockerization

Executer `docker-compose up` dans le dossier services
Publiera 9 copies du service simple movie (REST), et trois container NGINX, le premier balancant la charge sur 4 services, l'autres sur 9, le dernier sur 9 avec une repartition de la charge suivant un algorithme de moindre connexion active.

| Service | Port      |
| ------- | --------- |
| movie   | 5001-5009 |
| nginx   | 8000      |
| nginx2  | 8001      |
| nginx3  | 8002      |

# Comment tester ?

Il suffiera une fois les services ouverts de lancer le script `performance.py`
