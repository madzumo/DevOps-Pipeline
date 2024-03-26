from colorama import Fore, Back, Style

# ec2 = boto3.client('ec2')

# response = ec2.describe_instances(
#     Filters=[
#         {
#             'Name': 'tag:madzumo',
#             'Values': ['demo']
#         }
#     ]
# )

# if response['Reservations']:
#     print('yes')
# else:
#     print('no')

print(Fore.RED + Style.BRIGHT + 'some red text')
print(Back.LIGHTYELLOW_EX + 'and with a green background')
print(Style.DIM + Back.LIGHTWHITE_EX + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')
