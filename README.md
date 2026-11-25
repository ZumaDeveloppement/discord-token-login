<div align="center">

# ◈ Discord Token Login

**Connexion Discord via token — GUI violet animé**

![Python](https://img.shields.io/badge/Python-3.8%2B-7b2ff7?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-9b59f5?style=for-the-badge&logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-4a1f8a?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-3d1f6b?style=for-the-badge)

*by GenZ · 2026*

</div>

---

## 📌 À propos

**Discord Token Login** est un outil GUI permettant de se connecter à un compte Discord via son token d'authentification, sans saisir email/mot de passe.

- Splash screen animé **Matrix** violet au démarrage
- Interface **sombre violet** avec effets de glow
- Injection via **webpack JS** (deux méthodes de fallback)
- Chrome ouvert directement sur le compte

> ⚠️ **Usage éducatif / personnel uniquement.** N'utilisez pas cet outil sur des comptes qui ne vous appartiennent pas.

---

## ✨ Fonctionnalités

| Feature | Détail |
|---|---|
| 🎬 Splash animé | Matrix violet — 3.2s, révélation char par char |
| 🔐 Input token | Mode masqué / affiché à la volée |
| 💉 Injection webpack | 2 méthodes enchaînées en fallback |
| 🌐 Chrome automatisé | Via `undetected-chromedriver` |
| 📋 Console intégrée | Log en temps réel dans l'UI |
| 🎨 UI violet complète | Gradients, glow, shadows, 60fps |

---

## 🚀 Installation

### Prérequis

- Python **3.8+**
- Google Chrome installé

### Lancer depuis les sources

```bash
# Cloner le repo
git clone https://github.com/TON_USERNAME/discord-token-login.git
cd discord-token-login

# Installer les dépendances
pip install PyQt5 undetected-chromedriver selenium

# Lancer
python discord_token_gui.py
```

### Compiler un `.exe` (Windows)

```bash
build.bat
```

> Le `.exe` apparaît dans `dist/` et est copié à la racine automatiquement.

---

## 🔧 Dépendances

```
PyQt5                    — Interface graphique
undetected-chromedriver  — Chrome non-détecté
selenium                 — Automation navigateur
```

---

## 📁 Structure

```
discord-token-login/
├── discord_token_gui.py   # Source principal — UI + logique
├── build.bat              # Script de compilation PyInstaller
└── README.md
```

---

## ⚙️ Comment ça marche

1. L'utilisateur colle son token Discord dans le champ
2. Un thread worker lance Chrome via `undetected-chromedriver`
3. Discord est ouvert, le token est injecté via `localStorage` + `webpack`
4. Chrome redirige vers `discord.com/channels/@me`
5. La connexion est vérifiée via l'URL courante

---

## 📜 Licence

MIT — Voir [LICENSE](LICENSE)

---

<div align="center">
<sub>◈ GenZ · Discord Token Login · 2026</sub>
</div>
