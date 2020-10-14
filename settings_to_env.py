import re
import os
import glob

def main():
    settings_path = ''
    current_dir = os.getcwd()
    settings_path = input('Enter path to settings.py,\nor leave blank if the script is in the root directory of your Django project: ')
    if settings_path and not os.path.exists(current_dir + 'settings.py'):
        while not os.path.exists(settings_path):
            settings_path = input('"{}" not found. Enter path to settings.py'.format(settings_path))
            if not settings_path:
                for filename in glob.iglob('./**/settings.py', recursive=True):
                    settings_path = filename
                if settings_path:
                    break
    elif not settings_path:
        for filename in glob.iglob('./**/settings.py', recursive=True):
            settings_path = filename
    custom_value = input("Please answer with y or n.\n Do you wish to enter a custom value for each key? (if not 'test' will be set as value for all keys): ")
    while custom_value.lower() not in ['y','n']:
        custom_value = input("Please answer with y or n.\n Do you wish to enter a custom value for each key? (if not 'test' will be set as value for all keys): ")
    with open(settings_path, 'r') as f:
        settings_file = f.readlines()
    config = ["config\('","'"]
    env_list = []
    for line in settings_file:
        try:
            key = re.search('{0}(.+?){1}'.format(config[0],config[1]), line).group(1)
            key = key.split("'", 1)[0]
            if custom_value.lower() == 'y':
                value = input('Enter value for {}: '.format(key))
                env_list.append({'key':key,'value':value})
            else:
                if "cast=bool" in line:
                    env_list.append({'key':key,'value':'True'})
                else:
                    env_list.append({'key':key,'value':'test'})
        except AttributeError as e:
            pass
    print(env_list)
    if not env_list:
        return 'Did not find decouple config in {}. Aborting.'.format(settings_path)
    env_path = os.path.dirname(os.path.dirname(os.path.abspath(settings_path)))
    print(env_path)
    with open(env_path + '/' + '.env', 'w') as env_file:
       for i in env_list:
           print(i)
           env_file.write('{0} = {1}\n'.format(i['key'],i['value']))

    return True

if __name__ == '__main__':
    main()
