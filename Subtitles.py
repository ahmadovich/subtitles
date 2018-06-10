'''
Author: Ahmad Hamdy
Date: April 2018
Purpose: manage media subtitles
Travese directory structure
Identify directories with video and subtitles
Make sure video and subtitles filenames match
Fix subtitle fonts encoding issues
'''

import argparse
import os
from chardet import detect

# Set working dir with a default of '.'
parser = argparse.ArgumentParser('Manage media subtitles\n\n\
Subtitles.py ')
parser.add_argument('-d', '--dir', required = True, type = str, default = '.', metavar = '', help = 'Path to media directory')

# add mutual exclusve options with a default of 'listfiles only'
mutz1= parser.add_mutually_exclusive_group()
mutz1.add_argument('-l', '--listfiles', action = 'store_true', help = 'list all found media and subtitle files' )
mutz1.add_argument('-a', '--all', action = 'store_true' , help = 'listfiles, rename and fix encoding for all found media subtitles')
mutz1.add_argument('-r', '--ren', action = 'store_true' , help = 'Rename subtitles to match media')
mutz1.add_argument('-f', '--fix', action = 'store_true' , help = 'Fix encoding for all found media subtitles')

args = parser.parse_args()

class CoupleFiles():
    def __init__(self,subt,mediat,currentdir):
        '''
        This initiates the object, which contains the filenames
        and the methods which operate on them '''
       
        self.subt=subt #full subtitle filename
        self.mediat=mediat #full media filename
        self.cur = currentdir
        self.mediaroot = os.path.splitext(self.mediat)[0] # Name of media file without extension
        self.fixed=False
        if args.listfiles: 
            self.listfilesonly()
        if args.fix or args.all:
            self.fixfiles() 
        if args.ren or (args.all and not self.fixed):
            self.rename()
        
        else : 
            self.listfilesonly()
        
    def rename(self):
        ''' This method renames the subtitle file to match the media file name '''
        if os.path.splitext(self.subt)[0] ==  self.mediaroot:
            #print('Files match in:', self.cur)
            return 0
            
        try: 
            
            self.correct = os.path.join(self.mediaroot + '.srt')
            os.rename(self.subt, self.correct)
            print('.....\nRenaming files in:',self.cur)
            '''
            print using the new Pythong 3.x way, print each listfiles item in a new line
            print(*listfiles,sep='\n')
            '''
            print(*(os.listdir(self.cur)), sep = '\n')
            print('Files renamed successfully\n.....',end='')
            
            
        except:
            print('Error renaming file in:',self.cur)
            
    def listfilesonly(self): 
        print('.....') 
        print(self.cur,self.mediat,self.subt, sep = '\n')
        print('.....\n',end='')
    
    def fixfiles(self):
        
        try:
            with open(self.subt,'rb') as filetofix:
                raw=filetofix.read(1024)
                if 'utf' in detect(raw)['encoding'].lower():
                    print('.....')
                    print('Correct file encoding',self.subt)
                    print('.....')
                else:
                    filetofix.close()
                    print('.....')
                    print('.....Fixing file encoding:',self.subt)
                    with open(self.subt,'r',encoding='cp1256') as infile:
                        with open(os.path.join(self.cur,'___fixed___.srt'),'w',encoding = 'utf-8-sig') as outfile:
                            line = infile.read(1)
                            while line:
                                outfile.write(line)
                                line=infile.read(1024)
                    print('.....Done.')
                    print('.....Archiving old file and renaming new subtitle file')
                    infile.close()
                    outfile.close()
                    
                    os.rename(self.subt,self.mediaroot +'.srt.bak')
                    os.rename(os.path.join(self.cur,'___fixed___.srt'),self.mediaroot + '.srt')
                    print('.....Done.')
                    print('.....')
                    self.fixed=True
                            
                    
                
        except:
            print('.....Couldn\'t operate on file:',self.subt) 
            print('.....')   
            
            
def main():
    #debugging code
    #print(args.dir,args.all, args.listfiles,args.ren, args.fix)
    mediaexts = ['.mp4','.avi','.mkv','.m4v','.wmv','.mpg','.mpeg','.mov','.flv']
    if args.listfiles:
        print('listfiles enabled')
    if os.path.isdir(args.dir):
        for (curdir, subdirs, filenames) in os.walk(args.dir) :
            mediafiles = []
            subtitlefiles = []
            for file in filenames:
                #print(*(os.path.splitext(file)))
                if '.srt' in os.path.splitext(file.lower())[1]: #change filename to lowercase
                    subtitlefiles.append(file)
                #search for media extensions in lowercase filenames
                for catcher in mediaexts:
                    if catcher in file.lower():
                        mediafiles.append(file)
                
            if (len(subtitlefiles)== 1) and (len(mediafiles)== 1):
                
                fullmed = os.path.join(curdir,mediafiles[0])
                fullsubt = os.path.join(curdir,subtitlefiles[0])
                if (os.path.getsize(fullmed) > 10 and os.path.getsize(fullsubt) > 10) : 
                    mediaobject = CoupleFiles(fullsubt,fullmed,curdir)
                else:
                    print('.....')
                    print('Media or subtitle file doesn\'t contain enough data',fullmed,fullsubt,sep='\n')
                    print('.....')
                    

        
    else:
        print('.....')
        print("Path",args.dir,"is not a directory")
        print('.....')
        exit(1) # use echo %errorlevel% from dos to get the exit code

if __name__ == '__main__' : main()

'''
There is a bug in the script, when there is an ANSI file containing correct English characters
The script tries to transform it into utf-8, creates a new file and renames the old one but the new file
still contains ANSI encoding
Maybe check if encoding is latin-1 and if so leave it as it is
FIXED: used utf-8-sig (signed utf) while writing the files instead of utf-8
'''
