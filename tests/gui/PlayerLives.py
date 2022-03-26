from foundry.smb3parse.util.rom import Rom
from foundry.gui.PlayerLives import Store, State, Action, ActionNames, RomInterface

default_starting_lives = 5
default_continue_lives = 4

def defaultStore() -> Store:
    return Store(State(default_starting_lives, default_continue_lives, True, True))

def test_subscribeOnInvalidAction():
    store = defaultStore()
    callback = CallbackTester()
    store.subscribe(callback.function)
    assert 0 == callback.called

    store.dispatch(Action("", None))
    assert 0 == callback.called

def test_subscribeOnValidActionStateChange():
    store = defaultStore()
    callback = CallbackTester()
    store.subscribe(callback.function)
    assert 0 == callback.called

    store.dispatch(Action(ActionNames.starting_lives, 1))
    assert 1 == callback.called

def test_subscribeOnValidActionNoStateChange():
    store = defaultStore()
    callback = CallbackTester()
    store.subscribe(callback.function)
    assert 0 == callback.called

    store.dispatch(Action(ActionNames.starting_lives, default_starting_lives))
    assert 0 == callback.called

def test_startingLivesAction():
    startingLivesAction(defaultStore(), 1)

def startingLivesAction(store: Store, updated_starting_lives):
    store.dispatch(Action(ActionNames.starting_lives, updated_starting_lives))
    assert updated_starting_lives == store.getState().starting_lives

def test_startingLivesActionInvalidType():
    store = defaultStore()
    store.dispatch(Action(ActionNames.starting_lives, "P"))
    assert default_starting_lives == store.getState().starting_lives

def test_startingLivesActionInvalidValues():
    store = defaultStore()
    store.dispatch(Action(ActionNames.starting_lives, -1))
    assert default_starting_lives == store.getState().starting_lives
    store.dispatch(Action(ActionNames.starting_lives, 100))
    assert default_starting_lives == store.getState().starting_lives

def test_continueLivesActionInvalidType():
    store = defaultStore()
    store.dispatch(Action(ActionNames.continue_lives, "P"))
    assert default_continue_lives == store.getState().continue_lives

def test_continueLivesActionInvalidValues():
    store = defaultStore()
    store.dispatch(Action(ActionNames.continue_lives, -1))
    assert default_continue_lives == store.getState().continue_lives
    store.dispatch(Action(ActionNames.continue_lives, 100))
    assert default_continue_lives == store.getState().continue_lives

def test_continueLivesAction():
    updated_continue_lives = 2
    store = defaultStore()
    store.dispatch(Action(ActionNames.continue_lives, updated_continue_lives))
    assert updated_continue_lives == store.getState().continue_lives

def test_warningStartLivesValid():
    store = defaultStore()
    assert store.getState().starting_lives

def test_warningContinueLivesValid():
    store = defaultStore()
    assert store.getState().continue_lives

def test_deathTakesLivesAction():
    store = defaultStore()
    store.dispatch(Action(ActionNames.death_takes_lives, False))
    assert False == store.getState().death_takes_lives
    store.dispatch(Action(ActionNames.death_takes_lives, True))
    assert True == store.getState().death_takes_lives

class CallbackTester:
    called = 0
    def function(self):
        self.called = self.called+1

def test_readStateStartingLivesInvalid():
    rom = Rom(bytearray([0] * 0x50000))
    assert None == RomInterface(rom).readState().starting_lives

def createStartingLivesRom() -> Rom:
    rom = Rom(bytearray([0] * 0x50000))
    
    rom.write(0x308E1-4, [0xCA, 0x10, 0xF8, 0xA9])
    rom.write(0x308E1, [0x04])
    rom.write(0x308E1+1, [0x8D, 0x36, 0x07, 0x8D])
    return rom

def test_readStateStartingLivesValid():
    state = RomInterface(createStartingLivesRom()).readState()
    assert 0x04 == state.starting_lives

def test_writeStateStartingLives():
    romInterface = RomInterface(createStartingLivesRom())
    state = State(0xAA, default_continue_lives, True, True)
    assert 0x04 == romInterface.readState().starting_lives
    romInterface.writeState(state)
    assert 0xAA == romInterface.readState().starting_lives

def test_readStateContinueLivesInvalid():
    rom = Rom(bytearray([0] * 0x50000))
    assert None == RomInterface(rom).readState().continue_lives

def createContinueLivesRom() -> Rom:
    rom = Rom(bytearray([0] * 0x50000))   
    rom.write(0x3D2D6-4, [0x08, 0xD0, 0x65, 0xA9])
    rom.write(0x3D2D6, [0x04])
    rom.write(0x3D2D6+1, [0x9D, 0x36, 0x07, 0xA5])
    return rom

def test_readStateContinueLivesValid():
    state = RomInterface(createContinueLivesRom()).readState()
    assert 0x04 == state.continue_lives

def test_writeStateContinueLives():
    romInterface = RomInterface(createContinueLivesRom())
    state = State(0x00, 0xAA, True, True)
    assert 0x04 == romInterface.readState().continue_lives
    romInterface.writeState(state)
    assert 0xAA == romInterface.readState().continue_lives

def test_readStateDeathTakesLivesInvalid():
    rom = Rom(bytearray([0] * 0x50000))
    assert None == RomInterface(rom).readState().death_takes_lives

def createDeathTakesLivesRom(value):
    rom = Rom(bytearray([0] * 0x50000))
    rom.write(0x3D133-4, [0x8B, 0x07, 0xD0, 0x05])
    rom.write(0x3D133, value)
    rom.write(0x3D133+3, [0x30, 0x0b, 0xA9, 0x80])
    return rom

def test_readStateDeathTakesLivesFalse():
    state = RomInterface(createDeathTakesLivesRom([0xEA, 0xEA, 0xEA])).readState()
    assert False == state.death_takes_lives

def test_readStateDeathTakesLivesTrue():
    state = RomInterface(createDeathTakesLivesRom([0xDE, 0x36, 0x07])).readState()
    assert True == state.death_takes_lives

def test_readState100CoinsInvalid():
    rom = Rom(bytearray([0] * 0x50000))
    assert None == RomInterface(rom).readState().hundred_coins_1up

def create100CoinsRom(value):
    rom = Rom(bytearray([0] * 0x50000))
    rom.write(0x350A7-4, [0x7d, 0xae, 0x26, 0x07])
    rom.write(0x350A7, value)
    rom.write(0x350A7+3, [0xa9, 0x40, 0x8d, 0xf2])
    return rom

def test_readState100CoinsFalse():
    state = RomInterface(create100CoinsRom([0xEA, 0xEA, 0xEA])).readState()
    assert False == state.hundred_coins_1up

def test_readState100CoinsTrue():
    state = RomInterface(create100CoinsRom([0xfe, 0x36, 0x07])).readState()
    assert True == state.hundred_coins_1up

def test_writeState100Coins():
    romInterface = RomInterface(create100CoinsRom([0xEA, 0xEA, 0xEA]))
    state = State(0x00, 0x00, True, True)
    assert False == romInterface.readState().hundred_coins_1up
    romInterface.writeState(state)
    assert True == romInterface.readState().hundred_coins_1up

