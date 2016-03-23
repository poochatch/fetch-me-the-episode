class FileManagement():
    """ Handle files:
    torrent_history.txt - information about previously downloaded torrents
    download_history.txt - iformation about previos torrent client lauches
    series_table.txt - information about correct series urls
    
    there is only one instance of this class (Singleton),
    holding data about every file it handled. """

    def __init__(self, file_name):
        self.file_name = file_name
        self.load_file_into_buffer(file_name)

    def load_file_into_buffer(self, file_name):
        # load a file into a buffer in memory and close it
        self.file = open(PATH + '/configuration/' + file_name, 'r')
        self.parse_file(self.file)

    def parse_file(self,file):
        # parse *txt file into python data representation
        self.buffer = []
        lines = file.readlines()
        comments = []
        for _line in range(len(lines)):
            temp = []
            if lines[_line].startswith('#'):
                comments.append(lines[_line].split(' '))
            else:
                temp = lines[_line].split(',')
                if self.is_correct(temp, _line):
                    self.buffer.append(temp)
        self.file.close()
        self.save_buffer(comments)

    def is_correct(self, data, line_nr):
        lenghts = { 'download_history.txt': len(data)!=6,
                    'torrent_history.txt':  len(data)!=3,
                    'series_table.txt':     len(data)< 3     }
        if lenghts[self.file_name]:
            self.error_log(line_nr, data, 'Wrong entry lenght')
            return False
        for field in data:
            if field.startswith(('#',' ','\n', '\t', '\r')) or len(field)==0:
                self.error_log(line_nr, data, 'Invalid entry')
                return False
        return True
            
    def error_log(self, line_nr, data, err_descr):
        log = open(PATH + '/configuration/error_log.txt', 'a')
        error = ' '.join([time.strftime("%H:%M:%S %d %b %Y"),
                        err_descr,
                        'in line',
                        str(line_nr), 
                        'of',
                        self.file_name + ':' + '\t',
                        ','.join(data)])
        log.write(error)
        log.close()

    def update_buffer(self, data):
        if self.is_correct(data,'NEW_ENTRY'):
            self.buffer.append(','.join(data))

    def save_buffer(self, comments):
        # flush buffer into a file
        file = open(PATH + '/configuration/' + self.file_name, 'w')
        for line in comments:
            entry = ' '.join(line)
            file.write(entry)
        file.write('\n')
        for line in self.buffer:
            entry = ','.join(line)
            file.write(entry)
        file.close()


