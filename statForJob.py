#!/bin/python

import os
import csv


#Funktionen, die aufgerufen werden, um einzelne Logs/Reports auszuwerten

def progress_stat(path):
	#print("progress-statistics-Dummy")
	pass

# Crawl-Report: Gibt Gesamtzahl der verarbeiteten, fehlgeschlagenen und erfolgreichen URIs zurück.
# Worauf sich die Bewerung von success und failure bezieht, ist (mir) aber unklar. 
# Response-Code-Auswertung ist hier sprechender.
def crawl_report_stat( path ):
	#print("crawl-report")
	crawl_report = open(path)

#	inputlines = []
	URIs = {}
	for line in crawl_report:
#		inputlines.append(line) 	
#	for line in inputlines:
#		print(line)
		if line.startswith("crawl status"):
			status = line[14:].strip()
			URIs["status"]=status
		elif line.startswith("URIs processed"):
			doppelpunkt = line.find(":")			
			verarbeitet = line[(doppelpunkt + 2):-1]
#			print("Verarbeitet: " + verarbeitet + "\n")
			URIs["processed"] = verarbeitet 
		elif line.startswith("URI successes"):			
			doppelpunkt = line.find(":")			
			erfolgreich = line[(doppelpunkt + 2):-1]
#			print("Erfolgreich: " + erfolgreich + "\n")
			URIs["success"] = erfolgreich 
		elif line.startswith("URI failures"):
			doppelpunkt = line.find(":")
			fehlgeschlagen = line[(doppelpunkt + 2):-1]
#			print("Nicht erfolgreich: " + fehlgeschlagen + "\n")
			URIs["failure"] = fehlgeschlagen
		elif line.startswith("total crawled bytes"):
			doppelpunkt = line.find(":")			
			groesse = line[(doppelpunkt + 2):-1]
			URIs["size"] = groesse
		#print(URIsfailures, URIsprocessed, URIssuccess)
	crawl_report.close()
	return URIs

# Gibt TRUE zurück, wenn alle Seeds entweder mit 2xx oder 3xx-Code gecrawlt worden sind, 
# sonst FALSE
def seeds_rep_stat(path):
	all_crawled = True
	with open(path) as seeds_rep:
		for line in seeds_rep:
			if line.startswith("["):
				pass
			elif line.startswith("2"):
				pass
			elif line.startswith("3"):
				pass
			else: all_crawled = False
	return all_crawled

# Gibt Anzahl der Response-Codes zurück: Gesamtzahl, Codes nach 2xx, 3xx, 4xx, 5xx.
# 403-Fehler werden zusätzlich in eigener Variable gezählt.
# Außerdem einstellige Codes: zB DNS-Aufruf und negative: Heritrix-Fehler-Codes,
# sowie "Sonstiges". 

def response_code_stat(path):
	rAll = 0
	r5xx = 0
	r4xx = 0
	r403 = 0
	r2xx = 0
	r3xx = 0
	rNeg = 0
	rSingle = 0	
	rElse = 0
	with open(path) as res_code:
		res_code.readline()
		for line in res_code:
			line = line.split(" ")
			urls = int(line[0]) 
			rAll += urls
			code = line[1].strip()
#			if (int(code) > 99):
#				print(code[-3])
#			print(urls)
#			print(code)
			if ("-" in code):
				rNeg = rNeg + urls
			elif (int(code) < 100):
				rSingle = rSingle + urls
			elif (code[-3] == "2"):
				r2xx = r2xx + urls
			elif (code[-3] == "3"):
				r3xx = r3xx + urls
			elif (code[-3] == "4"):
				r4xx = r4xx + urls
				if code == "403":
					r403 = urls
			elif (code[-3] == "5"):
				r5xx = r5xx + urls
			else:
				rElse = rElse + urls
	response_dict = {'r2xx' : r2xx, 'r3xx' : r3xx, 'r4xx' : r4xx, 'r403' : r403, 'r5xx' : r5xx, 
			'rNeg' : rNeg, 'rSingle' : rSingle, 'rElse' : rElse, 'rAll' : rAll}

	return response_dict


# Funktion, um Eingabepfad anzulegen
def set_input_path():

	#Eingabe von Pfad, unter dem Job gespeichert ist - kann auch per Drag'n'Drop ins Terminal gezogen werden.
	jobpath = input("Pfad des Jobordners:").strip()
	#print(jobpath)
	jobpath = jobpath.strip("\'")
	return jobpath
	#print(jobpath)	

# Funktion für Pfad zu Ausgabe-Datei
def set_output_file():

	#Eingabe von Dokument (mit Pfad), in dem Statistik gespeichert werden soll - falls es nicht existiert, wird es angelegt.
	outputpath = input("Wohin soll Statistik geschrieben werden?").strip()
	outputpath = outputpath.strip("\'")
	return outputpath

# Funktion, um festzulegen, ob eine neue Kopfzeile angelegt werden soll.
# Per Default ist diese Variable in statForFolder auf False gesetzt, die Abfrage  
# kann also in statForFolder
# durch Auskommentieren einfach deaktiviert werden.
def set_header():
	header = input("Soll eine neue Kopfzeile angelegt werden? j/n \n")
	if (header == "j"):
		header = True
	elif (header == "n"):
		header = False
	else:
		header = input("Eingabe j oder n, bei anderer Eingabe wird Nein gesetzt. \n")
		if header == "j":
			header = True	
	return header
	print(header)


# Diese Funktion legt eine statistische Auswertung eines einzelnen Crawl-Jobs an 
# als Zeile in einer CSV-Datei. 
# Parameter: 
# folder_or_job: string, "job" oder "folder" als akzeptierte Werte, benötigt für Prozesssteuerung
# directory: string, gibt Timestamp des Jobs an, also crawl_date
# jobpath: string, unterscheidet sich, je nachdem ob es sich um einen Einzeljob handelt, o
def job_stat(folder_or_job, directory, jobpath, outputpath, header):	
	
#	print("called")
#	print(folder_or_job, directory, jobpath, outputpath, header)				

	# Default-Werte für Variablen deklariert
	# Stehen die Default-Werte in der Ausgabe-Tabelle, existieren die entsprechenden
	# Logs/Reports wahrscheinlich nicht, meist, weil der Job nocht nicht abgeschlossen 
	# oder unerwartet abgebrochen worden ist.
	crawlrepstat = {}
	crawl_name = "?"
	crawl_date = directory
	URIsprocessed = "?"
	URIssuccess = "?"
	URIsfailures = "?"
	errorquota = -1
	crawlstatus = "?"
	crawl_size = -1
	warc_size = 0
	warc_number = 0	
	res5xx = 0
	res4xx = 0
	res403 = 0
	res2xx = 0
	res3xx = 0
	resNeg = 0
	resSingle = 0
	resElse = 0
	resAll = 0
	all_seeds_crawled = "?"

	if (folder_or_job == "folder"):

		#Name und Datum des Crawls werden aus Pfad gewonnen
		job_index = jobpath.find("/jobs/")
		crawl_name = jobpath[job_index + 6:]
		#print(crawl)
#		date_index = crawl.find("/")
#		crawl_name = crawl[:date_index]
#		crawl_date = crawl[date_index+1:date_index+15]
		print(crawl_name)
#		print(crawl_date)

#		print(jobpath + directory)
		walkpath = (jobpath + "/" + directory)
	
	elif (folder_or_job == "job"):
		job_index = jobpath.find("/jobs/")
		crawl_name = jobpath[job_index + 6:-15]
		#print(crawl)
#		date_index = crawl.find("/")
#		crawl_name = crawl[:date_inde]

		walkpath = (jobpath)
#		print(walkpath)

	else:
		print("???")

	
					
		
	# Job-Ordner, der oben eingegeben worden ist, wird durchlaufen, bei relevanten Dokumenten wird 
	# Funktion aufgerufen
	for dirpath, dirnames, files in os.walk(walkpath):
#		print("Dirpath: " + dirpath)
#		print (dirnames)
		
		for dirname in dirnames:		
			if (dirname == "warcs"):
				print("Dirpath von warcs:" + dirpath)
				warc_folder_path = os.path.join(dirpath, dirname)
				for dpath, dnames, fls in os.walk(warc_folder_path):
#					print(warc_folder_path)
					for fl in fls:
						warc_number += 1
						warc_path = os.path.join(warc_folder_path, fl)
						print(warc_path)
						print(os.path.getsize(warc_path))
						warc_size += os.path.getsize(warc_path)
						print(warc_size)
						
			
		for file_name in files:
			if (file_name.startswith("progress-statistics")):
				progress_stat(dirpath + "/progress-statistics.log")
			if (file_name.startswith("crawl-report.txt")):
				crawlrepstat = crawl_report_stat(dirpath + "/crawl-report.txt")
				crawlstatus = crawlrepstat["status"]			
				URIsprocessed = crawlrepstat["processed"]
				URIsfailures = crawlrepstat["failure"]
				URIssuccess = crawlrepstat["success"]
				crawl_size = crawlrepstat["size"]
			if (file_name.startswith("responsecode-report")):
				rescodestat = response_code_stat(dirpath + "/responsecode-report.txt")
				res5xx = rescodestat['r5xx']
				res4xx = rescodestat['r4xx']
				res403 = rescodestat['r403']
				res3xx = rescodestat['r3xx']
				res2xx = rescodestat['r2xx']
				resNeg = rescodestat['rNeg']
				resSingle = rescodestat['rSingle']
				resElse = rescodestat['rElse']
				resAll = rescodestat['rAll']
	#			print (rescodestat)
				 
			if (file_name.startswith("seeds-report")):
				seedsstat = seeds_rep_stat(dirpath + "/seeds-report.txt")
				all_seeds_crawled = seedsstat



				

	# Aus ausgelesenen Werten werden statistische Werte berechnet.			
	try:
		errorquota = (int(URIsfailures)/int(URIsprocessed))*100
	except:
		errorquota = -1
	#print(f"Die Fehlerquote beträgt {errorquota} Prozent.")

	try:
		httperrorquota = ((res4xx+resNeg+res5xx)/resAll)*100
	except: 
		httperrorquota = -1

	try:
		http403errorquota = ((res403)/resAll)*100
	except: 
		http403errorquota = -1

	try:
		httpclienterrorquota = ((res4xx)/resAll)*100
	except: 
		httpclienterrorquota = -1

	try:
		httpservererrorquota = ((res5xx)/resAll)*100
	except: 
		httpservererrorquota = -1


	# Ausgabe der ausgelesenen und errechneten Werten im angegebenen File
	
	with open(outputpath, "a") as statfile:
		print(crawlrepstat)
		writer = csv.writer(statfile)
		if header:
			writer.writerow(["Crawl-Name", "Craw_Date", "Status", "verarbeitet", "erfolgreich", "nicht erfolgreich", 
				"Fehlerquote \n(URIs), in %", "Crawl-Größe", "WARC-Größe", "WARC-Anzahl", "Alle Seeds\ngecrawlt?", "2xx", "3xx","4xx",
				"403", "5xx","Negativ","Einstellig","Response\nSonstiges", "Alle", "Http-Fehlerquote\nin Prozent", 
				"Http-Fehlerquote\nclientseitig, in Prozent", "Http-Fehlerquote\nserverseitig, in Prozent", 
				"403-Fehlerquote\nin Prozent"])
		writer.writerow([crawl_name, crawl_date, crawlstatus, URIsprocessed, URIssuccess, URIsfailures,
		 		errorquota, crawl_size, warc_size, warc_number, all_seeds_crawled, res2xx, res3xx, res4xx, res403, res5xx, resNeg, 
				resSingle, resElse, resAll, httperrorquota, httpclienterrorquota, httpservererrorquota, 
				http403errorquota])

#job_stat()

