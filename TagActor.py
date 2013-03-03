import pykka, logging, json
from pygame import mixer

TAGS_FILE = 'data/tags.json'

class TagActor(pykka.ThreadingActor):
    def __init__(self, stateActor):
        super(TagActor, self).__init__()

        self.stateActor = stateActor

        mixer.init()
        self.ack = mixer.Sound('data/ack.wav')
        self.ack.set_volume(1.0)

    def playByTag(self, tag, fromStart=False):
        try:
            self.ack.play()

            tags = self.loadTags()
            print tags
            self.stateActor.playFromLastState(tags[tag], fromStart)
        except KeyError:
            logging.getLogger('zbap').error('No such tag %s' % tag)

    def loadTags(self):
        try:
            with open(TAGS_FILE, 'r') as tagsFile:
                return json.load(tagsFile) 
        except (IOError, ValueError) as e:
            logging.getLogger('zbap').error('Unable to load tag file %s' % TAGS_FILE)
            logging.getLogger('zbap').exception(e)
            return {}

    def saveTags(self, state):
        with open(TAGS_FILE, 'w') as tagsFile:
            json.dump(state, tagsFile)