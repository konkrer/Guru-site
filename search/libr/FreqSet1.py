from time import sleep
import os
module_dir = os.path.dirname(__file__)  # get current directory

"""
A class made to hold a frequency group of 5GHz FPV VTX channels,
then analyze and/or score for IMD interference level. 

Investigate method allows for scoring all possible combinations of
channels in study group. 40 channels, plus lowband channels availavle
to add to study group. Only groups with passing scores are output to 
file.  U.S. legal channels only option available. Selective removal 
of channels allows for almost all possible subsets of parent set to 
be explored. (removal allowed up to 40 channels)

"""



class FreqSet:
  
  def __init__(self, lst=[]):
    
    self.group = lst
    self.output = None
    self.scores = []


  def get_input(self, printz=True, channels=6, quit_on=2):
    
    self.group = []
    if printz:
      print ("""
    


=============================================================================
\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/>IMD ACE<\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
=============================================================================


                               ~ VTX Guru ~
                               IMD Analyzer 

                   FPV VTX CHANNEL INTERFERENCE CHECKER


    
    Transmitting on two or more video channels can cause problems.
    Enter two to six channels to check for interference.
""")
    print("""    
    Enter Band Channel abbreviation or four digit frequency.
    -Bands: A - B - E - F - R(C) - L
    -Channels: 1-8
    
""")   

    # for each channel
    for i in range(int(channels)):
      # ask appropritate question 
      continue_on = self.ask_question(i, quit_on)
      # if user enters 'done' or enters all chans at once we're done
      if continue_on == False:
        print('\n\n')
        return
    print('\n\n')




  def ask_question(self, ques_num, quit_on):

    questions =[
      "\n-- Enter first VTX channel -OR-\n-- Enter entire group at once ==> ",
      "\n-- Enter second video channel => ",
      "\n-- Enter {0} video channel\n-- (Enter D if done) ==========> ",
      "\n-- Enter next video channel\n-- (Enter D if done) ==========> ",
      "\n-- Enter second video channel\n-- (Enter D if done) ==========> ",
      ] 

    numbers = ['third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', \
    'tenth', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th']

    while True:

      # if quiting on second question is an option
      if (ques_num == 1) and (quit_on == 1):
        answer = input(questions[-1]).lower().strip(' ')

      # for 21st question and after just ask for next channel
      elif (ques_num > 19):
        answer = input(questions[-2]).lower().strip(' ')

      # for 1st and 2nd question use index to select question
      elif (ques_num < 2):
        answer = input(questions[ques_num]).lower().strip(' ')

      # else use standard question and plug in channel number  
      else:
        answer = input(questions[2].format(numbers[ques_num -2])).lower().strip(' ')
      
      # for 1st question
      if ques_num == 0:
        
        # if entry is multiple - split and remove empty strings
        input_group_init = answer.split(' ')           
        if len(input_group_init) > 1:
          input_group = [x for x in input_group_init if x != '']

          # more than 40 is too many, start over
          if  len(input_group) > 40:
            print('\n----- Try again. -----')
            continue

          # if an entry is Not a channel that's Not ok
          ok = True
          for chan in input_group:
            if not check_channel_input(chan):
              ok = False
              break

          # if inputs all were legit channels assign them to self.group
          if ok:
            self.group = input_group
            # no need to continue asking questions as group entry worked!
            return False

          # if not ok ask question again/start over
          else:
            continue

      # if we allow quitting at this question
      if ques_num >= int(quit_on):
        # check for 'done' entry, if so quit asking questions (return False)
        if answer == 'd':        
          return False

      # otherwise if entry is legit
      if check_channel_input(answer):
        # add to self.group, return True to continue asking questions if there are more 
        self.group.append(answer)
        return True




  # find all IMD frequencies
  def check_freqz(self, group):
  
    all_imd_freqs = []
  
    # for each channel 
    for channel in group: 

      # create a list of all other channels
      rest = filter(lambda x: (x != channel), group) 
      imd_freqs = []

      # compute IMD for channel and each other channel
      for chan in rest: 

        imd_freq = (int(channel) * 2) - int(chan)
        imd_freqs.append(imd_freq)
      
      # compile all sublists 
      all_imd_freqs.append(imd_freqs)

    return all_imd_freqs





  def analyze_interference(self, group, printz=True):
  
    bad_freq = self.check_freqz(group)
    bad_match = 0
    bad_close = 0
    close = 0
    near = 0
    warnings = []
    
    if printz:
      print('          --------------------------------------------------')
      print('                | IMD close to VTX channel instances |') 

    for sublst in bad_freq:
      for x in sublst:
      
        for i in range(len(group)):
           
          if int(group[i]) != x:    
            diff = abs(x - int(group[i]))
            if diff <20 and diff >= 10:
              if printz:
                print("\n   IMD on %s is quite close to %s (%s MHz)" % (x, group[i], diff))
              warnings.append("IMD on %s is close to %s (%s MHz)" % (x, group[i], diff))
              close += 1

            elif diff < 10:
              if printz:
                print("\n   Warning: IMD on %s is very close to %s (%s MHz)" % (x, group[i], diff))
              warnings.append("**Warning IMD on %s is very close to %s (%s MHz)" % (x, group[i], diff))
              bad_close += 1

            elif  diff < 35:
              if printz:
                print("\n   IMD on %s is close to %s (%s MHz)" % (x, group[i], diff))
              warnings.append("IMD on %s is near to %s (%s MHz)" % (x, group[i], diff))
              near += 1 

          elif int(group[i]) == x:
            if printz:
              print("\n   **Warning: %s will have terrible interference! IMD exact match to VTX channel!**" % (group[i]))
            warnings.append("**Warning %s will have terrible interference! IMD exact match to VTX channel!**" % (group[i]))
            bad_match += 1

    printable = self.convert_to_abbreviations()
    converted = self.convert_freq_abbreviations()

    if printz:
      if (close == 0) and (bad_close ==  0) and (near == 0) and (bad_match) == 0:
       print('                            --- NONE ---')  
      print('          --------------------------------------------------\n\n\n')


      if bad_match + bad_close + close + near == 0:
        print("                   -------ANALYSIS-------\n\n 	    All clear. Minimal IMD interference.")

      
      elif bad_match + bad_close + close == 0:
        
        print("                  -------ANALYSIS-------\n\n 	   	IMD interference not too bad.\n")
        
        if len(group) >= 5:
          print(" 	This is an excellent IMD rating for 5 or 6 channels.")
      

      elif bad_match == 0 and bad_close == 0:
        print("                  -------ANALYSIS-------\n\n 	      Troubling interference possible.\n")
        
        if len(group) >= 5:
          print(" 	     Good IMD rating for 5 and 6 channels.")
        

      elif bad_match == 0 and bad_close > 0:
        print("                   -------ANALYSIS-------\n\n 		     IMD problems likely!\n 	   IMD within 10MHz of at least one channel.")

      
      elif bad_match > 0:
        print(" 			 -------ANALYSIS-------\n\n 	  Bad channel grouping! Debilitating interference!")
      

      print("\n")
      print("                 ", end='')
      for chan in printable:
        print (chan.upper(), end='   ')
      

      print("\n")
      print("           ", end='')
      for chan in converted:
        print (chan, end='   ')

      print("\n\n\n")

    return warnings, printable, converted






  def convert_freq_abbreviations(self):
    
    converter = {}
    converted = []
    file_path = os.path.join(module_dir, 'vtx_channel_guide.txt')

    with open(file_path, 'r') as f:
      for line in f:

        sliced_raw = line.split(', ')
        dirty = sliced_raw[1]
        clean = dirty.strip('\n')
        converter[sliced_raw[0]] = clean
    
    for chan in self.group:    
        
      if len(str(chan)) == 2:
        value = converter[chan]
        converted.append(int(value))
        
      else:
        converted.append(int(chan))

    return converted






  def convert_to_abbreviations(self):
    
    converter = {}
    converted = []
    file_path = os.path.join(module_dir, 'vtx_channel_guide_abrv.txt')

    with open(file_path, 'r') as f:
      for line in f:

        sliced_raw = line.split(', ')
        dirty = sliced_raw[1]
        clean = dirty.strip('\n')
        converter[clean] = sliced_raw[0]
    
    for chan in self.group:
          
      if len(str(chan)) == 4:
        if str(chan) in converter.keys():
          value = converter[str(chan)]
          converted.append(value)
        else:
          converted.append(chan)   
      else:
        converted.append(chan)

    return converted






  def score(self, group, printz=True):
    
    IMD_freqz = self.check_freqz(group)
    score_total = 0
    divide_by = 0
    IMD_close_to_chan = 0
    broadcast_close_times = 0
    closest_imd = None
    closest_broadcast = None
    broadcast_factor = None
    score_alt = None
    score_alt_weighted = None
    IMD_score = None

    
    # for broadcast factor
    sorted_group = sorted(group, reverse=True)
    for i in range(len(sorted_group) - 1):

      # calculate VTX channel separation
      seperation = sorted_group[i] - sorted_group[i+1]
      
      # keep track of closest VTX channel separation
      if closest_broadcast == None:
        closest_broadcast = seperation
      else:
        if seperation < closest_broadcast:
          closest_broadcast = seperation

      # keep track of total times VTX channels separation less than 40
      if seperation < 40:
        broadcast_close_times += 1

 

    # for unique IMD score
    unique_prob_imd = []
    score_total_uniq = 0
    divide_by_uniq = 0

   # for each IMD freq
    for sublst in IMD_freqz:
      for IMD_freq in sublst:
        worst = None

        # then for each channel       
        for chan in group:
          # if seperation less than 35MHz
          diff3 = abs(IMD_freq - chan)
          if diff3 < 35:

            # count every time IMD is close to a channel
            IMD_close_to_chan += 1

            # keep track of least separation of current IMD to channel 
            if worst == None:
              worst = diff3
            else:
              if diff3 < worst:
                worst = diff3
        
        # if IMD was closer than 35 MHz to a channel
        if worst != None:

          # for each problem IMD, use least separation of that IMD to a channel to compute a reducing score
          # and keep running sum of squared reducing scores and of number of scores to divde by later
          to_add = (35 - worst) ** 2
          score_total += to_add
          divide_by += 1

          # for calculating unique IMD freqs score
          if (IMD_freq not in unique_prob_imd):
            # for each problem IMD, use least separation of that IMD to a channel to compute a reducing score
            # and keep running sum of squared reducing scores and of number of scores to divde by later
            score_total_uniq += to_add
            divide_by_uniq += 1
            unique_prob_imd.append(IMD_freq)

            # keep track of overall worst offender - closest IMD to channel
            if closest_imd == None:
              closest_imd = worst
            else:
              if worst < closest_imd:
                closest_imd = worst
           
    # ratio = (IMD_close_to_chan / len(group))

    # if there were problem IMD frequencies
    if divide_by != 0:

      # calculate two IMD scores
      IMD_score =  100 - (((float(score_total) /divide_by) ** .5) * 2.857142857)  
      IMD_score_uniq =  100 - (((float(score_total_uniq) /divide_by_uniq) ** .5) * 2.857142857)

      # use the lower of these two scores
      if IMD_score_uniq < IMD_score:
        IMD_score = IMD_score_uniq
        divide_by = divide_by_uniq

      # to reduce proportional to times IMD was close to channels in total
      IMD_score *= (1 - (IMD_close_to_chan / 30))  

    if printz: # print stats
      print(" Number of Problem \n IMD frequencies: ============> " + str(divide_by) + "\n")
      print(" Times problem IMD freq \n is close to VTX channel: ====> " + str(IMD_close_to_chan) + "\n")
      #print(" Problem IMD close / Channels \n ratio is: ===================> " + str(round(ratio, 1)) + "\n")
      print(" Minimum Problem IMD\n frequency seperation\n to VTX channel: =============> " + str(closest_imd) + " MHz\n")

    # fail condition - IMD matches VTX channel
    if closest_imd == 0:
      score_alt = 0
      IMD_score = 0
      if printz:
        if closest_broadcast <= 27:
          print(" ***** VTX channels too close!!! %s MHz apart. *****\n" % (closest_broadcast))
        else:
          print(" Minimum VTX\n channel separation  =========> %sMHz\n" % (closest_broadcast))
    
    # fail condition - VTX channels less than 27MHz separation
    elif closest_broadcast <= 27:
      score_alt = 0
      if printz:
        print(" ***** VTX channels too close!!! %s MHz apart. *****\n" % (closest_broadcast)) 
    
    else:

      # if a separation is less than 40 MHz calculate broadcast factor 
      if closest_broadcast < 40:
           
        if closest_broadcast < 35:
          if printz:
             print(" *** VTX channels close! %s MHz apart. ***\n" % (closest_broadcast))

        else:
          if printz:
            print(" Minimum VTX\n channel separation  =========> %sMHz\n (Channels getting close!)\n" % (closest_broadcast))
            
        broad_score = (40 - closest_broadcast)
        
        if closest_broadcast < 37:
          broadcast_factor = (1 - (broad_score / (26 - broad_score))) * (1/broadcast_close_times)
        
        else:
          broadcast_factor = (1 - (broad_score / (26 - broad_score)))

      # if there are problem IMD frequencies
      if divide_by != 0:
        # set score_alt to IMD_score for further calculations
        score_alt = IMD_score 
        
        # to reduce score proportional to close broadcast channels
        if broadcast_factor:   
          score_alt *= broadcast_factor  
                         
        # if no broadcast factor print separation info now
        else:
          if printz:
            print(" Minimum VTX\n channel separation  =========> %sMHz\n\n" % (closest_broadcast))
        
        # create weighted score if 6 channel group
        if len(group) == 6:

          # scale so top scoring 6 channel group (from 40 channel set) now scores 100. IMD6 now scores 62.3         
          score_alt_weighted = round(score_alt * 2.204, 1) 
          
        # create weighted score if 5 channel group
        elif len(group) == 5:
          
          # compress range of 5 group scores so IMD5 now scores 62.3 (after +20 below)
          if score_alt < 80:
            compressd =  ((80 - score_alt) / 6.09) + score_alt
          else:
            compressd = score_alt

          # scale so top scoring 6 channel group (from 40 channel set) now scores 100 (+20)      
          score_alt_weighted = round((compressd + 20), 1) 
          
      # no problem IMD's results in 100 IMD score
      else:
        IMD_score = 100.00

        # no VTX separation less than 40MHz score_alt is also 100
        if broadcast_factor == None:
          score_alt = 100.00
          # if printz print separation info now
          if printz:
            print(" Minimum VTX\n channel separation  =========> %sMHz\n\n" % (closest_broadcast))        
        # else the score is IMD score(100) X broadcast factor
        else:
          score_alt = 100.0 * broadcast_factor

    score_alt = round(score_alt, 2)
    IMD_score = round(IMD_score, 2)

    # to generate weighted score for 5 & 6 channel groups with perfect IMD scores; only needed for lowband groups
    if (divide_by == 0) and (len(group) in [5, 6]):
      if len(group) == 6:
        score_alt_weighted = round(score_alt * 2.204, 1)
      if len(group) == 5:
        score_alt_weighted = round((score_alt + 20), 1)

    # final stats to print
    if printz:
      # add IMD score only if it's different than score_alt
      if (broadcast_factor != None) or (closest_broadcast <= 27):
        print(" IMD Score: ==================> {:.2f}\n".format(IMD_score)) 
      print(" Video Clarity Score: ========> {:.2f}".format(score_alt))
      if score_alt_weighted:
        print("""
 Weighted Video Clarity Score
 (weighted relevant to {number}
 channels): ==================> {score}
        """.format(number=len(group), score=score_alt_weighted))
      print("\n Top Possible Score is 100\n\n\n\n")
    
    self.scores = [score_alt, score_alt_weighted, closest_broadcast, IMD_score]

    # returns for web app
    return score_alt, score_alt_weighted, closest_broadcast, IMD_score, divide_by, IMD_close_to_chan, closest_imd




  def export(self, converted, csv=False):
    
    if self.output == None:
      
      abbreviations = self.convert_to_abbreviations()
      output_file = input("-- Name of output_file?")

      with open(output_file, "a") as f:
        f.write("%.2f  %.2f  %s  %s   " % (self.scores[0], self.scores[3], self.scores[1], self.scores[2]))
        for chan in abbreviations:
          f.write(str(chan).lower() +" ")
        f.write('-- ')
        for freq in converted:
          f.write(str(freq) + " ",)
        f.write('-- ')
        converted.sort()
        for freq in converted:
          f.write(str(freq) + " ",) 
        f.write("\n")

    elif csv == False:
      with open(self.output, "a") as f:
        f.write("%.2f  %.2f  %s  %s   " % (self.scores[0], self.scores[3], self.scores[1], self.scores[2]))
        for chan in self.group:
          f.write(str(chan).lower() + " ",)
        f.write('-- ')
        for freq in converted:
          f.write(str(freq) + " ",)
        f.write('-- ')
        converted.sort()
        for freq in converted:
          f.write(str(freq) + " ",)
        f.write("\n")
 
    else:

      with open(self.output, "a") as f:
        f.write("%.2f,%.2f,%s,%s," % (self.scores[0], self.scores[3], self.scores[1], self.scores[2]))
        for chan in self.group:
          f.write(str(chan).lower() + " ",)
        f.write(',')
        for freq in converted:
          f.write(str(freq) + " ",)
        f.write(',')
        converted.sort()
        for freq in converted:
          f.write(str(freq) + " ",)
        f.write("\n")








  def investigate(self, score_limit=60):

    num_channels = 0
    usa_only = False
    add_lowband = False
    extra_remove = False
    csv = False
    print("""



===========================================================================      
??????????????????????????????????i????????????????????????????????????????      
===========================================================================
                      
                             ~ VTX GURU ~
                            EZ iNVESTIGATE





** NOTE: Channels R7 and F8 are both the same frequency - 5880 MHz.
         The output only shows 'R7' when referring to 5880 MHz.


         """)
    while True:
      num_channels_raw =  input("\n\n-- How many in channel group\n-- to investigate? (3-6) =======> ")
      num_channels = num_channels_raw.strip(' ')
      
      if (num_channels == '3') or (num_channels == '4')\
         or (num_channels == '5') or (num_channels == '6')\
         or (num_channels == '7'):
        
        if (num_channels == '7'):
          print("\n\n\n**** YOU SELCETED 7 ......SNEAKY!!! GET READY TO WAIT FOR COMPLETION!\n**** CTRL C to force quit program.")  
          print("**** SCORE LIMIT FOR CHANNEL GROUPS LOWERED TO 8 (unless adding lowband)")
          score_limit = 8
          break
          
        else:
          break
      else:
        print("\n\n---- Try Again ----\n\n")
    
    while True:
      usa_only = input("\n\n-- USA only? (Enter Y or N) ====> ").lower().strip(' ')
      
      if usa_only == 'y':
        print('\n\n---- USA VTX CHANNELS ONLY CONFIRMED ----\n\n')
        usa_only = True
        break
      if usa_only == 'n':
        print('\n\n---- 40 VTX CHANNELS CONFIRMED ----\n\n')
        usa_only = False
        add_lowband = input("-- Add lowband channels? (Enter Y or N) =====> ")
        if add_lowband == 'y':
          add_lowband = True
          if num_channels == '7':
            score_limit = 60
          break
        if add_lowband == 'n':
          add_lowband = False
          break
      
      print("\n\n---- Try Again ----\n\n")
      

    if not usa_only:
      while True:
        extra_remove_raw = input("""

-- Remove any frequencies from the VTX channel set? --

-- (Enter Y or N) ==============> """).lower()
        extra_remove = extra_remove_raw.strip(' ')
        if (extra_remove == 'y'):
          extra_remove = True
          break
        if (extra_remove == 'n'):
          extra_remove = False
          break
        else:
          print("\n\n---- Try Again ----\n\n")
    
    if extra_remove:
      to_remove = FreqSet()
      to_remove.get_input(False, 40, 1)
           
      if 'f8' in to_remove.group:
        f8_idx = to_remove.group.index('f8')
        to_remove.group[f8_idx] = 'r7'

      new_list =[]
      for chan in to_remove.group:
        if (chan not in new_list):
          new_list.append(chan)
      to_remove.group = new_list
      
    csv_ques = input('\n-- Export to CSV? (Enter Y or N) =====> ').strip(' ').lower()
    if csv_ques == 'y':
      print('\n-- Exporting to CSV.')
      csv = True
    else:
      print('\n-- Exporting readable text format.')


    self.output = input("\n-- Filename to output data?\n\n-- (E.g. something.txt): ")

    
    channels = []

    with open('libr/vtx_channel_guide_abrv.txt') as f:
      for i in range(39):

        line = f.readline()
        sliced_raw = line.split(', ')
        channels.append(sliced_raw[0])

    if usa_only:
      channels.remove('e4')
      channels.remove('e7')
      channels.remove('e8')
    
    if add_lowband:
      channels = []
      with open('libr/vtx_channel_guide_abrv.txt') as f:
        for i in range(47):
          line = f.readline()
          sliced_raw = line.split(', ')
          channels.append(sliced_raw[0])

    if extra_remove:
      for chan in to_remove.group:
        try:
          channels.remove(chan)
        except ValueError:
          pass
      print("\n\n\n** Channels that were removed\n   from study set ============> ", end=' ')
      for chan in to_remove.group:
        print(chan, end=' ')
      print("\n")

      if len(channels) < int(num_channels):
        print("**** Too many channels removed! ****")
        sleep(3)
        return

    print("\n")

    if csv:
      with open(self.output, "a") as f:
          f.write("score,IMD_score,weighted_score,vtx_separation,channel_group,freq_group,frequency_group\n")
    else:
       with open(self.output, "a") as f:
          f.write(
"""IMD = IMD score | WVCS = weighted Video Clarity Score  |  SEP = minimum VTX channel seperation

VCS   | IMD | WVCS | SEP|   CHANNELS    |        FREQUENCIES        |    Sorted Frequencies\n""")

    gen = combo_explor(channels, int(num_channels))

    coutner = 0

    while True:
      
      out = next(gen)

      if out == None:
        break

      flat = flatten(out)
      self.group = flat

      converted = self.convert_freq_abbreviations()
      self.score(converted, False)


      # judge scores by weighted scores for 5 channel non-lowband groups
      if ((int(num_channels) == 5) and not (add_lowband)):
     
        if self.scores[1] != None:
          if self.scores[1] >= score_limit:
            self.export(converted, csv)

      # judge scores by weighted scores for 6 channel groups
      elif (int(num_channels) == 6):
        
        if add_lowband:
          if self.scores[1] != None:
            if self.scores[1] >= 83.3:
              self.export(converted, csv)
        else:
          if self.scores[1] != None:
            if self.scores[1] >= score_limit:
              self.export(converted, csv)


      # judge scores by un-weighted scores for all other groups
      else:
        if self.scores[0] >= score_limit:
          self.export(converted, csv)
      
      coutner+=1

    print("\n\n---- %s Combinations checked! ----" % (coutner))

    
    
    


   

def combo_explor(lst, combo_of, first_loop=True):

  first_count = 0

  # if we're looking for a combination of 1
  if combo_of == 1:
    
    while True:
      # for each item in list
      for i in range(len(lst)):
        # count each time if back at begining of list 
        if i == 0:
          first_count += 1
        # if on second lap return None
        if first_count == 2:
          yield (None)
        # yeild item
        yield (lst[i])

  else:
    # create list minus the remaining number of elements of combo from end of list
    end_shortened = lst[:-(combo_of-1)]

    while True:
      # for each element in truncated list
      for i in range(len(end_shortened)):
        # as each first element of combo iterates show progress
        if first_loop:
          print("-- WORKING.....")
        # count each time back at begining of list
        if i == 0:
          first_count += 1
        # if on second lap return None
        if first_count ==2:
          yield (None)
        # the actual element of the list
        element = end_shortened[i]
        # generator for what's left of the list to explore
        rest = combo_explor(lst[i+1:], combo_of-1, False)

        while True:
          # call next combo 
          nxt = next(rest) 
          # if nxt == None all combos explored go to next element in list          
          if nxt == None:
            break                           
          # yeild list element plus next combo from generator
          yield element, nxt



def flatten(tup):

  if tup == None:
    return None

  flat_list = []
  # when second element is not another tuple
  if not isinstance(tup[1], tuple):
    # just unpack 1st and 2nd element to flat_list
    flat_list = [tup[0], tup[1]]
    return flat_list

  else:
    # first element is extracted and added to flat_list
    x = tup[0]
    flat_list.append(x)
    # secong element is extracted and flattened
    y = tup[1]
    z = flatten(y)
    # add flattened elements to flat_list
    flat_list += z

    return flat_list



def check_channel_input(chan_input):
    
    bands = ['a', 'b', 'c', 'e', 'f', 'r', 'l']
    channels = [str(x) for x in range(1,9)]

    try:
        
      if (chan_input[0] in bands and chan_input[1] in channels)\
      and len(chan_input) == 2:         
        return True

      if ((int(chan_input) <= 5945) and (int(chan_input) >= 5325)):        
        return True
         
      else:
        print("\n----- Try Again. -----\n")
        return False


    except (ValueError, IndexError):
      print("\n----- Try Again. -----\n")
      return False

   

'''
l = len(channels)
    
    base_case = factorial(l, num_channels) / factorial(num_channels)


    channel_1_used = []
    combo_count = 0

    while True:
      for i in range(len(channels)):
        
        channel_1 = channels[i]
        channel_1_used.append(channel_1)
        channels_2 = [channel for channel in channels if channel not in channel_1_used] 
        
        channel_2_used = []
        channels_2_redux = [channel for channel in channels_2]

        if num_channels == 3:
          channels_2_redux.pop()
        elif num_channels == 4:
          channels_2_redux.pop()
          channels_2_redux.pop()
        elif num_channels == 5:
          channels_2_redux.pop()
          channels_2_redux.pop()
          channels_2_redux.pop()
        elif num_channels == 6:
          channels_2_redux.pop()
          channels_2_redux.pop()
          channels_2_redux.pop()
          channels_2_redux.pop()
        

        for i in range(len(channels_2_redux)):
          channel_2 = channels_2_redux[i]
          channel_2_used.append(channel_2)
          
          channels_3 = [channel for channel in channels_2 if channel not in channel_2_used]
          
          channel_3_used = []
          channels_3_redux = [channel for channel in channels_3]
          if num_channels == 4:
            channels_3_redux.pop()
          elif num_channels == 5:
            channels_3_redux.pop()
            channels_3_redux.pop()
          elif num_channels == 6:
            channels_3_redux.pop()
            channels_3_redux.pop()
            channels_3_redux.pop()
             

          for i in range(len(channels_3_redux)):
            channel_3 = channels_3_redux[i]
          
            if num_channels >= 4:

              channel_3_used.append(channel_3)
              channels_4 = [channel for channel in channels_3 if channel not in channel_3_used]
              channel_4_used = []
              channels_4_redux = [channel for channel in channels_4]
              if num_channels == 5:
                channels_4_redux.pop()
              elif num_channels == 6:
                channels_4_redux.pop()
                channels_4_redux.pop()

              for i in range(len(channels_4_redux)):
                channel_4 = channels_4_redux[i]
              
                if num_channels >= 5:

                  channel_4_used.append(channel_4)
                  channels_5 = [channel for channel in channels_4 if channel not in channel_4_used]
                  channel_5_used = []
                  channels_5_redux = [channel for channel in channels_5]

                  if num_channels == 6:

                    channels_5_redux.pop()

                  for i in range(len(channels_5_redux)):
                    channel_5 = channels_5_redux[i]

                    if num_channels == 6:
                      channel_5_used.append(channel_5)
                      channels_6 = [channel for channel in channels_5 if channel not in channel_5_used]
                    
                      for i in range(len(channels_6)):
                        channel_6 = channels_6[i]

                        self.group = [channel_1, channel_2, channel_3, channel_4, channel_5, channel_6]
                        converted = self.convert_freq_abbreviations()
                        print(self.group)
                        self.score(converted)
                        if self.scores[1] != None:
                          if self.scores[1] >= score_limit: 
                            self.export()

                        combo_count += 1
                        if combo_count == (int(base_case)):
                          return
                  
              
                    else:

                      self.group = [channel_1, channel_2, channel_3, channel_4, channel_5]
                      print(self.group)
                      converted = self.convert_freq_abbreviations()
                      self.score(converted)
                      if self.scores[1] != None:
                        if self.scores[1] >= score_limit: 
                          self.export()

                      combo_count += 1
                      if combo_count == (int(base_case)):
                        return 
         
                else:

                  self.group = [channel_1, channel_2, channel_3, channel_4]
                  print(self.group)
                  converted = self.convert_freq_abbreviations()
                  self.score(converted)
                  if self.scores[0] >= score_limit:
                    self.export()

                  combo_count += 1
                  if combo_count == (int(base_case)):
                    return


            else:

              self.group = [channel_1, channel_2, channel_3]
              print(self.group)
              converted = self.convert_freq_abbreviations()
              self.score(converted)
              if self.scores[0] >= score_limit:
                self.export()  

              combo_count += 1
              if combo_count == (int(base_case)):
                return
              
            
          
def factorial(n, limit=None):

  
  if limit != None:
    if limit == 1:
      return n

  if n == 1:
    return n
  
  else:
    
    if limit != None:
      return n * factorial(n-1, limit-1)
    
    else:
      return n * factorial(n-1)
'''      



