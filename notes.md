#run this in the folder where are xml files
#' python3 to_jason2017.py '
#This will result in a directory (by looking in all subdirectories) of xml files and their json veriosn.
#The directory name will be "json-data..." and files in it will be xmls and their json translations.
#If script fails at a file, it will place its json varsion in the folder "problematic_files"

There are two files to_jason2017.py and to_jason.py.
The difference is that to_jason.py works for 'new dataset' (e.g. version 2.1.),
whereas to_jason2017.py works for 'old' versions (webnlg2017 challange).

The dataset for webnlg2017 is added with both xml and their corresponding json files.
* That is, the xml files from webnlg2017 are alread transformed into json files in the folder webnlg-dataset-master-webnlg_challenge_2017_XML_JSON.

So, these scripts work (but how well we don't yet know, but at least they don't crash. After all, it's a script from xml to json...)
Since the script is there, so if there are bugs, we can further modify them (needless to say).
