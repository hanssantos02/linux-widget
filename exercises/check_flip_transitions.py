"""State regression checks added by the mentor at the learner's request.

Run from the project root: python -m exercises.check_flip_transitions
Loads the actual FlipCharacter.qml offscreen; it does not assess rendered appearance.
"""
import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")

from PySide6.QtCore import QElapsedTimer, QObject, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QTest


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def wait_until(predicate, message, timeout_ms=4000):
    elapsed = QElapsedTimer()
    elapsed.start()
    while not predicate():
        require(elapsed.elapsed() < timeout_ms, message)
        QTest.qWait(10)


def run_case(name, actions, expected_values, expected_captures):
    view = QQuickView()
    view.setInitialProperties({"character": "3"})
    view.setSource(QUrl.fromLocalFile(str(Path(__file__).resolve().parents[1] / "FlipCharacter.qml")))
    require(view.status() == QQuickView.Status.Ready, str(view.errors()))
    tile = view.rootObject()
    animations = [obj for obj in tile.findChildren(QObject)
                  if "SequentialAnimation" in obj.metaObject().className()]
    require(len(animations) == 1, "Expected one outer fold sequence")
    fold = animations[0]
    values = [tile.property("displayedCharacter")]
    captures = []
    tile.displayedCharacterChanged.connect(lambda: values.append(tile.property("displayedCharacter")))
    fold.started.connect(lambda: captures.append(tile.property("transitionCharacter")))
    view.show()
    try:
        QTest.qWait(50)
        require(tile.property("initialized") is True, "Startup gate not opened")
        require(tile.property("character") == "3" and values == ["3"], "Startup must settle at 3")
        require(tile.property("transitionCharacter") == "3", "Startup capture must be 3")
        require(not fold.property("running"), "Startup must not animate")

        def request(value):
            require(tile.setProperty("character", value), "Cannot change tile input")

        def settle():
            wait_until(lambda: not fold.property("running")
                       and tile.property("displayedCharacter") == tile.property("character"),
                       f"{name}: did not catch up to the latest request")
            QTest.qWait(100)

        actions(request, settle, tile, fold)
        settle()
        # Observe beyond one whole normal fold to detect unwanted replay.
        QTest.qWait(1000)
        require(values == expected_values, f"{name}: settled history {values}")
        require(captures == expected_captures, f"{name}: capture history {captures}")
        require(not fold.property("running"), f"{name}: unexpectedly still running")
        print(f"PASS {name}: settled {' -> '.join(values)}; captures {captures}")
    finally:
        view.close()
        view.deleteLater()
        QTest.qWait(20)


def startup(request, settle, tile, fold):
    pass


def idle_round_trip(request, settle, tile, fold):
    request("4")
    settle()
    request("3")


def busy_reversal(request, settle, tile, fold):
    request("4")
    QTest.qWait(100)
    require(fold.property("running"), "Reversal request missed the busy window")
    request("3")
    require(tile.property("transitionCharacter") == "4", "Busy request changed the captured glyph")


def latest_wins(request, settle, tile, fold):
    request("4")
    QTest.qWait(100)
    require(fold.property("running"), "First busy request missed the fold")
    request("3")
    QTest.qWait(100)
    require(fold.property("running"), "Second busy request missed the fold")
    request("4")
    require(tile.property("transitionCharacter") == "4", "Capture changed during the fold")


if __name__ == "__main__":
    app = QGuiApplication([])
    run_case("startup", startup, ["3"], [])
    run_case("idle round trip", idle_round_trip, ["3", "4", "3"], ["4", "3"])
    run_case("busy reversal", busy_reversal, ["3", "4", "3"], ["4", "3"])
    run_case("latest request wins", latest_wins, ["3", "4"], ["4"])
    print("All four flip-state checks passed (offscreen; visual motion not assessed).")
