from django.shortcuts import render

def home(request):
	return render(request, "home.html")

def scores(request):
	return render(request, "scores.html")

def IMD(request):
	return render(request, "IMD.html")

def metrics(request):
	return render(request, "metrics.html")

def boxplot(request):
	return render(request, "metrics/box_plot.html")

def piechart(request):
	return render(request, "metrics/piechart.html")

def chan_occur(request):
	return render(request, "metrics/chan_occur.html")

def scores_bar(request):
	return render(request, "metrics/scores_bar.html")

def bands_bar(request):
	return render(request, "metrics/bands_bar.html")

def freq_dist(request):
	return render(request, "metrics/freq_dist.html")