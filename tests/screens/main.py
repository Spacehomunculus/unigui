from userset import user
from guielements import *

name = "Main"
icon = 'blur_linear'
order = 0
header = 'Test app'

table = Table('Videos', actions = '+-', headers = ['Video', 'Duration', 'Owner', 'Status', 'Links'],rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed', 'Refererence 1'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed', 'Refererence 8'],
    ['opt_sync1_3_0.mp4', '39 seconds', 'Admin', 'Processed', 'Refererence 10']
], value = -1)


select_concept_mode = SingleSelect('Select', value='All', options=['All','Based','Group'])
select_concept_group = SingleSelect('Group', value='Group 1', options=['Group 1','Group 2', 'Group 3'])

block = Block('_Current', 
    [           
        select_concept_mode,
        select_concept_group,
    ], table)

def prepare():
    pass

blocks= [block]