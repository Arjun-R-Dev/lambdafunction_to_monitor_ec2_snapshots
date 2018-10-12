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
        
        for region in regions:
            reg=region['RegionName']
            ec2 = boto3.client('ec2', region_name=reg)
            result = ec2.describe_volumes( Filters=[{'Name': 'status', 'Values': ['in-use']}])
        
            for volume in result['Volumes']:
                result1 = ec2.describe_snapshots(Filters=filters)
            
                for snapshot in result1['Snapshots']:
                    time = snapshot['StartTime'].replace(tzinfo=None)
                    print time.date()
                    if snapshot['VolumeId'] == volume['VolumeId']:
                        if time.date() > datetime.date.today() - datetime.timedelta(days=7):
                            
                            ak.append("snapshot has been taken for the volume %s today and the snapshot ID is : %s "% (volume['VolumeId'] , snapshot['SnapshotId']))
                            break
                        else:
                            aj.append("No backup taken for today for the volume %s  " % (volume['VolumeId']))
                            
                            break
        return (aj,ak)
    out = test()
    print (out)
    def mail(out):
        message = json.dumps(out)
        client = boto3.client('sns')
        arn = 'arn of your sns topic'
        response = client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
        )
    mail(out)
