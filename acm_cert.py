#!/usr/bin/python
try:
    import boto3
except ImportError:
    pass  # caught by imported HAS_BOTO3

from ansible.module_utils.basic import *
#client = boto3.client('acm')
import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ec2 import boto3_conn, ec2_argument_spec, get_aws_connection_info
from ansible.module_utils.ec2 import camel_dict_to_snake_dict, AWSRetry, HAS_BOTO3, boto3_tag_list_to_ansible_dict

def main():
   fields = {
         "Certificate":{"required": True, "type": "str"},
         "PrivateKey":{"required": True, "type": "str"},
         "CertificateChain":{"required": False, "type": "str"},
#         "CertificateArn":{"required": False, "type": "str"}
        }
   module = AnsibleModule(argument_spec=fields)

   if not HAS_BOTO3:
        module.fail_json(msg='boto3 and botocore are required by this module')

   region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
   client = boto3_conn(module, conn_type='client', resource='acm',
                        region=region, endpoint=ec2_url, **aws_connect_kwargs)


   if module.params["CertificateChain"]:
       response = client.import_certificate(
           Certificate=module.params["Certificate"],
           PrivateKey=module.params["PrivateKey"],
           CertificateChain=module.params["CertificateChain"]
       )
   else:
       response = client.import_certificate(
           Certificate=module.params["Certificate"],
           PrivateKey=module.params["PrivateKey"]
       )

   module.exit_json(response=response)


if __name__ == '__main__':
    main()
