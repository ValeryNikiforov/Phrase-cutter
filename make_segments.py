import json
from pydub import AudioSegment
import sys

if (len(sys.argv) == 4):
	lev_dist = int(sys.argv[2])
	length_for_lev = int(sys.argv[3])

elif (len(sys.argv) == 3): 
	lev_dist = int(sys.argv[2])
	length_for_lev = 5

elif (len(sys.argv) == 2):
	lev_dist = 1
	length_for_lev = 5

else: 
	print("Скрипту сегментации передано неверное число параметров")
	exit(0)
print(sys.argv)
print(lev_dist,length_for_lev)

def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

class phrase:
	def __init__(self,text):
		self.words = text.split()
		self.start = None
		self.end = None

end = False 
text = []
while(end != True):
	try:
		text.append(input().split())
	except (EOFError): 
		end = True

phrases = []
with open('phrases.json') as json_file:
    data = json.load(json_file)
for x in data:
	phrases.append(phrase(**x))
for phrase in phrases:
	score = 0
	i=0
	while (i<len(phrase.words)):
		for j in range (len(text)):
			if (i < len(phrase.words)):
				#if (text[j][4] == phrase.words[i]): 
				if ((text[j][4] == phrase.words[i]) or (distance(text[j][4], phrase.words[i]) <= lev_dist and len(text[j][4])>=length_for_lev)):
					score += 1
					i+=1
				else:
					i -= score 
					score=0
				if (score==len(phrase.words)):
					phrase.start = text[j-i+1][2]
					if (j+1>=len(text)): 
						phrase.end=-1 ##отдельно обработать последнее слово во всей записи 
					else:
						phrase.end = text[j+1][2]
						score = 0
		i+=1			

newAudio = AudioSegment.from_wav('{}'.format(sys.argv[1]))
for phrase in phrases:
	if (phrase.start != None):
		print('Фраза: ',phrase.words,'выделена:',phrase.start,":",phrase.end)
		phrase_signal = newAudio[float(phrase.start)*1000:float(phrase.end)*1000]
		phrase_signal.export('{}.wav'.format(phrase.words) ,format="wav")
	else:
		print('Фраза: ',phrase.words,'отсутствует')	 