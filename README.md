**✅ Voici un beau README.md propre et bien structuré :**

````markdown
# 🏬 Quincaillerie - Application de gestion

Application web de gestion de quincaillerie développée avec **Django** et **PostgreSQL**.  
Elle permet de gérer les stocks, les ventes, les achats, les clients, les fournisseurs, les inventaires, et inclut un tableau de bord avec des statistiques.

---

## 🚀 Fonctionnalités

- **Authentification** sécurisée avec rôles (Administrateur, Gérant, Magasinier, Caissier)
- **Gestion des produits et catégories** (recherche, filtrage, alerte stock minimum)
- **Gestion des fournisseurs et clients**
- **Achats** avec mise à jour automatique du stock
- **Ventes** avec contrôle des stocks et génération de ticket de caisse / facture PDF
- **Historique complet des mouvements de stock**
- **Inventaires physiques** avec calcul des écarts et ajustements
- **Ajustements manuels du stock**
- **Tableau de bord** dynamique avec graphiques (Chart.js)
- **Génération de PDF** (Bons d'achat et Factures de vente) avec WeasyPrint
- **Journal d'audit** traçant toutes les actions sensibles
- **Interface moderne et responsive** (Bootstrap 5)

---

## 🧰 Prérequis

- Python 3.10+
- PostgreSQL (ou SQLite pour le développement)
- pip

## ⚙️ Installation locale

1. **Cloner le dépôt**
   ```bash
   git clone <url-du-depot>
   cd quincaillerie
   ```
````

2. **Créer et activer l'environnement virtuel**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Sur Windows : venv\Scripts\activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   Copiez le fichier `.env.example` en `.env` et ajustez les valeurs si nécessaire.

5. **Appliquer les migrations**

   ```bash
   python manage.py migrate
   ```

6. **Initialiser les groupes d'utilisateurs**

   ```bash
   python manage.py init_groups
   ```

7. **Créer un superutilisateur**

   ```bash
   python manage.py createsuperuser
   ```

8. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

Accédez à l’application sur : **http://127.0.0.1:8000**

---

## 🐳 Déploiement

L’application est prête pour un déploiement sur **Render** ou **Railway**.

Fichiers déjà configurés :

- `requirements.txt`
- `runtime.txt`
- `Procfile`
- `build.sh` (pour WeasyPrint)
- `render.yaml` (optionnel)
- Configuration de production

### Sur Render

1. Créez un nouveau **Web Service** lié à votre dépôt.
2. Build command : `./build.sh`
3. Start command : `gunicorn config.wsgi:application --log-file -`
4. Ajoutez les variables d’environnement :
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=.onrender.com`
   - `DATABASE_URL`
   - `DJANGO_SETTINGS_MODULE=config.settings.production`
5. Exécutez les commandes après déploiement :
   ```bash
   python manage.py migrate
   python manage.py init_groups
   ```

---

## 📁 Structure du projet

```bash
quincaillerie/
├── apps/                    # Applications Django
│   ├── accounts/
│   ├── inventory/
│   ├── purchases/
│   ├── sales/
│   ├── suppliers/
│   ├── customers/
│   ├── dashboard/
│   └── audit/
├── config/                  # Configuration Django
│   └── settings/
│       ├── base.py
│       ├── development.py
│       └── production.py
├── static/
├── templates/
├── media/
├── manage.py
└── requirements.txt
```

---

## 🔑 Principales URLs

| URL                    | Description                |
| ---------------------- | -------------------------- |
| `/`                    | Tableau de bord            |
| `/admin/`              | Interface d'administration |
| `/accounts/login/`     | Connexion                  |
| `/inventory/produits/` | Liste des produits         |
| `/purchases/`          | Achats                     |
| `/sales/`              | Ventes                     |
| `/audit/`              | Journal d'audit            |

---

## 📄 Licence

Ce projet est un exemple pédagogique. Vous êtes libre de l’utiliser et de le modifier.

## 🤝 Contribution

Les contributions sont les bienvenues !  
N’hésitez pas à ouvrir une **issue** ou une **pull request**.

---

**Prêt à déployer ?**  
Poussez ce README sur GitHub et lancez votre déploiement !

```

---

**Tu peux copier-coller directement** ce contenu dans un fichier `README.md`.

Veux-tu que je modifie quelque chose (ajouter des badges, changer le ton, ajouter des captures d’écran, etc.) ?
```
