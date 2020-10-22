def remove_header(location):
    """
    doc
    """
    n=location.find('.')
    file=open(location)
    lines=file.readlines()
    file2=open(location[:n]+'_headless'+location[n:],"a")
    file2.writelines(lines[1:])
    file.close()
    file2.close()
    return(None)
