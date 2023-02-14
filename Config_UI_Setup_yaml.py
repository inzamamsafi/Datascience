import ipywidgets as widgets
from IPython.display import display, Markdown, Javascript, clear_output 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from functools import partial
import json
import requests
from ipywidgets import interact

E1_token = 'OACCESSTOKEN=eyJraWQiOiI4UGl6QTdwYUk5SGxYcmNURDBucVhrQXZNc19HNUJYc2pPcUJxN3ZPWm9zIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULlZFdEMxdFdNUWpTdTVrS09SMV9DUFVnSHVyYWp6UDNucWZBRkhoakZMWFkub2FyMXlxYTVpb0R3UXRoZUEwaDciLCJpc3MiOiJodHRwczovL2FleHAtZGV2Lm9rdGFwcmV2aWV3LmNvbS9vYXV0aDIvYXVzaXVsOWlnOVBlazVzdVgwaDciLCJhdWQiOiJtbHBsYXRmb3JtIiwiaWF0IjoxNjc2MzU5NTU5LCJleHAiOjE2NzYzNjMxNTksImNpZCI6IjBvYWl1YnZndmN1a25MY3JGMGg3IiwidWlkIjoiMDB1MWU1ZjdibGhxelpkUzkwaDgiLCJzY3AiOlsicHJvZmlsZSIsIm9wZW5pZCIsIm9mZmxpbmVfYWNjZXNzIl0sImF1dGhfdGltZSI6MTY3NjM1OTU0Niwic3ViIjoiaXNhZmkiLCJGaXJzdE5hbWUiOiJJTlpBTUFNIiwiTGFzdE5hbWUiOiJTQUZJIiwiYXhwR3VpZCI6ImQ1MWZhNGRhMzM1ZTRkMWJiZThiMjUyNjczYjczNTYwIiwiZW1wbG95ZWVpZCI6IjgxOTQzMzgiLCJncm91cHNfYWlkYSI6WyJTU09fQUlEQV9BRE1JTiJdLCJlbWFpbCI6IklOWkFNQU0uU0FGSUBhZXhwLmNvbSJ9.FTfPIa4bJGr934OTc6q-5OxiUI7oUyhKs4c1dwjGoaWvNDXV8qj4st8yD8dH18QSbfdHuN3HwPE2c9OUPqnM8d4ttIp3M6L0-7IYQ1KF7fFBsMP7dpXIS5DU-d3SgiPrwMP0TTuDDGRpkXxzVCU-N4FDALsOw8u4SCRnAIIahVYfTZkhK9-TuAV7-QTgeZe-vRI_p7-HrJLmjFOGVMYhtdpHgpHDntZM4wPBo1mvumEW_F8ueRKvQgZLntGtjsBRGCsBw4O4Qg4lzsRFgxqPBkZ2r1vJpvoNhkZikCzutBasLISKuEO1hLDSITCtsQPUcs0EZ7X5lVj8qsJ-eGfRmg'

vars_config = []
vars_config_widgets = []
output_widgets = []

json_file = open('C:/Users/isafi/Music/Create_UI/simple_task_02/config.json')
initial_setup = json.load(json_file)

display(Markdown('''# **Configurable Data Model : Setup**'''))

display(Markdown('''## **Feature Pipeline Information**'''))
print(' ')

pipeline_id_wid = widgets.Text(value=initial_setup['pipeline_id'], description='Pipeline ID : ', style={
                               'description_width': 'initial'},)
version_wid = widgets.FloatText(value=initial_setup['version'], description='Version : ', style={
                                'description_width': 'initial'},)
pipeline_type_wid = widgets.Text(value=initial_setup['pipeline_type'], description='Pipeline Type : ', style={
                                 'description_width': 'initial'},)
deploy_type_wid = widgets.Text(value=initial_setup['deploy_type'], description='Deploy Type : ', style={
                               'description_width': 'initial'},)

display(pipeline_id_wid)
display(version_wid)
display(pipeline_type_wid)
display(deploy_type_wid)

print(' ')
display(Markdown(
    '''**NOTE** : The functionality of creating multiple time windows has been provided to support retro-scoring use cases to manage changing SOR/s over their required execution period.
    
    '''))

display(Markdown(
    '''Time Windows can be defined for every task group to support different logics for different execution dates. The number of time windows for every task group is initialized to 1. **Should you not wish to make multiple time windows, select "Run Indefinitely" in the initialized time window**. To know more visit [Config DM - Time Windows](https://enterprise-confluence.aexp.com/confluence/display/GS/Data+Model+POC+Documentation)'''))
print(' ')
display(Markdown('''---'''))
print(' ')
display(Markdown('''## **Task Setup**'''))
print(' ')
parent_output = widgets.Output()
display(parent_output)

# for removing any task info
def remove_task(task_index):
    for i in range(len(output_widgets)):
        with output_widgets[i]:
            clear_output()

    del output_widgets[task_index]
    del vars_config[task_index]
    del vars_config_widgets[task_index]
    new_task_name.value = f'task_group_{len(vars_config)+1}'
    display_all_tasks()

## tdchange 
def update_task_values_tw(task_index):
    i = task_index
## Eg if vars_config_widgets =4 and vars_config = 4 use updated vars_config_widgets= 2
#
    if vars_config[i]['num_tw'] >= vars_config_widgets[i]['num_tw'].value:
        vars_config[i]['time_windows'] = vars_config[i]['time_windows'][:
                                                                        vars_config_widgets[i]['num_tw'].value] # WE are updating vars_config = 2 just like widget
    else: # vars_config_widgets > vars_config so we are creating new value and populating it.
        for j in range(vars_config_widgets[i]['num_tw'].value-vars_config[i]['num_tw']):  # Empty template only key
            vars_config[i]['time_windows'].append({
                'Task_Name_XX': 'sample_xx',           ## tdchange       
                'start_date': date.today(),
                'end_date': date(date.today().year + 1, date.today().month, date.today().day),
                'run_indefinitely': False,
                'code_file_path': '',
                'num_params': 0,
                'config': {},
                'language': 'Hive',
            })

    for j in range(min(vars_config[i]['num_tw'], len(vars_config[i]['time_windows']))):  # filling the empty template key with the value from the config_widget
        for wid in ['Task_Name_XX', 'start_date', 'end_date', 'run_indefinitely', 'code_file_path', 'language', 'num_params']:  ## tdchange 
            vars_config[i]['time_windows'][j][wid] = vars_config_widgets[
                i]['time_windows'][j][wid].value
        param_config = {}
        for k in range(vars_config[i]['time_windows'][j]['num_params']):
            param_config[vars_config_widgets[i]['time_windows'][j]['config']
                         [f'key_{k}'].value] = vars_config_widgets[i]['time_windows'][j]['config'][f'value_{k}'].value

        vars_config[i]['time_windows'][j]['config'] = param_config

    vars_config[i]['num_tw'] = vars_config_widgets[i]['num_tw'].value

    for wid in ['code_file_path', 'language']:
        vars_config[i]['default'][wid] = vars_config_widgets[i]['default'][wid].value

## vars_config_num_par = 4 , vars_config_widgets_num_parm = 4 , after update vars_config_widgets_num_parm = 2
def update_task_values_param(task_index):
    i = task_index

    for j in range(vars_config[i]['num_tw']):
        for wid in ['start_date', 'end_date', 'run_indefinitely', 'code_file_path', 'language']:  ## tdchange 
            vars_config[i]['time_windows'][j][wid] = vars_config_widgets[
                i]['time_windows'][j][wid].value
        param_config = {}

        if (vars_config[i]['time_windows'][j]['num_params'] >= vars_config_widgets[i]['time_windows'][j]['num_params'].value):
            for k in range(vars_config_widgets[i]['time_windows'][j]['num_params'].value):
                param_config[vars_config_widgets[i]['time_windows'][j]['config']
                             [f'key_{k}'].value] = vars_config_widgets[i]['time_windows'][j]['config'][f'value_{k}'].value
        else:
            for k in range(vars_config[i]['time_windows'][j]['num_params']):
                param_config[vars_config_widgets[i]['time_windows'][j]['config']
                             [f'key_{k}'].value] = vars_config_widgets[i]['time_windows'][j]['config'][f'value_{k}'].value

            for k in range(vars_config_widgets[i]['time_windows'][j]['num_params'].value - vars_config[i]['time_windows'][j]['num_params']):
                param_config[f"new_key_{vars_config[i]['time_windows'][j]['num_params']+k+1}"] = ''

        vars_config[i]['time_windows'][j]['config'] = param_config
        vars_config[i]['time_windows'][j]['num_params'] = vars_config_widgets[i]['time_windows'][j]['num_params'].value

    for wid in ['code_file_path', 'language']:
        vars_config[i]['default'][wid] = vars_config_widgets[i]['default'][wid].value


def add_new_task(b):

    vars_config.append({'task_group_id': new_task_name.value, 'num_tw': 1, 'time_windows': [{'Task_Name_XX' : 'sample_xx',  ## tdchange 
                                                                                            'start_date': date.today(),
                                                                                            'end_date': date(date.today().year + 1, date.today().month, date.today().day),
                                                                                             'run_indefinitely': False,
                                                                                             'code_file_path': '',
                                                                                             'num_params': 0,
                                                                                             'config': {},
                                                                                             'language': 'Hive', }], 'default': {'code_file_path': '', 'language': 'Hive', }})
    vars_config_widgets.append({})
    output_widgets.append(widgets.Output())
    with parent_output:
        display(output_widgets[-1])

    new_task_name.value = f'task_group_{len(vars_config)+1}'
    display_task(len(vars_config)-1)


def display_task(task_index):
    # clearing out the previous values in the widgets array
    vars_config_widgets[task_index] = {}
    task_widget_array = []
    i = task_index
    with output_widgets[i]:
        clear_output()
## GDChange2
        vars_config_widgets[i]['task_group_id'] = widgets.Text(
            value=vars_config[i]['task_group_id'], description='Task Group Name:', style={'description_width': 'initial'})
        task_widget_array.append(vars_config_widgets[i]['task_group_id'])


        vars_config_widgets[i]['num_tw'] = widgets.IntText(
            value=vars_config[i]['num_tw'], description='Number of Time-Windows : ', style={'description_width': 'initial'})

        task_widget_array.append(vars_config_widgets[i]['num_tw'])
 
        task_widget_array.append(widgets.Label())  # blank line for spacing

        vars_config_widgets[i]['time_windows'] = []
        vars_config_widgets[i]['default'] = {}
## TDchange1x
        for j in range(vars_config[i]['num_tw']):
            task_tw_widgets_array = []
            vars_config_widgets[i]['time_windows'].append({
                'Task_Name_XX': widgets.Text(value=vars_config[i]['time_windows'][j]['Task_Name_XX'], description='Task_Name_XX: ', style={'description_width': 'initial'}),
                'start_date': widgets.DatePicker(value=vars_config[i]['time_windows'][j]['start_date'], description='Start Date(MM-DD-YYYY): ', style={'description_width': 'initial'}),
                'end_date': widgets.DatePicker(value=vars_config[i]['time_windows'][j]['end_date'], description='End Date(MM-DD-YYYY): ', style={'description_width': 'initial'}),
                'run_indefinitely': widgets.Checkbox(value=vars_config[i]['time_windows'][j]['run_indefinitely'], description='Run Indefinitely ', style={'description_width': 'initial'}),
                'code_file_path': widgets.Text(value=vars_config[i]['time_windows'][j]['code_file_path'], description='Code File Path : ', style={'description_width': 'initial'}),
                'language': widgets.Dropdown(options=['Hive', 'PySpark'], value=vars_config[i]['time_windows'][j]['language'], description='Language :', style={'description_width': 'initial'}),
                'num_params': widgets.IntText(value=vars_config[i]['time_windows'][j]['num_params'], description='Number of Configurable Params : ', style={'description_width': 'initial'}),
                'config': {}
            })
            for wid in ['Task_Name_XX','start_date', 'end_date', 'run_indefinitely', 'code_file_path', 'language']:
                if (wid == 'run_indefinitely'):
                    task_tw_widgets_array.append(widgets.Label(
                        value='(Select "Run Indefinitely" if you want this logic to run without any defined end date)'))
                task_tw_widgets_array.append(
                    vars_config_widgets[i]['time_windows'][j][wid])

            task_tw_widgets_array.append(
                widgets.Label())  # blank line for spacing
            task_tw_widgets_array.append(
                vars_config_widgets[i]['time_windows'][j]['num_params'])
            task_tw_widgets_array.append(widgets.Label('(optional field)'))
            task_tw_config = []

            def on_num_param_change_tw(change):
                update_task_values_param(task_index)
                display_task(task_index)

            vars_config_widgets[i]['time_windows'][j]['num_params'].observe(
                on_num_param_change_tw, names='value')

            for key, value in vars_config[i]['time_windows'][j]['config'].items():
                task_tw_config.append((key, value))

            for k in range(vars_config[i]['time_windows'][j]['num_params']):
                vars_config_widgets[i]['time_windows'][j]['config'][f'key_{k}'] = widgets.Text(
                    value=task_tw_config[k][0], description=f'Key #{k+1} : ', style={'description_width': 'initial'})
                vars_config_widgets[i]['time_windows'][j]['config'][f'value_{k}'] = widgets.Text(
                    value=task_tw_config[k][1], description=f'  Value #{k+1} : ', style={'description_width': 'initial'})
                task_tw_widgets_array.append(widgets.HBox(
                    [vars_config_widgets[i]['time_windows'][j]['config'][f'key_{k}'], vars_config_widgets[i]['time_windows'][j]['config'][f'value_{k}']]))

            vars_config_widgets[i]['time_windows'][j]['accordion'] = widgets.Accordion(children=[
                widgets.VBox(task_tw_widgets_array)])
            vars_config_widgets[i]['time_windows'][j]['accordion'].set_title(
                0, f'Time Window {j+1}')
            task_widget_array.append(
                vars_config_widgets[i]['time_windows'][j]['accordion'])

        def on_num_tw_change(change):
            update_task_values_tw(task_index)
            display_task(task_index)

        vars_config_widgets[i]['num_tw'].observe(
            on_num_tw_change, names='value')

        task_widget_array.append(widgets.Label())  # blank line for spacing
        vars_config_widgets[i]['default'] = {
            'code_file_path': widgets.Text(value=vars_config[i]['default']['code_file_path'], description='Code File Path : ', style={'description_width': 'initial'}),
            'language': widgets.Dropdown(options=['Hive', 'PySpark'], value=vars_config[i]['default']['language'], description='Language :', style={'description_width': 'initial'}),
        }

        default_widgets_array = []
        for wid in ['code_file_path', 'language']:
            default_widgets_array.append(
                vars_config_widgets[i]['default'][wid])

        vars_config_widgets[i]['default']['accordion'] = widgets.Accordion(children=[
            widgets.VBox(default_widgets_array)])
        vars_config_widgets[i]['default']['accordion'].set_title(
            0, 'Default')
        task_widget_array.append(
            vars_config_widgets[i]['default']['accordion'])

        task_widget_array.append(widgets.Label())

        vars_config_widgets[i]['delete'] = widgets.Button(
            description='Delete Task Group', button_style='danger')

        def delete_task(b):
            remove_task(task_index)

        vars_config_widgets[i]['delete'].on_click(delete_task)

        task_widget_array.append(vars_config_widgets[i]['delete'])

        vars_config_widgets[i]['accordion'] = widgets.Accordion(children=[
            widgets.VBox(task_widget_array)])
        vars_config_widgets[i]['accordion'].set_title(
            0, vars_config[i]['task_group_id'])

        display(vars_config_widgets[i]['accordion'])

        display(Markdown('''---'''))


def display_all_tasks():
    for ind in range(len(vars_config)):
        display_task(ind)

# updating non structural changes
def update_all_tasks():
    for i in range(len(vars_config)):
##GDCHANGE3
        vars_config[i]['task_group_id'] = vars_config_widgets[i]['task_group_id'].value

        for j in range(vars_config[i]['num_tw']):
            for wid in ['Task_Name_XX','start_date', 'end_date', 'run_indefinitely', 'code_file_path', 'language']: ## tdchange 
                vars_config[i]['time_windows'][j][wid] = vars_config_widgets[
                    i]['time_windows'][j][wid].value
            param_config = {}

            for wid in ['Task_Name_XX','start_date', 'end_date', 'run_indefinitely', 'code_file_path', 'language', 'num_params']: ## tdchange 
                vars_config[i]['time_windows'][j][wid] = vars_config_widgets[i]['time_windows'][j][wid].value
            param_config = {}
            for k in range(vars_config[i]['time_windows'][j]['num_params']):
                param_config[vars_config_widgets[i]['time_windows'][j]['config']
                             [f'key_{k}'].value] = vars_config_widgets[i]['time_windows'][j]['config'][f'value_{k}'].value

            vars_config[i]['time_windows'][j]['config'] = param_config    #bug_fix

            vars_config[i]['num_tw'] = vars_config_widgets[i]['num_tw'].value    #bug_fix

        for wid in ['code_file_path', 'language']:
            vars_config[i]['default'][wid] = vars_config_widgets[i]['default'][wid].value


def get_dates(condition):
    start_i = -1
    end_i = -1
    for a in range(len(condition)):
        if condition[a] == '[':
            start_i = a+1
        elif condition[a] == ']':
            end_i = a
            break

    dates_str = condition[start_i: end_i]
    dates_arr = dates_str.split(",")
    start_date = datetime.strptime(dates_arr[0].strip(), '%Y-%m-%d').date()
    end_date = datetime.strptime(dates_arr[1].strip(), '%Y-%m-%d').date()
    if end_date == date(2039, 3, 5):
        return start_date, start_date+relativedelta(years=1), True
    else:
        return start_date, end_date, False

##tdchange Task_Name
def initialize_form():
    for i in range(len(initial_setup['stages'])-1):
        output_widgets.append(widgets.Output())
        vars_config_widgets.append({})
        ## GDChange1
        vars_config.append({'task_group_id': list(initial_setup['stages'][i].values())[0], 'num_tw': len(initial_setup['stages'][i]['branch']), 'time_windows': [], 'default': {
            'code_file_path': initial_setup['stages'][i]['default']['code_file_path'], 'language': initial_setup['stages'][i]['default']['language'], }, })
        for tw in range(len(initial_setup['stages'][i]['branch'])):
            start_date, end_date, run_indefinitely = get_dates(
                initial_setup['stages'][i]['branch'][tw]['condition'])
            vars_config[i]['time_windows'].append({'Task_Name_XX' : 'Task_Name_XX',
                                                'start_date': start_date,
                                                'end_date': end_date,
                                                'run_indefinitely': run_indefinitely,
                                                'code_file_path': initial_setup['stages'][i]['branch'][tw]['code_file_path'],
                                                'num_params': len(initial_setup['stages'][i]['branch'][tw]['config']),
                                                'config': initial_setup['stages'][i]['branch'][tw]['config'],
                                                'language': initial_setup['stages'][i]['branch'][tw]['language'], })
    with parent_output:
        for i in range(len(output_widgets)):
            display(output_widgets[i])
        

    display_all_tasks()

initialize_form()

print(' ')
add_task_bt = widgets.Button(
    description='+ Add Task Group', button_style='primary')
new_task_name = widgets.Text(value=f'task_group_{len(output_widgets)+1}')
output_add_bt = widgets.Output()
display(output_add_bt)
with output_add_bt:
    display(widgets.HBox([new_task_name, add_task_bt]))
    add_task_bt.on_click(add_new_task)


print(' ')

display(Markdown('''## **Aggregation**'''))
print(' ')

aggr_task_id_wid = widgets.Text(value=initial_setup['stages'][-1]['task_id'], description='Aggr Task ID : ', style={
    'description_width': 'initial'},)

aggr_code_file_path_wid = widgets.Text(value=initial_setup['stages'][-1]['code_file_path'], description='Aggr Code File Path : ', style={
                                       'description_width': 'initial'},)

aggr_lang_wid = widgets.Dropdown(options=['Hive', 'PySpark'], value=initial_setup['stages'][-1]['language'],
                                 description='Aggr Logic Language : ', style={'description_width': 'initial'},)

display(aggr_task_id_wid)
display(aggr_code_file_path_wid)
display(aggr_lang_wid)

print(' ')
display(Markdown('''---'''))

display(Markdown('''## **Dependencies**'''))
print(' ')
config_dependencies_wid = widgets.Text(value=initial_setup['dependencies'], description='Dependencies : ', style={
    'description_width': 'initial'},)
display(config_dependencies_wid)
display(Markdown('''(example - ['task_group_id_01_Name >> task_group_id_02_Name >> aggregation_logic'])'''))
print(' ')

create_config_btn = widgets.Button(
    description='Update Config', button_style='success')
display(create_config_btn)

#### Createn API Button ####
# print(' ')
# create_api_btn = widgets.Button(
#     description='Save config', button_style='success')
# display(create_api_btn)

#######  END   #########


def create_config_file(b):
    # print('vars_config_widgets_##',vars_config_widgets)
    # print('vars_config_##',vars_config)
    update_all_tasks()
    print('vars_config_widgets_After_@@',vars_config_widgets)
    print('vars_config_after_@@',vars_config)

    config_setup_json = {
        'pipeline_id': pipeline_id_wid.value,
        'version': version_wid.value,
        'stages': [],
        'dependencies': config_dependencies_wid.value,
        'pipeline_type': pipeline_type_wid.value,
        'deploy_type': deploy_type_wid.value,
    }

    for ind in range(len(vars_config)):
        var = vars_config[ind]

        config_setup_json['stages'].append(
            {'task_group_id': var['task_group_id'], 'branch': [], 'default': {'task_id': f"{var['task_group_id']}_default",
                                                                              "code_file_path": var['default']['code_file_path'],
                                                                              "language": var['default']['language'],
                                                                              "config": {}, }})

        for i in range(len(var['time_windows'])):
            config_setup_json['stages'][ind]['branch'].append({'task_id': var['time_windows'][i]['Task_Name_XX'],   ## tdchange
                                                               "code_file_path": var['time_windows'][i]['code_file_path'],
                                                               "language": var['time_windows'][i]['language'],
                                                               "config": var['time_windows'][i]['config'],
                                                               "sequence": i+1,
                                                               })

            if (len(var['time_windows']) == 1 and var['time_windows'][i]['run_indefinitely']):
                config_setup_json['stages'][ind]['branch'][i][
                    'condition'] = f"in_start_date in range [{str(var['time_windows'][i]['start_date'])}, 2039-03-05]"

            else:
                config_setup_json['stages'][ind]['branch'][i][
                    'condition'] = f"in_start_date in range [{str(var['time_windows'][i]['start_date'])} , {str(var['time_windows'][i]['end_date'])}]"

    # aggregation logic
    config_setup_json['stages'].append(
        {'task_id': aggr_task_id_wid.value, 'code_file_path': aggr_code_file_path_wid.value, 'language': aggr_lang_wid.value, 'config': {}, })

    with open('config.json', "w") as outfile:
        json.dump(config_setup_json, outfile, default=str)

    

create_config_btn.on_click(create_config_file)



## Defining a function



def create_api(b):
    
    API_ENDPOINT = "https://functions-dev.aexp.com/CreateAiDaDeployPipelineTaskConfiguration.v1"
    json_file = open('C:/Users/isafi/Music/Create_UI/simple_task_02/config.json')
    initial_setup = json.load(json_file)
    # print('##initial_setup',initial_setup)
    data = {}
    data["pipelineId"] = int(initial_setup["pipeline_id"])
    data["pipelineVersion"] = int(initial_setup["version"])
    
    ## Empty taskconfiguration
    count=0
    for i in range(len(initial_setup["stages"])-1):
        for j in range(len(initial_setup["stages"][i]["branch"])):
            for k in initial_setup["stages"][i]["branch"][j].keys():
                if k == "task_id":
                    count+=1
    data["taskConfigurations"] = [dict() for x in range(count)]

    # print("Empty taskconfiguration", data)


    ## Taskname
    task_name = []
    for i in range(len(initial_setup["stages"])-1):
        for j in range(len(initial_setup["stages"][i]["branch"])):
            for k,v in initial_setup["stages"][i]["branch"][j].items():
                if k == "task_id":
                    task_name.append(v)
    # print("## Taskname",task_name)
    for x,y in zip(range(count),range(len(task_name))):
        data["taskConfigurations"][x]["taskName"] = task_name[y]
    # print("## Taskname2",data)
    ## Adding config key value
    key = []
    value = []

    for i in range(len(initial_setup["stages"])-1):
        for j in range(len(initial_setup["stages"][i]["branch"])):
            for k,v in initial_setup["stages"][i]["branch"][j]["config"].items():
                    key.append(k)
                    value.append(v)

    # print(key)
    # print(value)
    
    ## config KEY
    for x,y in zip(range(count),range(len(key))):
        data["taskConfigurations"][x]["configKey"] = key[y]

    ## config VALUE
    for x,y in zip(range(count),range(len(value))):
        data["taskConfigurations"][x]["configValue"] = value[y]
    # print("config VALUE##", data)
    ## Adding indicator,username and email ---- STATIC

    for i in range(count):
        data["taskConfigurations"][i]["analyticalRunAppliedIndicator"] = True
        data["taskConfigurations"][i]["productionRunAppliedIndicator"] = False
        # data["taskConfigurations"][i]["creatorId"] = "yyang11"
        # data["taskConfigurations"][i]["creatorEmail"] = "yan.yang@aexp.com"

    # print('### API value update 111 ## ', data)

    ## When Number of Configurable Params is 0
    sum_of_num_params = []
    for i in range(len(vars_config)):
        for j in range(len(vars_config[i]['time_windows'])):
            sum_of_num_params.append(vars_config[i]['time_windows'][j]['num_params'])




    # key_check
    key_check = []
    for ele in key:
        if ele.strip():
            key_check.append(ele)
    
    # Value_check
    Value_check = []
    for ele in value:
        if ele.strip():
            Value_check.append(ele)
    

    headers = {"Content-Type": "application/json", "Authorization":E1_token}
    if len(key) == len(key_check) and len(value)==len(Value_check):
        if 0 not in sum_of_num_params:

            r = requests.post(url = API_ENDPOINT, headers=headers, json = data)
        
            display(widgets.Label(value="Key Value Pair Created"))

        else:
            display(widgets.Label(value="Config param is set to zero"))

    else:
        display(widgets.Label(value="You have left some key value empty"))
        # print("You have left some key value empty")
    
    # print("Method_03_GEN##",data)
    # print("pastebin_url##",pastebin_url)

    # return pastebin_url


create_config_btn.on_click((create_api))




