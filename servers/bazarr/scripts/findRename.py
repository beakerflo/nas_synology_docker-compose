import os
from datetime import datetime

dateString = (datetime.now()).strftime("%Y%m%d_%H%M%S")

os.rename('/volume1/containers/services/bazarr/scripts/rename.sh', '/volume1/containers/services/bazarr/scripts/rename.sh_' + dateString + '.txt')

renameSrt = open('/volume1/containers/services/bazarr/scripts/rename.sh','a')

movies = '/volume2/movies'

for movieLanguage in os.listdir(movies):
	if movieLanguage != '.DS_Store':
		for movieFolder in os.listdir(movies + '/' + movieLanguage):
			if ' (' in movieFolder:
				for movieFile in os.listdir(movies + '/' + movieLanguage + '/' + movieFolder):
					if 'srt' in movieFile: 
						if 'synced' in movieFile:
							srtfile = '"' + movies + '/' + movieLanguage + '/' + movieFolder + '/' + movieFile + '"'
							
							syncedSrtFile = srtfile
							outOfSync = srtfile.replace('synced.','')
							newNameForOutOfSync = srtfile.replace('synced','downloaded')
							newNameForSyncedSrtFile = outOfSync
							
							renameSrt.write('mv ' + outOfSync + ' ' + newNameForOutOfSync + '\n')
							renameSrt.write('mv ' + syncedSrtFile + ' ' + newNameForSyncedSrtFile + '\n')
							
series = '/volume2/tvshows'

for serieLanguage in os.listdir(series):
	if serieLanguage != '.DS_Store' and serieLanguage != '@eaDir':
		for serieFolder in os.listdir(series + '/' + serieLanguage):
			if serieFolder != '.DS_Store' and serieFolder != '@eaDir':
				for serieSeason in os.listdir(series + '/' + serieLanguage + '/' + serieFolder):
					if serieSeason != '.DS_Store' and serieSeason != '@eaDir':
						for serieFile in os.listdir(series + '/' + serieLanguage + '/' + serieFolder + '/' + serieSeason):
							if 'synced' in serieFile:
								srtfile = '"' + series + '/' + serieLanguage + '/' + serieFolder + '/' + serieSeason + '/' + serieFile + '"'

								syncedSrtFile = srtfile
								outOfSync = srtfile.replace('synced.','')
								newNameForOutOfSync = srtfile.replace('synced','downloaded')
								newNameForSyncedSrtFile = outOfSync
								
								renameSrt.write('mv ' + outOfSync + ' ' + newNameForOutOfSync + '\n')
								renameSrt.write('mv ' + syncedSrtFile + ' ' + newNameForSyncedSrtFile + '\n')
