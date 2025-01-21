#! /bin/python

# statForJob.py muss im selben Ordner liegen wie statForFolder.py
import statForJob as jobstat
import os

# Voreinstellungen: Statistik wird für Ordner angelegt, in dem man sich bei Programmaufruf befindet.
input_path = os.getcwd()
# Statistik wird in festgelegtes Dokument geschrieben
output_file = '/home/archiv/QS/statistik-test2.csv'
new_header = False
# Hierüber kann eingestellt werden, ob eine Kopfzeile gewünscht ist. 
# Durch Auskommentieren lässt sich die Funktion abstellen.
# new_header = jobstat.set_header()

# Variablen für Ablaufsteuerung
folder_or_job = ""
n = 0
end = input_path[-14:]
print(end)

# Test: Handelt es sich um einen einzelnen Job-Ordner (Ordner hat Namen des Timestamps)
# oder um einen Ordner, der durchlaufen werden soll, um einzelne Jobs zu finden?	 
try:
#if True:
	# Test konkret: lassen sich die letzten 14 Stellen in Integer umwandeln?
	# Falls ja: Einzeljob ("job"), falls Exception: Ordner durchlaufen ("folder").	
	directoryTest = int(end)
	directory = end
	folder_or_job = "job"	
	print(directory)
	
	#if True:
	try:
	# Statistik mit Parametern für Einzeljob wird aufgerufen
		jobstat.job_stat(folder_or_job, directory, input_path, output_file, new_header)
		n = n+1
	#if False:
	except: 
		print("Fehler beim Versuch, den Einzeljob auszuwerten.")	

# Es handelt sich nicht um einen Ordner mit Timestamp als Namen. 
#if False:
except:
	print("except")
	folder_or_job = "folder"
	# Der Ordner wird durchlaufen auf der Suche nach einem Einzeljob.
	for dirpath, dirnames, files in os.walk(input_path):

		print(dirpath)
		print(dirnames)
		#print(files)	
	
		for directory in dirnames:
			# Funktioniert nur für Jobs, die zwischen 2000 und 2099 angelegt sind...
			if directory.startswith("20"):
				print(new_header)
				print(n)
				# Test, ob Kopfzeile in Tabelle angelegt werden soll.
				if (n > 0):
					new_header = False
				print(directory)
				print(dirpath)
				print(output_file)
				# Aufruf der Funktion für Jobstatistik mit Parametern für mehrere Jobs im Ordner
				jobstat.job_stat(folder_or_job, directory, dirpath, output_file, new_header)
				# Kopfzeile soll nur einmal angelegt werden.				
				n = n+1



if (n == 0):
	print("Kein Job-Ordner gefunden.")
			


#jobstat.job_stat()
