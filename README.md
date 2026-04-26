# test_ops_dataplatform
## part1 pyinfra
### flask
app flask qui expose un endpoint health, exposé sur le port 8080

### systemd service
Exécution via flask --app run ==> OK Pour POC / Dev, KO prod

### pyinfra
Pour le déploiement pyinfra la 1ère idée était de créer 2 service docker basé sur des images alpine avec ssh

Le problème c'est qu'alpine n'utilise par systemd mais OpenRC ==> **KO**

Passage sur une debian ssh, docker et systemd ne font pas bon ménage ==> **KO**

Utilisation de Debian sur WSL ==> **OK**

Utilisation d'une distribution Ubuntu pour "simuler" un 2ème serveur (en reconfigurant les ports 2221 & 2222 au lieu de 22) ==> **OK** pour le déploiement via pyinfra, **KO** pour le service systemd car l'api est lancée 2 fois avec le port 8080. Limite malheureusement de WSL

Depuis le passage sur WSL, utilisation du user root pour simplifier un peu (pas bien).
Installtion openssh-server
Génération d'une clé publique / privée via ssh-keygen
Ajout de la clé publique dans ~/.ssh/authorized_keys


## part 2 k8s + clickhouse

### Mise en place de l'instance clickhouse 
Sur WSL installation de kubectl et k3d + activation de l'intégration WSL dans docker desktop
Mise en place du même environnement sur macOs pour tester le déploiement sur une autre plateforme.

Création d'un noeud de test
```bash
k3d cluster create clickhouse-cluster
```
Création du StatefulSet. Entre Deployment et StatefulSet ChatGPT suggère un StatefulSet pour une BDD.
```bash
kubectl apply -f clickhouse-deployment.yaml
```
Vérifications diverses
```bash
kubectl get statefulsets # On vérifie que le statefulset est bien créé
kubectl get pods # Que le pod tourne bien
kubectl describe statefulset clickhouse
kubectl get pvc # vérification du volume
kubectl logs clickhouse-0
```

ClickHouse désactive le network si aucun USER / PASSWORD n'est défini
Création d'un secret à partir d'un fichier .env 
```bash
kubectl create secret generic clickhouse-secret --from-env-file=.env
```
Modification du clickhouse-deployment.yaml pour ajouter le user et password.
Redeploiement + restart
```bash
kubectl rollout restart statefulset clickhouse
```

Création du service
```bash
kubectl apply -f clickhouse-service.yaml
```
Vérifications
```bash
kubectl get svc
kubectl describe svc clickhouse
```
Forward du port
```bash
kubectl port-forward svc/clickhouse 8123:8123
```

Une fois toutes ces étapes sur http://localhost:8123 on a bien une instance de clikhouse **OK**

### Création de la table
L'énoncé laissé entendre qu'on pouvait créer la table via l'interface. On va faire un fichier **job_metrics.sql** et une méthode python dans le module **send_metrics.py** à la place.
Ajout de create database pour éviter de créer la table dans **default**.

L'utilisation de **sqlglot** qui a un dialect clickhouse a été testé mais **KO** car **FORMAT** n'est pas une expression SQL valide. 

On pourrait ajouter un paramètre format pour valider la requête sans et ajouter le format après dans le cadre d'une insertion de données.


### Insertion de mock data
Utilisation de faker pour générer des données dans la fonction **mock_data()**.

### tests
Ajout de tests pytest pour valider que la table existe et qu'elle contient des lignes.
Il faudrait ajouter des tests unitaire sur la fonction run_query

### BONUS
Création d'un déploiement pyinfra pour le cluster clickhouse.
Création d'un module **send_metrics_clickhouse_connect** qui réalise les mêmes étapes mais avec un client **clickhouse_connect** et des données au format polars / arrow.

Cette partie ne suit pas les consignes du test mais s'approche plus de ce que je ferais si j'avais le choix des méthodes / outils. Jusqu'à trouver mieux.