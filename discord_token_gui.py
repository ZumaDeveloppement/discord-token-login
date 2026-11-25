#!/usr/bin/env python3
"""
Discord Token Login — GUI violet + splash screen animé
"""

import sys
import time
import random
import math

try:
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QPushButton, QTextEdit, QFrame,
        QGraphicsDropShadowEffect, QDesktopWidget, QSplashScreen
    )
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QRect, QPointF
    from PyQt5.QtGui import (
        QFont, QColor, QPalette, QPainter, QBrush, QPen,
        QLinearGradient, QRadialGradient, QFontMetrics, QPixmap
    )
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5", "--quiet"])
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QPushButton, QTextEdit, QFrame,
        QGraphicsDropShadowEffect, QDesktopWidget, QSplashScreen
    )
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QRect, QPointF
    from PyQt5.QtGui import (
        QFont, QColor, QPalette, QPainter, QBrush, QPen,
        QLinearGradient, QRadialGradient, QFontMetrics, QPixmap
    )


# ─────────────────────────────────────────────
#  SPLASH SCREEN ANIMÉ
# ─────────────────────────────────────────────

CHARS = "DiscordABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*<>[]{}|/\\~^"

class MatrixColumn:
    def __init__(self, x, h, char_h):
        self.x = x
        self.h = h
        self.char_h = char_h
        self.y = random.uniform(-h, 0)
        self.speed = random.uniform(1.5, 4.5)
        self.length = random.randint(6, 20)
        self.chars = [random.choice(CHARS) for _ in range(self.length)]
        self.mutate_timer = 0

    def update(self):
        self.y += self.speed
        self.mutate_timer += 1
        if self.mutate_timer > 4:
            self.mutate_timer = 0
            idx = random.randint(0, self.length - 1)
            self.chars[idx] = random.choice(CHARS)
        if self.y - self.length * self.char_h > self.h:
            self.y = random.uniform(-self.h * 0.5, 0)
            self.speed = random.uniform(1.5, 4.5)
            self.length = random.randint(6, 20)
            self.chars = [random.choice(CHARS) for _ in range(self.length)]

    def draw(self, painter, font, char_w, char_h):
        for i, ch in enumerate(self.chars):
            cy = self.y - i * char_h
            if cy < 0 or cy > self.h:
                continue
            t = i / self.length
            if i == 0:
                r, g, b, a = 220, 180, 255, 255
            elif i < 3:
                r, g, b, a = 180, 100, 255, int(220 * (1 - t * 0.3))
            else:
                r, g, b, a = 100, 30, 180, int(160 * (1 - t))
            painter.setPen(QColor(r, g, b, a))
            painter.drawText(int(self.x), int(cy), ch)


class SplashWidget(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setFixedSize(520, 400)
        self._center()

        self.char_font = QFont("Consolas", 13, QFont.Bold)
        fm = QFontMetrics(self.char_font)
        self.char_w = fm.averageCharWidth()
        self.char_h = fm.height()

        cols = self.width() // self.char_w + 1
        self.columns = [MatrixColumn(i * self.char_w, self.height(), self.char_h)
                        for i in range(cols)]

        # stagger starts
        for col in self.columns:
            col.y = random.uniform(-self.height(), 0)

        self.frame = 0
        self.alpha = 0           # fade in
        self.fade_out = False
        self.fade_alpha = 255

        self.logo_chars = list("DiscordTokenLogin")
        self.logo_reveal = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)  # ~60fps

        # auto close after 3.2s
        QTimer.singleShot(3200, self._start_fade_out)

    def _center(self):
        s = QDesktopWidget().screenGeometry()
        self.move((s.width() - self.width()) // 2,
                  (s.height() - self.height()) // 2)

    def _tick(self):
        self.frame += 1

        # fade in
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 12)

        # logo reveal
        if self.frame % 4 == 0 and self.logo_reveal < len(self.logo_chars):
            self.logo_reveal += 1

        # fade out
        if self.fade_out:
            self.fade_alpha -= 14
            if self.fade_alpha <= 0:
                self.timer.stop()
                self.close()
                self.finished.emit()
                return

        for col in self.columns:
            col.update()

        self.update()

    def _start_fade_out(self):
        self.fade_out = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()

        # background
        bg = QLinearGradient(0, 0, 0, h)
        bg.setColorAt(0, QColor(8, 4, 20))
        bg.setColorAt(1, QColor(13, 5, 30))
        painter.fillRect(0, 0, w, h, bg)

        # matrix columns
        painter.setFont(self.char_font)
        painter.setOpacity(self.alpha / 255 * 0.85)
        for col in self.columns:
            col.draw(painter, self.char_font, self.char_w, self.char_h)
        painter.setOpacity(1.0)

        # center glow
        cx, cy = w // 2, h // 2
        glow = QRadialGradient(cx, cy, 180)
        glow.setColorAt(0, QColor(120, 40, 220, 60))
        glow.setColorAt(0.5, QColor(80, 20, 160, 30))
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, w, h, glow)

        # border glow
        pen = QPen(QColor(140, 60, 240, 180), 2)
        painter.setPen(pen)
        painter.drawRoundedRect(2, 2, w - 4, h - 4, 12, 12)
        inner_pen = QPen(QColor(80, 20, 160, 80), 1)
        painter.setPen(inner_pen)
        painter.drawRoundedRect(5, 5, w - 10, h - 10, 10, 10)

        # ◈ logo icon
        icon_font = QFont("Segoe UI", 38, QFont.Bold)
        painter.setFont(icon_font)
        pulse = 180 + int(60 * math.sin(self.frame * 0.07))
        painter.setPen(QColor(pulse, 80, 255, 230))
        painter.drawText(QRect(0, cy - 110, w, 60), Qt.AlignCenter, "◈")

        # animated logo text — reveal char by char
        logo_font = QFont("Segoe UI", 22, QFont.Bold)
        painter.setFont(logo_font)
        revealed = "".join(self.logo_chars[:self.logo_reveal])
        # scramble unrevealed part
        scramble_len = len(self.logo_chars) - self.logo_reveal
        scramble = "".join(random.choice(CHARS) for _ in range(scramble_len))
        full = revealed + scramble

        fm2 = QFontMetrics(logo_font)
        tw = fm2.horizontalAdvance(full)
        tx = (w - tw) // 2
        ty = cy - 38

        for i, ch in enumerate(full):
            if i < self.logo_reveal:
                painter.setPen(QColor(210, 160, 255, 240))
            else:
                painter.setPen(QColor(80, 30, 120,
                                      random.randint(60, 140)))
            painter.drawText(tx + fm2.horizontalAdvance(full[:i]), ty, ch)

        # subtitle
        sub_font = QFont("Segoe UI", 10)
        painter.setFont(sub_font)
        painter.setPen(QColor(100, 60, 160, 200))
        painter.drawText(QRect(0, cy - 10, w, 30), Qt.AlignCenter,
                         "Token Injector  •  by GenZ  •  2026")

        # loading bar
        bar_w = 300
        bar_h = 4
        bar_x = (w - bar_w) // 2
        bar_y = cy + 30

        # track
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(30, 10, 60))
        painter.drawRoundedRect(bar_x, bar_y, bar_w, bar_h, 2, 2)

        # fill — progress based on frame / ~190 frames (3.2s @ 60fps)
        progress = min(1.0, self.frame / 192)
        fill_w = int(bar_w * progress)
        if fill_w > 0:
            grad = QLinearGradient(bar_x, 0, bar_x + fill_w, 0)
            grad.setColorAt(0, QColor(100, 20, 200))
            grad.setColorAt(1, QColor(200, 100, 255))
            painter.setBrush(grad)
            painter.drawRoundedRect(bar_x, bar_y, fill_w, bar_h, 2, 2)

        # loading label
        dots = "." * (1 + (self.frame // 20) % 3)
        label_font = QFont("Consolas", 9)
        painter.setFont(label_font)
        painter.setPen(QColor(120, 60, 200, 180))
        painter.drawText(QRect(0, bar_y + 14, w, 20), Qt.AlignCenter,
                         f"Initialisation{dots}")

        # corner tags
        corner_font = QFont("Consolas", 8)
        painter.setFont(corner_font)
        painter.setPen(QColor(60, 20, 100, 150))
        painter.drawText(10, 20, "[ GenZ.TokenLogin.v2 ]")
        painter.drawText(10, h - 10, f"frame:{self.frame:04d}")

        # fade overlay
        if self.fade_out and self.fade_alpha < 255:
            painter.fillRect(0, 0, w, h,
                             QColor(8, 4, 20, 255 - self.fade_alpha))

        painter.end()


# ─────────────────────────────────────────────
#  STYLES MAIN WINDOW
# ─────────────────────────────────────────────

STYLE = """
QWidget#MainWindow {
    background-color: #0d0d1a;
}
QWidget {
    background-color: transparent;
    color: #e0d0ff;
    font-family: 'Segoe UI', Arial;
}
QFrame#Card {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1a0d2e, stop:1 #0d0d1a);
    border: 1px solid #3d1f6b;
    border-radius: 16px;
}
QLineEdit#TokenInput {
    background: #12082a;
    border: 2px solid #4a1f8a;
    border-radius: 10px;
    padding: 12px 16px;
    color: #c8a8ff;
    font-size: 13px;
    font-family: 'Consolas', monospace;
    selection-background-color: #6b2fa0;
}
QLineEdit#TokenInput:focus {
    border: 2px solid #9b59f5;
    background: #160a30;
}
QPushButton#LoginBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7b2ff7, stop:1 #4a1f8a);
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 15px;
    font-weight: bold;
    padding: 14px;
    letter-spacing: 1px;
}
QPushButton#LoginBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #9b3fff, stop:1 #6b2fa0);
}
QPushButton#LoginBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b1fd7, stop:1 #3a0f7a);
}
QPushButton#LoginBtn:disabled {
    background: #2a1a3a;
    color: #6b5a8a;
}
QPushButton#ClearBtn {
    background: transparent;
    border: 1px solid #3d1f6b;
    border-radius: 8px;
    color: #8b6aaa;
    font-size: 12px;
    padding: 8px 16px;
}
QPushButton#ClearBtn:hover {
    border-color: #7b2ff7;
    color: #c8a8ff;
    background: #1a0d2e;
}
QTextEdit#LogBox {
    background: #0a0618;
    border: 1px solid #2a1a3a;
    border-radius: 10px;
    color: #a888dd;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    padding: 10px;
}
QScrollBar:vertical {
    background: #0a0618;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #4a1f8a;
    border-radius: 3px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""


# ─────────────────────────────────────────────
#  LOGIN WORKER
# ─────────────────────────────────────────────

class LoginWorker(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(bool)

    def __init__(self, token):
        super().__init__()
        self.token = token

    def log(self, msg):
        self.log_signal.emit(msg)

    def run(self):
        try:
            self.log("⚡ Installation des dépendances...")
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install",
                           "undetected-chromedriver", "selenium", "--quiet"],
                          capture_output=True)

            self.log("🚀 Lancement de Chrome...")
            import undetected_chromedriver as uc

            opts = uc.ChromeOptions()
            opts.add_argument("--start-maximized")
            opts.add_argument("--disable-blink-features=AutomationControlled")

            driver = uc.Chrome(options=opts, use_subprocess=True)

            self.log("🌐 Ouverture de discord.com...")
            driver.get("https://discord.com/login")
            time.sleep(3)

            self.log("💉 Injection du token...")
            js_inject = """
            function setToken(token) {
                try { localStorage.setItem('token', JSON.stringify(token)); } catch(e) {}
                try {
                    webpackChunkdiscord_app.push([['x'],{},e=>{
                        for(const k in e.c){
                            const m=e.c[k];
                            if(m?.exports?.default?.login){m.exports.default.login(token);return;}
                            if(m?.exports?.Z?.login){m.exports.Z.login(token);return;}
                        }
                    }]);
                } catch(e) {}
                return true;
            }
            return setToken(arguments[0]);
            """
            driver.execute_script(js_inject, self.token)
            time.sleep(1)

            self.log("🔄 Redirection Discord...")
            driver.get("https://discord.com/channels/@me")
            time.sleep(4)

            if "channels" in driver.current_url or "@me" in driver.current_url:
                self.log("✅ CONNECTÉ avec succès !")
                self.log("🎉 Chrome ouvert sur ton compte.")
                self.done_signal.emit(True)
            else:
                self.log("⚠️  Méthode 2...")
                driver.get("https://discord.com/login")
                time.sleep(2)
                js2 = """
                (function(){
                    const t=arguments[0];
                    try{localStorage.setItem('token',JSON.stringify(t));}catch(e){}
                    self['webpackChunkdiscord_app']=self['webpackChunkdiscord_app']||[];
                    self['webpackChunkdiscord_app'].push([[Math.random()],{},function(e){
                        for(let r in e.c){
                            try{
                                const x=e.c[r].exports;
                                if(x?.Z?.login){x.Z.login(t);return;}
                                if(x?.default?.login){x.default.login(t);return;}
                            }catch(err){}
                        }
                    }]);
                })(arguments[0]);
                return true;
                """
                driver.execute_script(js2, self.token)
                time.sleep(1)
                driver.get("https://discord.com/channels/@me")
                time.sleep(4)

                if "channels" in driver.current_url:
                    self.log("✅ CONNECTÉ (méthode 2) !")
                    self.done_signal.emit(True)
                else:
                    self.log("❌ Token invalide ou expiré.")
                    driver.quit()
                    self.done_signal.emit(False)

        except Exception as e:
            self.log(f"❌ Erreur : {str(e)}")
            self.done_signal.emit(False)


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Discord Token Login")
        self.setFixedSize(520, 580)
        self.setStyleSheet(STYLE)
        self.worker = None
        self._build_ui()
        s = QDesktopWidget().screenGeometry()
        self.move((s.width() - self.width()) // 2,
                  (s.height() - self.height()) // 2)

    def _shadow(self, widget, radius=20, color="#7b2ff7"):
        s = QGraphicsDropShadowEffect()
        s.setBlurRadius(radius)
        s.setOffset(0, 0)
        s.setColor(QColor(color))
        widget.setGraphicsEffect(s)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # HEADER
        header = QFrame()
        header.setObjectName("Card")
        hlay = QVBoxLayout(header)
        hlay.setContentsMargins(24, 20, 24, 20)
        hlay.setSpacing(6)

        logo_row = QHBoxLayout()
        disc_icon = QLabel("◈")
        disc_icon.setFont(QFont("Segoe UI", 28))
        disc_icon.setStyleSheet("color: #9b59f5;")
        logo_row.addWidget(disc_icon)

        title_col = QVBoxLayout()
        title = QLabel("Discord Token Login")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #c8a8ff; letter-spacing: 1px;")
        sub = QLabel("Connexion via token  •  by GenZ")
        sub.setFont(QFont("Segoe UI", 10))
        sub.setStyleSheet("color: #6b4a9a;")
        title_col.addWidget(title)
        title_col.addWidget(sub)
        logo_row.addLayout(title_col)
        logo_row.addStretch()

        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont("Segoe UI", 14))
        self.status_dot.setStyleSheet("color: #4a1f8a;")
        logo_row.addWidget(self.status_dot)
        hlay.addLayout(logo_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background: #2a1a3a; max-height: 1px;")
        hlay.addWidget(sep)

        self._shadow(header, 30, "#4a1f8a")
        root.addWidget(header)

        # TOKEN INPUT
        card = QFrame()
        card.setObjectName("Card")
        clay = QVBoxLayout(card)
        clay.setContentsMargins(24, 20, 24, 20)
        clay.setSpacing(12)

        lbl = QLabel("Token Discord")
        lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        lbl.setStyleSheet("color: #9b59f5;")
        clay.addWidget(lbl)

        self.token_input = QLineEdit()
        self.token_input.setObjectName("TokenInput")
        self.token_input.setPlaceholderText("Colle ton token ici...")
        self.token_input.setEchoMode(QLineEdit.Password)
        self.token_input.setMinimumHeight(46)
        clay.addWidget(self.token_input)

        toggle_row = QHBoxLayout()
        self.show_btn = QPushButton("👁 Afficher")
        self.show_btn.setObjectName("ClearBtn")
        self.show_btn.setFixedHeight(32)
        self._showing = False
        self.show_btn.clicked.connect(self._toggle_show)
        toggle_row.addWidget(self.show_btn)
        toggle_row.addStretch()
        clr = QPushButton("✕ Effacer")
        clr.setObjectName("ClearBtn")
        clr.setFixedHeight(32)
        clr.clicked.connect(self.token_input.clear)
        toggle_row.addWidget(clr)
        clay.addLayout(toggle_row)

        self.login_btn = QPushButton("⚡  Se connecter")
        self.login_btn.setObjectName("LoginBtn")
        self.login_btn.setMinimumHeight(50)
        self.login_btn.clicked.connect(self._on_login)
        self._shadow(self.login_btn, 20, "#7b2ff7")
        clay.addWidget(self.login_btn)

        self._shadow(card, 25, "#3d1f6b")
        root.addWidget(card)

        # LOG
        log_card = QFrame()
        log_card.setObjectName("Card")
        llay = QVBoxLayout(log_card)
        llay.setContentsMargins(16, 12, 16, 12)
        llay.setSpacing(8)

        lh = QHBoxLayout()
        ll = QLabel("Console")
        ll.setFont(QFont("Segoe UI", 10, QFont.Bold))
        ll.setStyleSheet("color: #6b4a9a;")
        lh.addWidget(ll)
        lh.addStretch()
        clrl = QPushButton("Effacer")
        clrl.setObjectName("ClearBtn")
        clrl.setFixedHeight(26)
        clrl.clicked.connect(lambda: self.log_box.clear())
        lh.addWidget(clrl)
        llay.addLayout(lh)

        self.log_box = QTextEdit()
        self.log_box.setObjectName("LogBox")
        self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(140)
        self.log_box.setMaximumHeight(200)
        self.log_append("▶  Prêt. Colle ton token et clique Connecter.")
        llay.addWidget(self.log_box)
        root.addWidget(log_card)

        footer = QLabel("discord.com  •  Token injecté via webpack JS  •  GenZ 2026")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFont(QFont("Segoe UI", 9))
        footer.setStyleSheet("color: #3d2a5a;")
        root.addWidget(footer)

    def _toggle_show(self):
        self._showing = not self._showing
        self.token_input.setEchoMode(
            QLineEdit.Normal if self._showing else QLineEdit.Password)
        self.show_btn.setText("🙈 Masquer" if self._showing else "👁 Afficher")

    def log_append(self, msg):
        self.log_box.append(f"<span style='color:#a888dd'>{msg}</span>")
        self.log_box.verticalScrollBar().setValue(
            self.log_box.verticalScrollBar().maximum())

    def _on_login(self):
        token = self.token_input.text().strip()
        if not token:
            self.log_append("⚠️  Token vide !")
            return
        self.login_btn.setEnabled(False)
        self.login_btn.setText("⏳  Connexion en cours...")
        self.status_dot.setStyleSheet("color: #f5a623;")
        self.worker = LoginWorker(token)
        self.worker.log_signal.connect(self.log_append)
        self.worker.done_signal.connect(self._on_done)
        self.worker.start()

    def _on_done(self, success):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("⚡  Se connecter")
        if success:
            self.status_dot.setStyleSheet("color: #57f287;")
            self.log_append("─────────────────────────")
            self.log_append("✅  Chrome ouvert avec ton compte.")
        else:
            self.status_dot.setStyleSheet("color: #ed4245;")
            self.log_append("─────────────────────────")
            self.log_append("❌  Échec. Vérifie ton token.")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0d0d1a"))
    palette.setColor(QPalette.WindowText, QColor("#e0d0ff"))
    app.setPalette(palette)

    # Splash animé — s'affiche 3.2s puis ouvre la main window
    splash = SplashWidget()
    splash.show()

    main_win = MainWindow()

    def on_splash_done():
        main_win.show()

    splash.finished.connect(on_splash_done)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
