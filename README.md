## What the script does

The web archiving crawler [heritrix](https://github.com/internetarchive/heritrix3) heritrix generates specific log and report files.
This script selects certain outputs of these log and reports files and writes the output as the line in a csv file.

The values that are given out are 
- the number of successfully and unsuccessfully crawled urls and the ratio of unsuccessfully crawled urls, furthermore
- the number of 2xx, 3xx, 4xx and 5xx HTTP responses and the single digit reponses that indicate a [heritrix error status](https://heritrix.readthedocs.io/en/latest/glossary.html#status-codes) and the ratio of errors indicated by these status codes

The script has only been tested in a Linux Debian environment.

## Running

- The file location of the output statistic csv is hard coded in statForFolder.py as output_file.
- statForFolder.py and statForFile.py need to be in the same folder.
- To start the script, just run the statForFolder.py script, it will then call the statForFile script itself.
  The script starts looking for heritrix job folders, identifying them by their 14 digit timestamp folder name, starting from the folder the script is started from.
  So it speeds up the to navigate to the folder where the jobs lie before starting the script.


The comments in the scripts are in German - if you need help with that, let us know.
