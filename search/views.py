from django.shortcuts import render, redirect
from .libr import finder, FreqSet1


def search(request):

	if request.method == "POST":
		try:
			if request.POST['num_pilots'] and request.POST['chan_choices']:
				# allow empty list input
				if not request.POST['channel_group']:
					input_group = []
				# check channel inputs if inputs given
				else:
					input_group_init = request.POST['channel_group'].strip().split(' ')         		
					input_group = [x.lower() for x in input_group_init if x != '']

					if  len(input_group) > 10:
						return render(request, "search/search.html", {'error': 'Too many channels'})

					for chan in input_group:
						if not FreqSet1.check_channel_input(chan):
							return render(request, 'search/search.html', {'error': 'Channel entry incorrect'})

				# study set  choice logic
				if request.POST['chan_choices'] == "USA legal only":
					usa_only_ = True
					add_lowband_ = False
				elif request.POST['chan_choices'] == "40 channel":
					usa_only_= False
					add_lowband_= False
				elif request.POST['chan_choices'] == "40 chan plus lowband":
					usa_only_= False
					add_lowband_= True

				num_pilots = request.POST['num_pilots']

				# lock channels logic
				lock_chan_all_init = ['lock_chan1', 'lock_chan2', 'lock_chan3', 'lock_chan4', 'lock_chan5', 'lock_chan6']

				if len(input_group) < int(num_pilots):
					lock_limit = len(input_group)
				else:
					lock_limit = int(num_pilots)

				# look for relevant lock input and create list of indices of locked channels
				lock_chan_all = lock_chan_all_init[:lock_limit]
				lock_chan_idx_ = []
				for i in range(len(lock_chan_all)):
					try:
						if request.POST[lock_chan_all[i]]:
							# append indices of channels to lock in input_group
							lock_chan_idx_.append(request.POST[lock_chan_all[i]])
					except KeyError:
						pass


				# pass data to finder.smartlookup
				output_list, channels_abbrev, digit_list = finder.smart_lookup(num_pilots=num_pilots, usa_only=usa_only_, 
				group_to_find=input_group, E_extra_max=request.POST['40_avilb'], add_lowband=add_lowband_, 
				L_max=request.POST['low_avilb'], printz=False, lock_chan_idx=lock_chan_idx_)

				# create output list of locked channels
				locked_channels = []
				for idx in lock_chan_idx_:
					locked_channels.append(channels_abbrev[int(idx)])

				# if nothing found
				if output_list == []:
					error_addit = ''			 
					if (usa_only_ == True):
						if ('e4' in input_group) or ('e7' in input_group) or ('e8' in input_group): # 
							error_addit = "E4, E7, and E8 cannot be found in USA only. "
						if (num_pilots == '6'): 
							error_addit += ' Only 8 channel groups in this table. Leave search entry blank to see whole list.'
					elif (request.POST['40_avilb'] == '0'):
						if ('e4' in input_group) or ('e7' in input_group) or ('e8' in input_group): # 
							error_addit = "E4, E7, and E8 cannot be found when no 40 chan VTX avilable. "

					return render(request, 'search/search.html', {'error': 'Nothing found!', 'error_addit': error_addit, 'num_pilots': num_pilots,
				 	'chan_choices': request.POST['chan_choices'], '40_avilb': request.POST['40_avilb'],
				 	'low_avilb': request.POST['low_avilb'], 'channels_abbrev': channels_abbrev, 'channels_freqz': digit_list, 
				 	'locked_channels': locked_channels})

				# output list creation

				top = output_list[0]
				if input_group == []:
					top_label = 'Top scoring'
				else:
					top_label = len(output_list)
				two_label = "No"
				three_label = "No"
				two = []
				three = []

				# add output data if it's there
				if len(output_list) > 1:
				    two = output_list[1]
				    two_label = (top_label - 1) 
				if len(output_list) > 2:
				    three = output_list[2]
				    three_label = (top_label - 2)
				    # in case the three lists are identical ignore the second two
				    if (output_list[0] == output_list[1]) and (output_list[0] == output_list[2]):
				    	two_label = "No"
				    	three_label = "No"

				# additional information relevant to the conditions set
				chan_choices_addit = ''
				if (usa_only_ == True):
					if ('e4' in input_group) or ('e7' in input_group) or ('e8' in input_group): # 
						chan_choices_addit = "E4, E7, and E8 cannot be found in USA only. "
				elif (request.POST['40_avilb'] == '0'):
					if ('e4' in input_group) or ('e7' in input_group) or ('e8' in input_group): # 
						chan_choices_addit = "E4, E7, and E8 cannot be found when no 40 chan VTX avilable. "

				if (usa_only_ == True) and (num_pilots == '5'):
					chan_choices_addit += ' Top scoring USA 5 channel group has weighted VCS of 84.0'
				if (usa_only_ == True) and (num_pilots == '6'):
					chan_choices_addit += ' Top scoring USA 6 channel group has weighted VCS of 65.6'
				elif (add_lowband_ == True) and (num_pilots == '6'):
					chan_choices_addit += ' Lowband 6 channel groups scores are 83.3 and above, weighted.'

				return render(request, 'search/search2.html', {'top':top, 'two': two, 'three': three, 'top_label': top_label, 
					'two_label': two_label, 'three_label': three_label, 'num_pilots': num_pilots, 'channels_abbrev': channels_abbrev,
				 	'channels_freqz': digit_list, 'chan_choices': request.POST['chan_choices'], '40_avilb': request.POST['40_avilb'],
				 	'low_avilb': request.POST['low_avilb'], 'chan_choices_addit': chan_choices_addit, 'locked_channels': locked_channels})

		except KeyError:
			return render(request, 'search/search.html', {'error': 'All fields required'})
	else:
		return render(request, 'search/search.html')