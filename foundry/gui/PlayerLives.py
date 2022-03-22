from xmlrpc.client import Boolean
from PySide6.QtGui import QPixmap, Qt, QIntValidator
from PySide6.QtWidgets import QBoxLayout, QLabel, QDialogButtonBox, QLineEdit, QGridLayout, QCheckBox

from foundry.smb3parse.util.rom import Rom
from foundry.game.File import ROM
from foundry.gui.CustomDialog import CustomDialog
from foundry.gui.HorizontalLine import HorizontalLine
from foundry.smb3parse.util.code_edit_area import CodeEditArea
from dataclasses import dataclass
import copy
from foundry.core.ReduxStore import ReduxStore, Action

DEATH_TAKES_LIVES_VANILLA = bytearray([0xDE, 0x36, 0x07])
DEATH_TAKES_LIVES_INFINATE = bytearray([0xEA, 0xEA, 0xEA])

@dataclass
class UIStrings:
    title = "Player Lives"
    starting_lives = "Starting Lives"
    continue_lives = "Continue Lives"
    invalid_rom_warning = "The selected ROM has code modifications that are incompatible with one or more features of this window. The affected features are visible but disabled."
    death_takes_lives = "Subtract a life when the player dies"

@dataclass
class CodeEditAreas:
    starting_lives =    CodeEditArea(0x308E1, 1, bytearray([0xCA, 0x10, 0xF8, 0xA9]), bytearray([0x8D, 0x36, 0x07, 0x8D]))
    continue_lives =    CodeEditArea(0x3D2D6, 1, bytearray([0x08, 0xD0, 0x65, 0xA9]), bytearray([0x9D, 0x36, 0x07, 0xA5]))
    death_takes_lives = CodeEditArea(0x3D133, 3, bytearray([0x8B, 0x07, 0xD0, 0x05]), bytearray([0x30, 0x0b, 0xA9, 0x80]))

@dataclass
class ActionNames:
    load = "[PlayerLives] Load"
    starting_lives = "[PlayerLives] StartingLives"
    continue_lives = "[PlayerLives] ContinueLives"
    death_takes_lives = "[PlayerLives] DeathTakesLives"

ACTION_LOAD = Action(ActionNames.load, None)

@dataclass
class State:
    starting_lives: int
    starting_lives_area_valid: Boolean
    continue_lives: int
    continue_lives_area_valid: Boolean
    death_takes_lives: Boolean
    death_takes_lives_area_valid: Boolean

class Store(ReduxStore[State]):
    rom : Rom

    def __init__(self, rom: Rom):
        self.rom = rom
        self.state = Store.__loadStateFromRom(rom)

    def __loadStateFromRom(rom: Rom) -> State:
        return State(   
                        Store.__readCodeEditArea(rom, CodeEditAreas.starting_lives)[0],
                        CodeEditAreas.starting_lives.isValid(rom),
                        Store.__readCodeEditArea(rom, CodeEditAreas.continue_lives)[0],
                        CodeEditAreas.continue_lives.isValid(rom),
                        Store.__readCodeEditArea(rom, CodeEditAreas.death_takes_lives) == DEATH_TAKES_LIVES_VANILLA,
                        Store.__isDeathTakesLivesValid(rom)
                    )

    def __isDeathTakesLivesValid(rom: Rom) -> Boolean:
        code_area_data = Store.__readCodeEditArea(rom, CodeEditAreas.death_takes_lives)
        known_value = (code_area_data == DEATH_TAKES_LIVES_INFINATE) | (code_area_data == DEATH_TAKES_LIVES_VANILLA)
        return CodeEditAreas.death_takes_lives.isValid(rom) & known_value

    def __readCodeEditArea(rom: Rom, area:CodeEditArea) -> bytearray:
        return rom.read(area.address, area.length)

    def reduce(self, state:State, action: Action) -> State:

        if state is None:
            state = Store.__loadStateFromRom(self.rom)

        if action.type == ActionNames.starting_lives:
            if(Store.__isBoundedInteger(action.payload, 0, 99)):
                state.starting_lives = int(action.payload)

        elif action.type == ActionNames.continue_lives:
            if(Store.__isBoundedInteger(action.payload, 0, 99)):
                state.continue_lives = int(action.payload)

        elif action.type == ActionNames.load:
            state = Store.__loadStateFromRom(self.rom)

        elif action.type == ActionNames.death_takes_lives:
            state.death_takes_lives = action.payload

        return state

    def __isBoundedInteger(input, lower_limit: int, upper_limit: int) -> Boolean:
        if isinstance(input, int) == False: return False
        return (int(input) >= lower_limit) & (int(input) <= upper_limit)

class Generator():
    store : Store
    rom : Rom

    def __init__(self, store: Store, rom : Rom):
        self.store = store
        self.rom = rom

    def render(self):
        state = self.store.getState()

        if state.starting_lives_area_valid == True:
            self.rom.write(CodeEditAreas.starting_lives.address, [state.starting_lives])

        if state.continue_lives_area_valid == True:
            self.rom.write(CodeEditAreas.continue_lives.address, [state.continue_lives])

        if state.death_takes_lives_area_valid == True:
            if state.death_takes_lives == True:             
                self.rom.write(CodeEditAreas.death_takes_lives.address, DEATH_TAKES_LIVES_VANILLA)
            else:
                self.rom.write(CodeEditAreas.death_takes_lives.address, DEATH_TAKES_LIVES_INFINATE)

class View(CustomDialog):
    store : Store
    generator : Generator

    starting_lives_edit : QLineEdit
    continue_lives_edit : QLineEdit
    button_box : QDialogButtonBox
    invalid_rom_warning : QLabel
    death_takes_lives: QCheckBox

    def __init__(self, parent, store : Store, generator : Generator):
        super(View, self).__init__(parent, title=UIStrings.title)
        self.generator = generator
        self.store = store

        main_layout = QBoxLayout(QBoxLayout.TopToBottom, self)

        self.starting_lives_edit = QLineEdit(self)
        self.starting_lives_edit.setValidator(QIntValidator(0, 99, self))
        self.starting_lives_edit.textEdited.connect(self.__on_starting_lives)

        self.continue_lives_edit = QLineEdit(self)
        self.continue_lives_edit.setValidator(QIntValidator(0, 99, self))
        self.continue_lives_edit.textEdited.connect(self.__on_continue_lives)

        invalid_rom_warning_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.invalid_rom_warning = QLabel(f"{UIStrings.invalid_rom_warning}")
        self.invalid_rom_warning.setWordWrap(True)
        self.invalid_rom_warning.setFixedWidth(400)
        self.invalid_rom_warning.setStyleSheet("QLabel { background-color : pink; }")   # I didn't see a style sheet to draw from, should probably create one?  Better way to do this?
        invalid_rom_warning_layout.addWidget(self.invalid_rom_warning)

        self.button_box = QDialogButtonBox()
        self.button_box.addButton(QDialogButtonBox.Ok).clicked.connect(self.__on_ok)
        self.button_box.addButton(QDialogButtonBox.Cancel).clicked.connect(self.__on_cancel)

        fields_layout = QGridLayout()
        fields_layout.addWidget(QLabel(f"{UIStrings.starting_lives} (0-99):", self), 0, 0)
        fields_layout.addWidget(self.starting_lives_edit, 0, 1)
        fields_layout.addWidget(QLabel(f"{UIStrings.continue_lives} (0-99):", self), 1, 0)
        fields_layout.addWidget(self.continue_lives_edit, 1, 1)

        death_takes_lives_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.death_takes_lives = QCheckBox(f"{UIStrings.death_takes_lives}")
        self.death_takes_lives.stateChanged.connect(self.__on_death_takes_lives)
        death_takes_lives_layout.addWidget(self.death_takes_lives)

        main_layout.addLayout(invalid_rom_warning_layout)
        main_layout.addLayout(fields_layout)
        main_layout.addLayout(death_takes_lives_layout)
        main_layout.addWidget(HorizontalLine())
        main_layout.addWidget(self.button_box, alignment=Qt.AlignRight)

        self.store.subscribe(self.render)
        self.render()
        self.show()

    def render(self):
        state = self.store.getState()

        self.starting_lives_edit.setDisabled(state.starting_lives_area_valid == False)
        self.starting_lives_edit.setText(f"{state.starting_lives}")

        self.continue_lives_edit.setDisabled(state.continue_lives_area_valid == False)
        self.continue_lives_edit.setText(f"{state.continue_lives}")

        self.invalid_rom_warning.setVisible(View.allAreasValid(state) == False)  

        self.death_takes_lives.setDisabled(state.death_takes_lives_area_valid == False)
        self.death_takes_lives.setChecked(state.death_takes_lives)     

    def allAreasValid(state : State) -> Boolean:
        return state.starting_lives_area_valid & state.continue_lives_area_valid & state.death_takes_lives_area_valid

    def __on_ok(self):
        self.generator.render()
        self.done(QDialogButtonBox.Apply)

    def __on_cancel(self):
        self.done(QDialogButtonBox.Cancel)

    def __on_starting_lives(self, text : str):
        self.store.dispatch(Action(ActionNames.starting_lives, text))

    def __on_continue_lives(self, text : str):
        self.store.dispatch(Action(ActionNames.continue_lives, text))

    def __on_death_takes_lives(self):
        self.store.dispatch(Action(ActionNames.death_takes_lives, self.death_takes_lives.isChecked()))
    

class PlayerLives():
    def __init__(self, parent):
        rom = ROM()
        store = Store(rom)
        View(parent, store, Generator(store, rom))


