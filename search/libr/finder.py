from .FreqSet1 import FreqSet
from .sorter import get_score, get_chan_group
from time import sleep
import os
module_dir = os.path.dirname(__file__)  # get current directory






def smart_lookup(num_pilots=None, usa_only=None, group_to_find=None,
				E_extra_max = None, add_lowband = False, L_max = None,
				printz=True, lock_chan_idx=False):

	entered_f8 = False
	output_list = []
	
	if not num_pilots:
		print("""
			


=================================================================================
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$>SMART SEARCH<$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
=================================================================================


			        ~ VTX Guru ~
			        Smart Search

	            VTX Channel Group Recommendation Engine


  Find a high clarity VTX channel group for 3 to 6 FPV pilots, while ensuring 
  as few as possible pilots need to change channels. VTX Guru will find the 
  best rated group that contains as many of the given channels as possible.

  Only groups possessing a passing video clarity score or passing weighted 
  video clarity score are searched. Scores range from 60 (worst) to 100 (best). 
  

  If scores returned are too low to your liking enter 'L' to look at a list of 
  groups with one less matching channel. If some pilots can change channels 
  eaisly and some cannot, you may want to enter only the difficult to change 
  channels; so difficult to change channels are more easily found in the groups 
  returned. 



		
-- Enter number of pilots that will be flying at once.
""")
		while True:

			num_pilots = input("-- (Enter number in range 3 - 6) ==> ")

			if (num_pilots=='3') or (num_pilots=='4') or \
			(num_pilots=='5') or (num_pilots=='6'):
				print("\n\n---------------- Search {} Channel Groups ----------------\n".format(num_pilots))
				break
			print("\n---- Try again. ----\n")


	if usa_only == None:

		while True:

			E_extra_max = None
			L_max = None
			add_lowband = False

			usa_only = input('-- U.S. legal channels only?\n\n-- (Enter Y or N) ==> ').lower()
			if usa_only == 'y':
				usa_only = True
				print("\n\n------------------------ USA ONLY Search ------------------------\n")
				

				if int(num_pilots) < 5:		
					break
				elif int(num_pilots) == 5:
					print("** Top scoring USA 5 channel group has weighted score of  84.0. **\n\n")
					sleep(1)
					break
				
				else:
					print("""
  ** You selected U.S. channels only and are looking for a 6 channel group. **
  ** THERE ARE ONLY 8 CHANNEL GROUPS IN THIS SET WITH A PASSING SCORE!      **
  ** You may be better off looking at the Chart for 6 channel U.S. groups.  **
  ** Top scoring USA 6 channel group has weighted score of  65.6.           **

""")
					sleep(3)
					break


			if usa_only == 'n':
				usa_only = False
				print("\n\n----------------- 40 Channel Search ---------------------------\n")
				add_lowband = input("\n-- Would you like to include lowband channels?\n-- (Enter Y or N) =========> ").lower().strip(" ")
				if add_lowband == 'n':
					add_lowband = False
					E_extra_max = input("\n-- Do at least 2 pilots have a 40 channel VTX?\n-- (Enter Y or N) =========> ").lower().strip(" ")
					if E_extra_max == 'y':
						E_extra_max = None
						break
					if E_extra_max == "n":
						E_extra_max = 1		
						break

				elif add_lowband == 'y':
					add_lowband = True
					if num_pilots == '6':
						print("\n-- *(Lowband 6 channel groups passing scores are 83.3 and above, weighted.)\n")

					L_max = input("\n-- How many pilots have a lowband VTX?\n-- (1-6) =========> ").strip(" ")
					if (L_max == '1') or (L_max == '2')\
					or (L_max == '3') or (L_max == '4')\
					or (L_max == '5') or (L_max == '6'):
						pass

					else:
					  print("\n---- Try again. ----\n")
					  continue

					E_extra_max = input("\n-- Do at least 2 pilots have a 40 channel VTX?\n-- Enter (Y or N) =========> ").lower().strip(" ")
					if E_extra_max == 'y':
						E_extra_max = None
						break
						
					elif E_extra_max == "n":
						E_extra_max = input("\n-- How many pilots have 40 channel VTX's? (0-1)  ===> ").strip(" ")		
					
						if E_extra_max == '1':
							E_extra_max = 1
							break
									
						elif E_extra_max == '0':
							E_extra_max = 0
							break
							
			print("\n---- Try again. ----\n")



	if group_to_find != None:
		if group_to_find == []:
			digit_list = []
		else:	
			group_to_find_init = group_to_find
			freqy = FreqSet(group_to_find)
			digit_list = freqy.convert_freq_abbreviations() # to make sure C channels are converted to R.
			freqy.group = digit_list 					   # to make sure C channels are converted to R.
			group_to_find_raw = freqy.convert_to_abbreviations() # convert back abbrev.
			group_to_find = []
			for chan in group_to_find_raw:
					if chan not in group_to_find:
						group_to_find.append(chan)


	elif group_to_find == None:
		
		print("\n-- Enter VTX channels that pilots are already on. -----")

		while True:
			entered_f8 = False
			group_to_find = []
			freqy = FreqSet()
			freqy.get_input(False, num_pilots, 1)


			if ('f8' in freqy.group):
				if ('r7' in freqy.group):
					print("** F8 and R7 are the same frequency, 5880 MHz.\n** Only enter one or the other. Two pilots cannot use the same frequency.\n\n")
					sleep(3)
					continue
				else:				
					entered_f8 = True
					

			for freq in freqy.group:
				if freq:
					if freq[0] == 'c':
						print('** All C band channels will be converted to R band. (E.g. C4 becomes R4) **\n\n')
						break

			digit_list = freqy.convert_freq_abbreviations() # to make sure C channels are converted to R.
			freqy.group = digit_list 					   # to make sure C channels are converted to R.


			group_to_find_raw = freqy.convert_to_abbreviations()
			

			for chan in group_to_find_raw:
				if chan not in group_to_find:
					group_to_find.append(chan)		
			

			if usa_only or (E_extra_max == 0):
				if ('e4' in group_to_find) or ('e7' in group_to_find)\
				or ('e8' in group_to_find):
					sleep(.5)
					print("-- E4, E7, and E8 cannot be looked for in U.S. only channels. (no 40 chan VTX's) --\n\n\n---- Try again. ----")
					sleep(3)
				else:
					break
			else:
				break


	studies = ['studies/list3.txt', 
	'studies/list4.txt', 
	'studies/list5.txt', 
	'studies/list6.txt']

	if usa_only:
		studies = ['studies/list3usa.txt', 
		'studies/list4usa.txt', 
		'studies/list5usa.txt', 
		'studies/list6usa.txt']

	if add_lowband:
		studies = ['libr/studies/list3low.txt', 
		'studies/list4low.txt', 
		'studies/list5low.txt', 
		'studies/list6low.txt']

	file_path = os.path.join(module_dir, studies[int(num_pilots) - 3])

	with open(file_path, 'r') as f:
		raw_group_list = f.readlines()

	group_list = raw_group_list[3:]
	max_matches = 0
	matches_lists = [[], [], [], [], [], []]
	E_extra_list = ['e4', 'e7', 'e8']
	L_list = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8']


	for i in range(len(group_list)):
		
		matches = 0
		ex_match = 0
		L_match = 0
		group = get_chan_group(group_list[i])
		
		# make sure locked chans in group
		if lock_chan_idx:
			lock_matches = 0
			for idx in lock_chan_idx:
				if group_to_find[int(idx)] in group:
					lock_matches += 1
			if lock_matches != len(lock_chan_idx):
				continue

		#print(E_extra_max)
		if (usa_only == False) and (int(E_extra_max) < 2):
			for extra in E_extra_list:
				if extra in group:
					ex_match += 1
			if ex_match > int(E_extra_max):
				continue
		
		if add_lowband and (int(L_max) < 4):
			for chan in L_list:
				if chan in group:
					L_match += 1
			if L_match > int(L_max):			
				continue
		
		# if empty list is searched add all
		if group_to_find == []:
			matches_lists[0].append(i)
			max_matches = 1
			continue

		for chan in group_to_find:
			if chan in group:
				matches += 1
		if matches >= 1:
			for z in range(1, matches+1):
				matches_lists[z - 1].append(i)

		if matches > max_matches:
			max_matches = matches
	
	if max_matches == 0:
		if printz:
			print("""
********** No group contains any of the frequencies entered. ************


** You may just be searching U.S. legal channels for a 6 channel group 
     -or possibly-
** Make sure to search for common VTX channels, not random frequencies.


				""")
			return

	if printz:
		top_again = max_matches
		while True:
			print("                   -- Pilots on: ", end=' ')
			for chan in group_to_find:
				if entered_f8:
						if chan == 'r7':
							print('F8', end=' ')		
						else:
							print(chan.upper(), end=' ')
				else:
					print(chan.upper(), end=' ')
			print(" --")
			print('\n\n                ------- VTX Guru suggestions: -------')
			print("\n                 Groups contain ~ {} ~ channel matches\n".format(max_matches))

			for i in range(len(matches_lists[max_matches-1])):
				idx = matches_lists[max_matches-1][i]
				list_line = group_list[idx]
				group = get_chan_group(list_line)
				print('\n\n {}.'.format(i+1), end='  ')
				for chan in group:
					if entered_f8:
						if chan == 'r7':
							print('F8', end=' ')		
						else:
							print(chan.upper(), end=' ')
					else:
						print(chan.upper(), end=' ')

				if (int(num_pilots) > 4) and (not add_lowband):
					score = get_score(list_line, 2)
					print(" --   Weighted Video Clarity Score: {}".format(score))

				elif (int(num_pilots) > 4) and (add_lowband):
					score = get_score(list_line, 0)
					print(" --   Video Clarity Score: {}".format(score), end='  ')
					wscore = get_score(list_line, 2)		
					print(" --   Weighted Video Clarity Score: {}".format(wscore))
					

				else:
					score = get_score(list_line, 0)
					print(" --   Video Clarity Score: {}".format(score))


				nextz = input('\n\n-- Press Enter to see next best group in list.\n-- Enter D if done.\n-- Enter L for list with less channel matches but better scores. ===> ').lower().strip(' ')
				if nextz == 'l':
					max_matches -= 1
					if max_matches == 0:
						max_matches = top_again
						break
					else:
						break

				if nextz == 'd':
					
					print("\n\n")
					return
			print('\n\n---------------------------- End of list. -----------------------------\n\n')
			return None

	else:
		if group_to_find != []:
			if ('f8' in group_to_find_init):
					if ('r7' in group_to_find_init):
						pass
					else:				
						entered_f8 = True

		output_list = [[] for j in range(max_matches)]
		for j in range(max_matches):
			for i in range(len(matches_lists[j])):
				idx = matches_lists[j][i]
				list_line = group_list[idx]
				group = get_chan_group(list_line)
				if entered_f8:
					new_group = []
					for g in group:
						if g == 'r7':
							new_group.append('f8')
						else:
							new_group.append(g)
					group = new_group
						
				group = [x.upper() for x in group] 
				score = str(get_score(list_line, 0))
				w_score = str(get_score(list_line, 2))
				if w_score == 'False':
					w_score = 'None'
				w_score += ' - '
				score += ' - '
				out = [score, w_score]
				out.extend(group)

				output_list[j].append(out)
				if i == 4:
					break

		output_list = output_list[::-1]
		if entered_f8:
			new_group = []
			for g in group_to_find:
				if g == 'r7':
					new_group.append('f8')
				else:
					new_group.append(g)
			group_to_find = new_group

		group_to_find_up = [x.upper for x in group_to_find] 
		return output_list, group_to_find_up, digit_list








def get_charts():

	usa_only = False
	add_lowband = False


	print("""



===========================================================================
O-O|O-O|O-O|O-O|O-O|O-O|O-O|>CHARTS EXPLORER<|O-O|O-O|O-O|O-O|O-O|O-O|O-O|O
===========================================================================

			      ~ VTX Guru ~
			     Charts Explorer





** NOTE: Channels R7 and F8 are both the same frequency - 5880 MHz.
         The charts only show 'R7' when referring to the 5880 MHz frequency.
         """)

	while True:
		num_pilots = input("""


-- Charts are organized by how many pilots will be flying at once.

-- Enter number of pilots 
-- (3 to 6) =====================> """)

		num_pilots.strip(' ')
		if (num_pilots=='3') or (num_pilots=='4') or (num_pilots=='5') or (num_pilots=='6'):
			break
		else:
			print("---- Try again ----")


	while True:
		usa_only = input("""
-- Should the chart include only 
-- U.S. legal channels?
-- (Enter Y or N) ===============> """).lower().strip(' ')

		if usa_only == "y":
			usa_only = True
			break
		if usa_only == 'n':
			usa_only = False
			add_lowband = input("""
-- Should the chart include 40
-- channels plus lowband?
-- (Enter Y or N) ===============> """).lower().strip(' ')
			if add_lowband == 'y':
				add_lowband = True
				break
			if add_lowband == 'n':
				add_lowband = False
				break
			
		print("---- Try again ----")

	studies = [
	'libr/studies/list3.txt', 
	'libr/studies/list4.txt', 
	'libr/studies/list5.txt', 
	'libr/studies/list6.txt']

	if usa_only:
		studies = ['libr/studies/list3usa.txt', 
		'libr/studies/list4usa.txt', 
		'libr/studies/list5usa.txt', 
		'libr/studies/list6usa.txt']

	if add_lowband:
		studies = ['libr/studies/markd_up/list3low.txt', 
		'libr/studies/list4low.txt', 
		'libr/studies/list5low.txt', 
		'libr/studies/list6low.txt']

	f = open(studies[int(num_pilots) - 3])
	first_line = f.readline()
	second_line = f.readline()
	third_line = f.readline()

	enumerate_num = 1
	print("\n\n\n\n")
	while True:
		
		print('\n' + "     " + first_line  + second_line + "     " + third_line)
		for i in range(50):
			x = f.readline()
			if (x == ""):
				return
			y = x.replace('100.00', '100 ')
			z = y.replace('100.0', '100 ')
			if enumerate_num < 10:
				print("{}.    ".format(enumerate_num) + z, end='')
			elif enumerate_num < 100:
				print("{}.   ".format(enumerate_num) + z, end='')
			elif enumerate_num < 1000:
				print("{}.  ".format(enumerate_num) + z, end='') 
			else:
				print("{}. ".format(enumerate_num) + z, end='')
			enumerate_num +=1
		more = input("\n\n-- Press Enter for more results. Enter D if done. ====> ").lower()
		more.strip(' ')
		if more == 'd':
				break
		print('\n')
			
	f.close()


'''
If some pilots can change channels eaisly and some cannot, you may 
  want to enter only the difficult to change channels.

'''	