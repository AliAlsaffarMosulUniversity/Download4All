"""Jazira Download Manager (JDM) - free, open download manager. No license, no activation."""
import datetime
import json
import os
import subprocess
import sys

from PySide6.QtCore import QSize, Qt, QTime, QTimer, QUrl
from PySide6.QtGui import QAction, QDesktopServices, QGuiApplication, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox,
    QFileDialog, QFormLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMessageBox, QProgressBar, QPushButton, QSpinBox,
    QStyle, QSystemTrayIcon, QTableWidget, QTableWidgetItem, QTimeEdit, QToolBar,
    QVBoxLayout, QWidget)

import bridge
import engine as E

APP_NAME = "Jazira Download Manager"
VERSION = "1.0.0"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ---------------------------------------------------------------- paths & settings
def data_dir():
    base = os.environ.get("APPDATA") or os.path.join(os.path.expanduser("~"), ".config")
    p = os.path.join(base, "JDM")
    os.makedirs(p, exist_ok=True)
    return p


def resource(rel):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, rel)


DEFAULTS = {
    "download_dir": os.path.join(os.path.expanduser("~"), "Downloads"),
    "connections": 8,
    "max_concurrent": 3,
    "speed_limit_kb": 0,
    "ask_on_browser_download": True,
    "notify_on_complete": True,
    "close_to_tray": True,
    "scheduler": {"enabled": False, "start": "02:00", "stop_enabled": False,
                  "stop": "08:00", "days": [0, 1, 2, 3, 4, 5, 6]},
}


def load_settings():
    s = json.loads(json.dumps(DEFAULTS))
    try:
        with open(os.path.join(data_dir(), "settings.json"), encoding="utf-8") as f:
            user = json.load(f)
        sched = {**s["scheduler"], **user.get("scheduler", {})}
        s.update(user)
        s["scheduler"] = sched
    except (OSError, ValueError):
        pass
    return s


def save_settings(s):
    with open(os.path.join(data_dir(), "settings.json"), "w", encoding="utf-8") as f:
        json.dump(s, f, indent=1, ensure_ascii=False)


def open_path(path):
    if sys.platform.startswith("win"):
        os.startfile(path)  # noqa
    else:
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))


def show_in_folder(path):
    if sys.platform.startswith("win") and os.path.exists(path):
        subprocess.Popen(["explorer", "/select,", os.path.normpath(path)])
    else:
        open_path(os.path.dirname(path))


# ---------------------------------------------------------------- dialogs
class AddDialog(QDialog):
    def __init__(self, parent, settings, url="", filename=""):
        super().__init__(parent)
        self.setWindowTitle("Add Download")
        self.setMinimumWidth(560)
        self.url = QLineEdit(url)
        self.url.setPlaceholderText("https://example.com/file.zip")
        self.name = QLineEdit(filename)
        self.name.setPlaceholderText("Automatic (from server)")
        self.folder = QLineEdit(settings["download_dir"])
        browse = QPushButton("Browse…")
        browse.clicked.connect(self._browse)
        row = QHBoxLayout()
        row.addWidget(self.folder)
        row.addWidget(browse)
        self.conn = QSpinBox()
        self.conn.setRange(1, 32)
        self.conn.setValue(int(settings["connections"]))
        form = QFormLayout()
        form.addRow("URL:", self.url)
        form.addRow("File name:", self.name)
        form.addRow("Save to:", row)
        form.addRow("Connections:", self.conn)
        self.choice = None
        now = QPushButton("Download Now")
        now.setDefault(True)
        later = QPushButton("Add to Schedule")
        paused = QPushButton("Add Paused")
        cancel = QPushButton("Cancel")
        now.clicked.connect(lambda: self._done(E.QUEUED))
        later.clicked.connect(lambda: self._done(E.SCHEDULED))
        paused.clicked.connect(lambda: self._done(E.PAUSED))
        cancel.clicked.connect(self.reject)
        btns = QHBoxLayout()
        btns.addStretch()
        for b in (now, later, paused, cancel):
            btns.addWidget(b)
        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addLayout(btns)

    def _browse(self):
        d = QFileDialog.getExistingDirectory(self, "Save to", self.folder.text())
        if d:
            self.folder.setText(d)

    def _done(self, status):
        u = self.url.text().strip()
        if not u.lower().startswith(("http://", "https://")):
            QMessageBox.warning(self, APP_NAME, "Please enter a valid http:// or https:// URL.")
            return
        self.choice = status
        self.accept()


class SettingsDialog(QDialog):
    def __init__(self, parent, s):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(480)
        self.s = s
        self.folder = QLineEdit(s["download_dir"])
        b = QPushButton("Browse…")
        b.clicked.connect(lambda: self.folder.setText(
            QFileDialog.getExistingDirectory(self, "Download folder", self.folder.text())
            or self.folder.text()))
        row = QHBoxLayout()
        row.addWidget(self.folder)
        row.addWidget(b)
        self.conn = QSpinBox()
        self.conn.setRange(1, 32)
        self.conn.setValue(int(s["connections"]))
        self.maxc = QSpinBox()
        self.maxc.setRange(1, 10)
        self.maxc.setValue(int(s["max_concurrent"]))
        self.limit = QSpinBox()
        self.limit.setRange(0, 1_000_000)
        self.limit.setSuffix(" KB/s")
        self.limit.setSpecialValueText("Unlimited")
        self.limit.setValue(int(s["speed_limit_kb"]))
        self.ask = QCheckBox("Show 'Add Download' window for browser downloads")
        self.ask.setChecked(bool(s["ask_on_browser_download"]))
        self.notify = QCheckBox("Notify when a download completes")
        self.notify.setChecked(bool(s["notify_on_complete"]))
        self.tray = QCheckBox("Closing the window keeps JDM running in the tray")
        self.tray.setChecked(bool(s["close_to_tray"]))
        form = QFormLayout()
        form.addRow("Default folder:", row)
        form.addRow("Connections per file:", self.conn)
        form.addRow("Simultaneous downloads:", self.maxc)
        form.addRow("Speed limit:", self.limit)
        form.addRow(self.ask)
        form.addRow(self.notify)
        form.addRow(self.tray)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addWidget(bb)

    def apply(self):
        self.s["download_dir"] = self.folder.text().strip() or DEFAULTS["download_dir"]
        self.s["connections"] = self.conn.value()
        self.s["max_concurrent"] = self.maxc.value()
        self.s["speed_limit_kb"] = self.limit.value()
        self.s["ask_on_browser_download"] = self.ask.isChecked()
        self.s["notify_on_complete"] = self.notify.isChecked()
        self.s["close_to_tray"] = self.tray.isChecked()


class SchedulerDialog(QDialog):
    def __init__(self, parent, sched):
        super().__init__(parent)
        self.setWindowTitle("Scheduler")
        self.sched = sched
        self.enabled = QCheckBox("Enable scheduler")
        self.enabled.setChecked(sched["enabled"])
        self.start = QTimeEdit(QTime.fromString(sched["start"], "HH:mm"))
        self.start.setDisplayFormat("HH:mm")
        self.stop_en = QCheckBox("Stop (pause) downloads at:")
        self.stop_en.setChecked(sched["stop_enabled"])
        self.stop = QTimeEdit(QTime.fromString(sched["stop"], "HH:mm"))
        self.stop.setDisplayFormat("HH:mm")
        days = QHBoxLayout()
        self.day_boxes = []
        for i, n in enumerate(DAYS):
            c = QCheckBox(n)
            c.setChecked(i in sched["days"])
            self.day_boxes.append(c)
            days.addWidget(c)
        grp = QGroupBox("Downloads marked 'Scheduled' start automatically")
        form = QFormLayout(grp)
        form.addRow("Start at:", self.start)
        form.addRow(self.stop_en, self.stop)
        form.addRow("Days:", days)
        hint = QLabel("Tip: right-click a download → 'Move to Schedule'.")
        hint.setStyleSheet("color: gray")
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        lay = QVBoxLayout(self)
        lay.addWidget(self.enabled)
        lay.addWidget(grp)
        lay.addWidget(hint)
        lay.addWidget(bb)

    def apply(self):
        self.sched["enabled"] = self.enabled.isChecked()
        self.sched["start"] = self.start.time().toString("HH:mm")
        self.sched["stop_enabled"] = self.stop_en.isChecked()
        self.sched["stop"] = self.stop.time().toString("HH:mm")
        self.sched["days"] = [i for i, c in enumerate(self.day_boxes) if c.isChecked()]


# ---------------------------------------------------------------- main window
COLS = ["File Name", "Size", "Progress", "Speed", "Time Left", "Status", "Connections", "Added"]


class MainWindow(QMainWindow):
    def __init__(self, settings, start_hidden=False):
        super().__init__()
        self.settings = settings
        self.engine = E.Engine(data_dir(), settings)
        self.icon = QIcon(resource(os.path.join("assets", "jdm.ico")))
        self.setWindowIcon(self.icon)
        self.setWindowTitle(f"{APP_NAME} {VERSION}")
        self.resize(1050, 560)
        self._rows = []                    # download ids in table order
        self._last_status = {}
        self._fired = {}                   # scheduler: event -> date string
        self._quitting = False

        self._build_toolbar()
        self._build_table()
        self._build_tray()
        self.speed_label = QLabel()
        self.limit_label = QLabel()
        self.statusBar().addPermanentWidget(self.limit_label)
        self.statusBar().addPermanentWidget(self.speed_label)

        self.server = bridge.start_server()
        if self.server is None:
            self.statusBar().showMessage("Browser bridge port is busy – browser capture disabled.")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(500)
        self._refresh(full=True)
        if not start_hidden:
            self.show()

    # ---- ui construction
    def _build_toolbar(self):
        tb = QToolBar("Main")
        tb.setIconSize(QSize(28, 28))
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb.setMovable(False)
        self.addToolBar(tb)
        st = self.style()

        def act(text, icon, slot, shortcut=None):
            a = QAction(st.standardIcon(icon), text, self)
            a.triggered.connect(slot)
            if shortcut:
                a.setShortcut(QKeySequence(shortcut))
            tb.addAction(a)
            return a

        act("Add URL", QStyle.SP_FileDialogNewFolder, self.add_dialog, "Ctrl+N")
        act("Resume", QStyle.SP_MediaPlay, self.resume_selected)
        act("Pause", QStyle.SP_MediaPause, self.pause_selected)
        act("Pause All", QStyle.SP_MediaStop, lambda: self.engine.stop_all())
        act("Delete", QStyle.SP_TrashIcon, self.delete_selected, "Del")
        tb.addSeparator()
        act("Scheduler", QStyle.SP_BrowserReload, self.scheduler_dialog)
        act("Settings", QStyle.SP_FileDialogDetailedView, self.settings_dialog)
        act("Open Folder", QStyle.SP_DirOpenIcon,
            lambda: open_path(self.settings["download_dir"]))
        tb.addSeparator()
        act("About", QStyle.SP_MessageBoxInformation, self.about)

    def _build_table(self):
        t = QTableWidget(0, len(COLS))
        t.setHorizontalHeaderLabels(COLS)
        t.setSelectionBehavior(QAbstractItemView.SelectRows)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.verticalHeader().setVisible(False)
        t.setAlternatingRowColors(True)
        t.setContextMenuPolicy(Qt.CustomContextMenu)
        t.customContextMenuRequested.connect(self._context_menu)
        t.doubleClicked.connect(self._double_click)
        h = t.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Stretch)
        for i, w in enumerate([0, 95, 170, 95, 85, 95, 90, 130]):
            if w:
                t.setColumnWidth(i, w)
        self.table = t
        self.setCentralWidget(t)

    def _build_tray(self):
        self.tray = QSystemTrayIcon(self.icon, self)
        m = QMenu()
        m.addAction("Show JDM", self.show_normal)
        m.addAction("Add URL…", self.add_dialog)
        m.addAction("Pause All", lambda: self.engine.stop_all())
        m.addSeparator()
        m.addAction("Exit", self.quit)
        self.tray.setContextMenu(m)
        self.tray.setToolTip(APP_NAME)
        self.tray.activated.connect(
            lambda r: self.show_normal() if r in (QSystemTrayIcon.Trigger,
                                                  QSystemTrayIcon.DoubleClick) else None)
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray.show()

    # ---- helpers
    def show_normal(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
        self.raise_()
        self.activateWindow()

    def selected(self):
        ids = {self._rows[i.row()] for i in self.table.selectionModel().selectedRows()
               if i.row() < len(self._rows)}
        return [d for d in self.engine.downloads if d.id in ids]

    # ---- actions
    def add_dialog(self, url="", filename="", headers=None, from_browser=False):
        if not url:
            clip = QGuiApplication.clipboard().text().strip()
            if clip.lower().startswith(("http://", "https://")) and " " not in clip:
                url = clip
        if from_browser and not self.settings["ask_on_browser_download"]:
            self.engine.add(url, filename=filename or None, headers=headers)
            self.tray.showMessage(APP_NAME, f"Download added:\n{filename or url}",
                                  QSystemTrayIcon.Information, 3000)
            return
        self.show_normal()
        dlg = AddDialog(self, self.settings, url, filename)
        dlg.setWindowFlag(Qt.WindowStaysOnTopHint, from_browser)
        if dlg.exec() == QDialog.Accepted:
            self.engine.add(dlg.url.text().strip(), dlg.folder.text().strip(),
                            dlg.name.text().strip() or None, dlg.conn.value(), headers,
                            status=dlg.choice)
            self._refresh(full=True)

    def resume_selected(self):
        for d in self.selected():
            self.engine.resume(d)

    def pause_selected(self):
        for d in self.selected():
            self.engine.pause(d)

    def schedule_selected(self):
        for d in self.selected():
            if d.status != E.COMPLETED:
                d.stop(E.SCHEDULED)
                d.status = E.SCHEDULED
        self.engine.request_save()

    def delete_selected(self):
        items = self.selected()
        if not items:
            return
        box = QMessageBox(self)
        box.setWindowTitle("Delete")
        box.setText(f"Remove {len(items)} download(s) from the list?")
        also = QCheckBox("Also delete the file(s) from disk")
        box.setCheckBox(also)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if box.exec() == QMessageBox.Yes:
            for d in items:
                self.engine.remove(d, also.isChecked())
            self._refresh(full=True)

    def settings_dialog(self):
        dlg = SettingsDialog(self, self.settings)
        if dlg.exec() == QDialog.Accepted:
            dlg.apply()
            self.engine.set_speed_limit_kb(self.settings["speed_limit_kb"])
            save_settings(self.settings)

    def scheduler_dialog(self):
        dlg = SchedulerDialog(self, self.settings["scheduler"])
        if dlg.exec() == QDialog.Accepted:
            dlg.apply()
            save_settings(self.settings)

    def about(self):
        QMessageBox.about(self, "About", f"<b>{APP_NAME}</b> {VERSION}<br><br>"
                          "Free download manager – no serial, no activation.<br>"
                          "Multi-connection downloads, pause/resume, scheduler, "
                          "speed limiter and browser capture.")

    def _context_menu(self, pos):
        items = self.selected()
        if not items:
            return
        d = items[0]
        m = QMenu(self)
        if d.status == E.COMPLETED:
            m.addAction("Open", lambda: open_path(d.path))
            m.addAction("Open Folder", lambda: show_in_folder(d.path))
            m.addAction("Download Again", lambda: self.engine.redownload(d))
        else:
            m.addAction("Resume", self.resume_selected)
            m.addAction("Pause", self.pause_selected)
            m.addAction("Move to Schedule", self.schedule_selected)
            m.addAction("Open Folder", lambda: open_path(d.save_dir))
        m.addAction("Copy URL", lambda: QGuiApplication.clipboard().setText(d.url))
        if d.error:
            m.addAction("Show Error", lambda: QMessageBox.warning(self, "Error", d.error))
        m.addSeparator()
        m.addAction("Delete", self.delete_selected)
        m.exec(self.table.viewport().mapToGlobal(pos))

    def _double_click(self, index):
        if index.row() < len(self._rows):
            d = self.engine.get(self._rows[index.row()])
            if d and d.status == E.COMPLETED and os.path.exists(d.path):
                open_path(d.path)
            elif d and d.status in (E.PAUSED, E.ERROR):
                self.engine.resume(d)

    # ---- periodic work
    def _tick(self):
        # browser / second-instance events
        while not bridge.events.empty():
            kind, data = bridge.events.get_nowait()
            if kind == "show":
                self.show_normal()
            elif kind == "add":
                headers = {}
                if data.get("referrer"):
                    headers["Referer"] = data["referrer"]
                if data.get("cookies"):
                    headers["Cookie"] = data["cookies"]
                if data.get("userAgent"):
                    headers["User-Agent"] = data["userAgent"]
                self.add_dialog(data["url"], data.get("filename", ""), headers, from_browser=True)
        self._scheduler()
        self.engine.tick()
        self._refresh()

    def _scheduler(self):
        sc = self.settings["scheduler"]
        if not sc["enabled"]:
            return
        now = datetime.datetime.now()
        if now.weekday() not in sc["days"]:
            return
        hm, today = now.strftime("%H:%M"), now.strftime("%Y-%m-%d")
        if hm == sc["start"] and self._fired.get("start") != today:
            self._fired["start"] = today
            self.engine.start_scheduled()
            self.statusBar().showMessage("Scheduler: scheduled downloads started", 8000)
        if sc["stop_enabled"] and hm == sc["stop"] and self._fired.get("stop") != today:
            self._fired["stop"] = today
            for d in self.engine.downloads:
                if d.status in (E.DOWNLOADING, E.QUEUED):
                    d.stop(E.SCHEDULED)
            self.engine.request_save()
            self.statusBar().showMessage("Scheduler: downloads stopped", 8000)

    def _refresh(self, full=False):
        items = list(self.engine.downloads)
        ids = [d.id for d in items]
        if full or ids != self._rows:
            sel = {d.id for d in self.selected()} if self._rows else set()
            self.table.setRowCount(len(items))
            for r, d in enumerate(items):
                for c in range(len(COLS)):
                    if c == 2:
                        bar = QProgressBar()
                        bar.setRange(0, 1000)
                        bar.setTextVisible(True)
                        bar.setAlignment(Qt.AlignCenter)
                        self.table.setCellWidget(r, c, bar)
                    else:
                        it = QTableWidgetItem()
                        if c in (1, 3, 4, 6):
                            it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.table.setItem(r, c, it)
            self._rows = ids
            for r, i in enumerate(ids):
                if i in sel:
                    self.table.selectRow(r)
        st = self.style()
        for r, d in enumerate(items):
            running = d.status == E.DOWNLOADING
            icon = {E.COMPLETED: QStyle.SP_DialogApplyButton, E.ERROR: QStyle.SP_MessageBoxCritical,
                    E.PAUSED: QStyle.SP_MediaPause, E.DOWNLOADING: QStyle.SP_ArrowDown,
                    E.SCHEDULED: QStyle.SP_BrowserReload}.get(d.status, QStyle.SP_FileIcon)
            it = self.table.item(r, 0)
            it.setText(d.filename)
            it.setIcon(st.standardIcon(icon))
            it.setToolTip(d.url + (f"\n\nError: {d.error}" if d.error else ""))
            self.table.item(r, 1).setText(E.human_size(d.size))
            bar = self.table.cellWidget(r, 2)
            p = d.progress()
            bar.setValue(int(p * 10))
            bar.setFormat(f"{p:.1f}%" if d.size > 0 else E.human_size(d.downloaded))
            self.table.item(r, 3).setText(E.human_size(d.speed) + "/s" if running else "")
            self.table.item(r, 4).setText(E.human_time(d.eta()) if running else "")
            self.table.item(r, 5).setText(d.status)
            self.table.item(r, 6).setText(str(d.live_connections) if running else "")
            self.table.item(r, 7).setText(
                datetime.datetime.fromtimestamp(d.added).strftime("%Y-%m-%d %H:%M"))
            # completion notification
            prev = self._last_status.get(d.id)
            if prev and prev != E.COMPLETED and d.status == E.COMPLETED \
                    and self.settings["notify_on_complete"]:
                self.tray.showMessage("Download complete", d.filename,
                                      QSystemTrayIcon.Information, 4000)
            self._last_status[d.id] = d.status
        total = self.engine.total_speed()
        active = sum(1 for d in items if d.status == E.DOWNLOADING)
        self.speed_label.setText(f"  {active} active  |  {E.human_size(total)}/s  ")
        lim = self.settings["speed_limit_kb"]
        self.limit_label.setText(f"Limit: {lim} KB/s" if lim else "No speed limit")

    # ---- window lifecycle
    def closeEvent(self, ev):
        if not self._quitting and self.settings["close_to_tray"] and \
                QSystemTrayIcon.isSystemTrayAvailable():
            ev.ignore()
            self.hide()
            if not self.settings.get("_tray_hint_shown"):
                self.settings["_tray_hint_shown"] = True
                save_settings(self.settings)
                self.tray.showMessage(APP_NAME, "JDM is still running in the tray.",
                                      QSystemTrayIcon.Information, 3000)
            return
        self._shutdown()
        ev.accept()
        QApplication.quit()

    def quit(self):
        self._quitting = True
        self.close()

    def _shutdown(self):
        self.timer.stop()
        self.engine.shutdown()
        if self.server:
            self.server.shutdown()
        self.tray.hide()


def main():
    args = sys.argv[1:]
    url = next((a for a in args if a.lower().startswith(("http://", "https://"))), None)
    if bridge.signal_running_instance(url=url):
        return 0                                      # already running -> it shows itself
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Fusion")
    settings = load_settings()
    w = MainWindow(settings, start_hidden="--minimized" in args)
    if url:
        QTimer.singleShot(300, lambda: w.add_dialog(url))
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
