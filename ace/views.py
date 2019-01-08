from django.shortcuts import render
from .libr import FreqSet1


def analyze(request):
    if request.method == 'POST':
        if request.POST['channel_group']:

            input_group_init = request.POST['channel_group'].split(' ')           
            if len(input_group_init) > 1:
                input_group = [x for x in input_group_init if x != '']

                if  len(input_group) > 8:
                	return render(request, "ace/ace.html", {'error': 'Too many channels'})
            
                for chan in input_group:
                    if not FreqSet1.check_channel_input(chan):
                        return render(request, 'ace/ace.html', {'error': 'Channel entry incorrect'})

                x = FreqSet1.FreqSet(input_group)

                converted = x.convert_freq_abbreviations()
                imd_freqz = x.check_freqz(converted)

                warnings, printableish, converted = x.analyze_interference(converted, printz=False)
                printable = [x.upper() for x in printableish]


                score_alt, score_alt_weighted, closest_broadcast, IMD_score, divide_by, IMD_close_to_chan, closest_imd = x.score(converted, printz=False)

                info_dic = {'score_alt': score_alt, 'score_alt_weighted': score_alt_weighted, 'closest_broadcast': closest_broadcast, \
                	'IMD_score': IMD_score, 'divide_by': divide_by, 'IMD_close_to_chan': IMD_close_to_chan, 'closest_imd': closest_imd, \
                	'warnings': warnings, 'printable': printable, 'converted': converted, 'imd_freqz': imd_freqz}

                return render(request, 'ace/ace2.html', info_dic)
            
            else:
                return render(request, 'ace/ace.html', {'error': 'Enter more than one channel'})

        else:
            return render(request, "ace/ace.html", {'error': 'All fields required'})

    else:
        return render(request, 'ace/ace.html')