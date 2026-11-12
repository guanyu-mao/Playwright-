import os
def write_to_log(msg:str):
    # write the log to the download location folder
    folder=os.getenv('download_location')
    org = org_short_name

    with open(folder+org+'_'+formatted_datetime+'_'+'log.txt', 'w') as file:
        file.write(msg)
