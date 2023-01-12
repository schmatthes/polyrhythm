from music21 import *
from random import choice, randint, random, randrange


# In case we want to use "Guitar Pro" instead of "MuseScore" as mxl reader
#
env = environment.Environment()
#env['musicxmlPath'] = '/System/Volumes/Data/Applications/Guitar Pro 7.app/Contents/MacOS/GuitarPro7'


# generate a measure of pentatonic transposed notes based on input note

def random_pentatonic(mynote: note.Note, count):
    # m2/M2 minor/major second
    # P4 fourth
    # etc
    pentatonic_steps = ["P1", "m3", "P4", "P5", "m7"]
    result = stream.Measure()
    old_picked = -1
    for i in range(count):
        picked = randrange(0,4)
        # Let us not pick the same note as before
        while(picked == old_picked):
            picked = randrange(0,4)

        # raise an octave with 25% likelyhood
        if random() < float(0.25):
            #print("before raise " + mynote.pitch.__str__())
            newnote = mynote.transpose("P8")
            #print("after raise " + mynote.pitch.__str__())
        else:
            newnote = mynote
        result.append(newnote.transpose(pentatonic_steps[picked]))
        old_picked = picked

        #result.show('text')
    return result


# From the "heise" library:
# https://github.com/pinae/music21-melodies
# https://www.heise.de/hintergrund/Jupyter-Musik-komponieren-mit-Python-und-music2-7448180.html?seite=all
#
# CHANGE:
# CHANGE-001: (2023/01/11) added parameter "only_merge" since splits do not go well in polyrhythms
# CHANGE-002: (2023/01/11) randomize the merge/split => only 66% of the measures are modified now
# CHANGE-003: (2023/01/11) rather than only 1 merge we may want to allow some more (-> merge_prob(ability))
# CHANGE-004: (2023/01/11) measures may also contain objects other than notes (e.g. time signature)
#
def modify_rhythm(melody: stream.Measure, do_merge=True, do_split=False, merge_prob=0):


    def do_random_merge(merge_prob=0):

        print("merge_prop: " + str(merge_prob))
        # see CHANGE-002

        #pos = choice(available_merges)
        #print(f"Merging at {pos}.")
        new_melody = stream.Measure()
        #for i, tone in enumerate(melody):

        skip_next = False
        for i in range(len(melody.notes)):
            if skip_next:
                skip_next = False
                continue

            if (i == (len(melody.notes)-1)) or (random() < float(merge_prob)):
                new_melody.append(melody.notes[i])
                #new_melody.append(pitch=melody.notes[i].pitch, quarterLength=tql_left)
            else:
                #print("HAPPY!")
                # create a new note with the quarter length of this and next note and skip next note
                skip_next = True
                tql_left = melody.notes[i].duration.quarterLength
                tql_right = melody.notes[i + 1].duration.quarterLength
                new_melody.append(note.Note(pitch=melody.notes[i].pitch, quarterLength=(tql_left+tql_right)))
                #new_melody.append(note.Note(pitch=melody.notes[i].pitch, quarterLength=(tql_left+tql_right))


#        for i, tone in enumerate(melody.notes):
#            tql = tone.duration.quarterLength
#            if i != pos + 1:
#                new_melody.append(note.Note(
#                    pitch=tone.pitch,
#                    quarterLength=tql * 2 if i == pos else tql))

        return new_melody

    # def do_random_split():
    #     if(len(available_splits) == 0):
    #         return melody
    #     pos = choice(available_splits)
    #     print(f"Splitting at {pos}.")
    #     new_melody = stream.Measure()
    #     for i, tone in enumerate(melody.notes):
    #         tql = tone.duration.quarterLength
    #         if i == pos:
    #             tql = 0.5 * tql
    #             new_melody.append(note.Note(
    #                 pitch=tone.pitch,
    #                 quarterLength=tql))
    #         new_melody.append(note.Note(
    #             pitch=tone.pitch,
    #             quarterLength=tql))
    #     return new_melody


    return do_random_merge(merge_prob)


# least common multiplier, used to make rhythms compatible in polyrhythms
# examples
# 5,2 => 10
# 9,3 = 18
def lcm(number_a, number_b):
    # todo: handle negative input
    # todo: handle zero as input
    if number_a == number_b:
        return number_a
    smaller = 0
    bigger = 0
    if number_a > number_b:
        smaller = number_b
        bigger = number_a
    else:
        smaller = number_a
        bigger = number_b
    result = smaller
    while True:
        if result % bigger == 0:
            #print("result", result)
            return result
        else:
            result += smaller