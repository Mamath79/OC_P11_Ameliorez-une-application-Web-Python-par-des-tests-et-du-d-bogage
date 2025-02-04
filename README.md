## OC_P11 - Améliorez une application Web Python par des tests et du débogage**

###Description**
Ce projet a pour objectif d'améliorer une application web existante en renforçant la **qualité du code**, la **robustesse des fonctionnalités** et la **performance globale** grâce à des **tests unitaires**, **tests d'intégration**, une **analyse de couverture de code**, et des **tests de performance** avec Locust.

---

## Installation et Configuration

### Prérequis
- Python 3.12
- Git
- Un terminal compatible (bash, zsh, etc.)
- Un éditeur de code (VS Code recommandé)
- **pip** pour la gestion des dépendances

### Cloner le dépôt
```bash
git clone https://github.com/Mamath79/OC_P11_Ameliorez-une-application-Web-Python-par-des-tests-et-du-d-bogage.git
cd OC_P11_Ameliorez-une-application-Web-Python-par-des-tests-et-du-d-bogage
```

### Créer et activer un environnement virtuel
```bash
python -m venv env
```
#### Sous Linux & Mac OS

```bash
source env/bin/activate 
```
#### Sous Windows
```bash
env\Scripts\activate 
```

### Installer les dépendances
```bash
pip install -r requirements.txt
```

---
## Pointer server.py comme app pour Flask
```bash
export 'FLASK_APP'=server.py
```

## Lancement de l'application
```bash
flask run
```
Par défaut, l'application tourne sur **http://127.0.0.1:5000**.

---

## Exécution des tests

### Lancer tous les tests unitaires et d'intégration
```bash
pytest
```

### Exécuter les tests avec un rapport de couverture
```bash
coverage run -m pytest
coverage report
coverage html
```

#### Ouvrir le rapport de couverture au format HTML
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```
> **Objectif** : Assurer un taux de couverture **≥ 60%** (exigence du projet).

---

## Tests de Performance avec Locust
### Démarrer l'interface web Locust

```bash
locust -f tests/performance_tests/locustfile.py
```
> **Ouvrir Locust** sur : **http://127.0.0.1:8089**

#### Ouvrir le rapport de performance au format HTML
```bash
open locust_report.html  # macOS
xdg-open locust_report.html  # Linux
start locust_report.html  # Windows
```
>  **Objectifs** :
> - **Temps de chargement max : 5s**
> - **Mises à jour ≤ 2s**
> - **6 utilisateurs simultanés**

---

##  Auteurs
- **Mathieu Vieillefont** - Ingénieur du son & Développeur Python
- **Formation OpenClassrooms - Développeur Python**