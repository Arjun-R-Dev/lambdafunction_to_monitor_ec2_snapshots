import boto3
from botocore.exceptions import ClientError
from datetime import datetime,timedelta
import datetime
import json
import subprocess

def lambda_handler(event, context):
    ak=list()
    aj=list()
    def test():
        filters = [{'Name': 'tag-key', 'Values': ['CreatedBy']}]

        ec2 = boto3.client('ec2')
        regions = ec2.describe_regions().get('Regions',[] )
        
        for region in regions: #search in all the region
            reg=region['RegionName']
            ec2 = boto3.client('ec2', region_name=reg)
            result = ec2.describe_volumes( Filters=[{'Name': 'status', 'Values': ['in-use']}])#store the volume details which are in use to the varilble result
        
            for volume in result['Volumes']:
                result1 = ec2.describe_snapshots(Filters=filters)#store the snapshot attributes to the variable result1
            
                for snapshot in result1['Snapshots']:
                    time = snapshot['StartTime'].replace(tzinfo=None)#get the time in which the snapshot was created
                    
                    if snapshot['VolumeId'] == volume['VolumeId']:
                        if time.date() > datetime.date.today() - datetime.timedelta(days=7):#if the date of the snapshot is greated than the retention date
                            #store the output to the list ak
                            ak.append("snapshot has been taken for the volume %s today and the snapshot ID is : %s "% (volume['VolumeId'] , snapshot['SnapshotId']))
                            break
                        else:
                            aj.append("No backup taken for today for the volume %s  " % (volume['VolumeId'])) #store the output to the list aj
                            
                            break
        return (aj,ak)#return the list to the functon call
    out = test()#save the output of function to the variable list
    #print (out) #uncommend it if you want see the output on lambda screen
    #function to send mail using the sns, We pass the variable out to this function
    def mail(out):
        message = json.dumps(out)
        client = boto3.client('sns')
        arn = 'arn of your sns topic'
        response = client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
        )
    mail(out)#function call for the mail function
