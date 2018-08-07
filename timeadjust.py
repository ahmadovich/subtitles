import re
import random
import argparse
import os

def modifytime(infile,mydelta):
    ignored_lines = 0
    #This will compile a pattern for 5 different regex groups.
    pattern = re.compile(r'(\d\d:\d\d:\d\d,\d\d\d)(\s*)(-->)(\s*)(\d\d:\d\d:\d\d,\d\d\d)')
    
    # Open temp file for writing correct subtitles
    
    with open(os.path.split(args.subfile)[0]+'\\fixed.srt','w') as outfile:
            
        for lines in infile:
                match = re.search(pattern,lines)
                # Start editing times
                if match:
                    starttime = (match.group(1)).split(':') #Time start
                    endtime = (match.group(5)).split(':') #Time end
                    start_seconds_split = starttime[2].split(',')
                    start_seconds = int(start_seconds_split[0]) + (float(start_seconds_split[1]) / 1000)
                    start_total_seconds = ((int(starttime[0]) *3600) + (int(starttime[1]) *60) + float(start_seconds)) + mydelta
                    end_seconds_split = endtime[2].split(',')
                    end_seconds = int(end_seconds_split[0]) + (float(end_seconds_split[1]) / 1000)
                    end_total_seconds = ((int(endtime[0]) *3600) + (int(endtime[1]) *60) + float(end_seconds)) + mydelta
                    #check if new value is less than 0 ( not allowed ), we can check on start time only if we want.
                    if start_total_seconds < 0  or end_total_seconds < 0:
                        ignored_lines += 1
                        #if new time is < 0 then keep the original timing for start and end
                        new_start_formatted = match.group(1)
                        new_end_formatted = match.group(5)
                        if ignored_lines > 5 :
                            print('Exiting, too many lines were ignored, more than five lines')
                            outfile.close()
                            print('Removing temp file')
                            os.remove(os.path.split(args.subfile)[0]+'\\fixed.srt')
                            exit(2)
                        else:
                            newlineformatted = new_start_formatted +' '+'-->'+' '+new_end_formatted
                            outfile.write(str(newlineformatted) + '\n')
                    else:
                        # Here we calculate new time and put it in the correct string format
                        new_start_formatted = formattime(start_total_seconds)
                        new_end_formatted = formattime(end_total_seconds)
                        newlineformatted = new_start_formatted +' '+'-->'+' '+new_end_formatted
                        outfile.write(str(newlineformatted ) + '\n')
                            
                                                                           
                else:
                    outfile.write(lines)
                    # here we should write other lines, like subtitles itself unchanged to the new file
        print('Subtitle time adjusted')            
def formattime(time): 
    hour = int(time // 3600)
    time %= 3600
    minutes = int(time // 60)
    time %= 60
    seconds = int(time)
    milliseconds = int((time - seconds) * 1000)
    return (str(hour).zfill(2)+':'+str(minutes).zfill(2)+':'+str(seconds).zfill(2)+','+str(milliseconds).zfill(3))

def files_rename():
    if args.delete: 
       os.remove(args.subfile)
       print('Removed old subtitle file')
    else:
        random_name = os.path.split(args.subfile)[0]+'\\'+str(random.randint(1,9999999))+'.srt'
        os.rename(args.subfile,random_name)
        print('Copy of original subtitle file saved as ' + random_name)
    
    os.rename(os.path.split(args.subfile)[0]+'\\'+'fixed.srt',args.subfile)
          
def main(file,delta_seconds):    
   
    with open(file,'r') as infile:
        if  abs(delta_seconds) < 600 :
            modifytime(infile, delta_seconds)
        else:
            print('Allowed change should be no more than 10 minutes')
            exit(1)
    files_rename()
            
# start by getting parameters
parser = argparse.ArgumentParser('timeadjust')
parser.add_argument('-f', '--subfile', required = True, type = str, metavar = '', help = 'Path to subtitle file')
parser.add_argument('-s', '--secondsdelta', type = float, default = -3, metavar = '', help = 'Time adjustment in seconds')
parser.add_argument('-d', '--delete', action = 'store_true' , help = 'Don\'t keep original files')            
args = parser.parse_args()

if __name__ == '__main__': main(args.subfile,args.secondsdelta)        


''' Create timelist for each line of timings, which is a list with two members
then split each member of the list into 3 (or 4) integers
add or delete the desired change

convert everything into seconds
allow only a maximum of +- 10 minutes of adjustment
check if the value is a negative timing and ignore it for the first 3 subtitles only
'''
