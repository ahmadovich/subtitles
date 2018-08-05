import re

def modifytime(infile,mydelta):
    
    #This will compile a pattern for 5 different regex groups.
    pattern = re.compile(r'(\d\d:\d\d:\d\d,\d\d\d)(\s*)(-->)(\s*)(\d\d:\d\d:\d\d,\d\d\d)')
    
    for lines in infile:
            match = re.search(pattern,lines)
            if match:
                starttime = (match.group(1)).split(':') #Time start
                endtime = (match.group(5)).split(':') #Time end
                seconds_split = starttime[2].split(',')
                seconds = int(seconds_split[0]) + (int(seconds_split[1]) / 1000)
                total_seconds = (int(starttime[0]) *3600) + (int(starttime[1]) *60) + seconds
                # You need to check delta before applying it, so that not to go out of range
                new_total = total_seconds + mydelta
                print ( new_total)
                
            else:
                pass
                #timelist = lines.split('-->',2)
                #timelist items are strings
                #print(timelist[0])
    
    
def main():    
    with open(r'D:\Python files\test\test\1\1.srt','r') as infile:
        modifytime(infile,-3)
          
if __name__ == '__main__': main()        


''' Create timelist for each line of timings, which is a list with two members
then split each member of the list into 3 (or 4) integers
add or delete the desired change'''
