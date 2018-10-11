# lambdafunction to monitor ec2 snapshots

Prerequisite : running ec2 instances 
              snapshots with a tag key
              arn of the sns topic to send mail
              IAM role to access sns , cloudwatch and ec2
Create a lambda function with the IAM role which has the policy attached.
Paste the python code in it.
Run the script.
