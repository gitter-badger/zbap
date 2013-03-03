import json, logging

from TickActor import TickActor

STATE_FILE = 'data/state.json'

class StateActor(TickActor):
    def __init__(self, mpdActor, sleepSeconds):
        super(StateActor, self).__init__(sleepSeconds)

        self.mpdActor = mpdActor

    def doTick(self):

        current = self.mpdActor.getCurrentSong().get()
        if current == None:
            return

        state = self.loadState()
        state["current"] = current 
        try:
            state["played"][current["name"]] = current["elapsed"]
        except KeyError:
            state["played"] = {}
            state["played"][current["name"]] = current["elapsed"]

        self.saveState(state)

    def playFromLastState(self, name=None, fromStart=False):
        state = self.loadState()
        try:
            if name == state["current"]["name"]:
                fromStart = True

            if name == None:
                name = state["current"]["name"]
        except KeyError:
            logging.getLogger('zbap').info('No info of currently played file. Probably a fresh start.')
            return

        elapsed = 0
        if not fromStart:
            try:
                elapsed = state["played"][name]
            except KeyError:
                logging.getLogger('zbap').info('No info of elapsed seconds of file %s. Playing from start.' % name)
                pass

        self.mpdActor.playByNameFrom(name, elapsed)
            
    def loadState(self):
        try:
            with open(STATE_FILE, 'r') as stateFile:
                return json.load(stateFile) 
        except (IOError, ValueError) as e:
            return {}

    def saveState(self, state):
        with open(STATE_FILE, 'w') as stateFile:
            json.dump(state, stateFile)
