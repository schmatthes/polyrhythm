#
# Program using library music21 to generate Music XML (mxl) or midi files with poly rhythms.
# It uses very simple randomization for rhythm and transpositions (minor pentatonic scale)
#
# It will create 4 tracks:
#   - Piano
#   - Cowbell
#   - Electric bass guitar
#   - bass drum
#
# Since many XML readers cannot handle tracks with different rhythms
# this program generates all tracks with the seemingly same rhythm using the greatest common multiplier.
# E.g. 3 over 4 will generate a cycle of 12 (i.e. 12/4 signature)
# However, it places the notes accordingly to the track's individual rhythm (primary or secondary).
#
# E.g. In the 3 over 4 polyrhythm the "4" would be the primary rhythm which would describe mainly the pulse.
#     The "3" as secondary beat is more about creating a tension or even disruption.
#
# There is even music that uses more than 2 different rhythms.
#
# The 4 tracks will be created as follows:
#   - Piano
#   - Cowbell - secondary rhythm
#   - Electric bass guitar - primary rhythm
#   - bass drum - primary rhythm
#


from nice_libraries import *
from random import choice, randint

# for 5 over 2
# upper_poly = 5   and   lower_poly = 2
#secondary_rhythm = 5
#primary_rhythm = 2

secondary_rhythm = 3
primary_rhythm = 4

print(str(secondary_rhythm) + " over " + str(primary_rhythm))

measure_count = 4

# greatest common multiplier to make upper and lower rhythms compatible
mylcm = lcm(secondary_rhythm, primary_rhythm)
#print("mylcm: " + str(mylcm))

poly_timesig = meter.TimeSignature(str(mylcm) + '/4')

high_part = stream.Part()
low_part = stream.Part()
bassdrum_part = stream.Part()
cowbell_part = stream.Part()

inst_high = instrument.Piano()
high_part.append(inst_high)
#high_part.append(clef.BassClef())
high_part.append(clef.TrebleClef())
high_part.append(poly_timesig)

inst_cowbell = instrument.Cowbell()
cowbell_part.append(inst_cowbell)
cowbell_part.append(poly_timesig)

inst_low = instrument.ElectricBass()
low_part.append(inst_low)
low_part.append(clef.BassClef())
low_part.append(poly_timesig)

inst_bassdrum = instrument.BassDrum()
bassdrum_part.append(inst_bassdrum)
#bassdrum_part.append(clef.PercussionClef())
bassdrum_part.append(poly_timesig)


my_note = note.Note("A3")
#my_note.duration.quarterLength = primary_rhythm
#repeat_count = secondary_rhythm

my_note.duration.quarterLength = 1.0
repeat_count = mylcm
#my_prop = float(1/(mylcm))
my_prop = float(0.6)

for i in range(measure_count):
    #high_part.append(random_pentatonic(my_note, repeat_count))
    high_part.append(modify_rhythm(random_pentatonic(my_note, repeat_count), merge_prob=my_prop))


my_note = note.Note("A1")
my_note.duration.quarterLength = secondary_rhythm
repeat_count = primary_rhythm
my_prop = float(1/(primary_rhythm/2))

for i in range(measure_count):
    #low_part.append(random_pentatonic(my_note, repeat_count))
    low_part.append(modify_rhythm(random_pentatonic(my_note, repeat_count), merge_prob=my_prop))



my_note = note.Note("C2")
my_note.quarterLength = secondary_rhythm
for i in range(measure_count):
    bassdrum_stream = stream.Measure()
    #bassdrum_stream.insert(0, meter.TimeSignature("10/4"))
    bassdrum_stream.repeatAppend(my_note, primary_rhythm)
    bassdrum_part.append(bassdrum_stream)


my_note = note.Note("G#3")
my_note.quarterLength = primary_rhythm
for i in range(measure_count):
    hihat_stream = stream.Measure()
    #hihat_stream.insert(0, meter.TimeSignature("10/4"))
    hihat_stream.repeatAppend(my_note, secondary_rhythm)
    cowbell_part.append(hihat_stream)

my_meta = metadata.Metadata(title='Pentatonic polyrhythm ' + str(secondary_rhythm) + " over " + str(primary_rhythm))


my_score = stream.Score()
my_score.append(my_meta)
my_score.append(high_part)
my_score.append(cowbell_part)
my_score.append(low_part)
my_score.append(bassdrum_part)

my_score.show('text')
my_score.show()
#my_score.show('midi')

