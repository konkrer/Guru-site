from django.shortcuts import render
from .libr import FreqSet1


def analyze(request):
    if request.method == 'POST':
        if request.POST['channel_group']:

            input_group_init = request.POST['channel_group'].split(' ') 
            input_group = [x.lower() for x in input_group_init if x != '']
          
            if len(input_group) > 1:
                
                if  len(input_group) > 8:
                	return render(request, "ace/ace.html", {'error': 'Too many channels'})
            
                for chan in input_group:
                    if not FreqSet1.check_channel_input(chan):
                        return render(request, 'ace/ace.html', {'error': 'Channel entry incorrect'})

                x = FreqSet1.FreqSet(input_group)

                converted = x.convert_freq_abbreviations()

                # IMD frequencies for display
                imd_freqz = x.check_freqz(converted)                
                replace = 1
                imd_freqz_numbered = []
                for sublist in imd_freqz:                
                    sublist.insert(0, converted[replace-1]) # insert channel
                    sublist.insert(replace, "") # insert space
                    replace += 1
                    enumd = enumerate(sublist)
                    imd_freqz_numbered.append(enumd)


                # get IMD warnings and printable channel abbreviations.
                warnings, printable = x.analyze_interference(converted, printz=False)
                
                # get scores and other analytics
                score_alt, score_alt_weighted, closest_broadcast, IMD_score, divide_by, IMD_close_to_chan, closest_imd = x.score(converted, printz=False)

                # dictionary for passing data to html document
                info_dic = {'score_alt': score_alt, 'score_alt_weighted': score_alt_weighted, 'closest_broadcast': closest_broadcast, \
                	'IMD_score': IMD_score, 'divide_by': divide_by, 'IMD_close_to_chan': IMD_close_to_chan, 'closest_imd': closest_imd, \
                	'warnings': warnings, 'printable': printable, 'converted': converted, 'imd_freqz': imd_freqz_numbered}

                return render(request, 'ace/ace2.html', info_dic)
            
            else:
                return render(request, 'ace/ace.html', {'error': 'Enter more than one channel'})

        else:
            return render(request, "ace/ace.html", {'error': 'All fields required'})

    else:
        return render(request, 'ace/ace.html')