import init

def app_close(text):
    print(f"Программа завершила работу с ошибкой{text}")
    input("Нажмите Enter, чтобы выйти...")
    init.sys.exit()

try:
    with open('config.json', 'r', encoding='utf-8') as json_file:
        config = init.json.load(json_file)
except Exception as e:
    app_close(text=f": {e}")

GROUP_ID = config['group_id']
ACCESS_TOKEN = config['access_token']
VERSION = config['version']
CHECK_INTERVAL = config['check_interval']
FILE_PATH = config['file_path']
table_file: str = 'Ссылки.xlsx'
full_path = f"{FILE_PATH}{table_file}"

def config_info():
    separator = "-" * 56
    print(f"{separator}\nТекущая конфигурация:\nID отслеживаемой группы: {GROUP_ID}\nИнтервал проверок: {CHECK_INTERVAL} сек.\n{separator}\n")

def get_last_post_id():
    url = 'https://api.vk.com/method/wall.get'
    params = {
        'owner_id': -int(GROUP_ID),
        'count': 2,
        'access_token': ACCESS_TOKEN,
        'v': VERSION
    }
    
    response = init.requests.get(url, params=params)
    data = response.json()

    if not 'error' in data:
        if 'response' in data and 'items' in data['response'] and len(data['response']['items']) > 0:
            try:
                if data['response']['items'][0]['is_pinned'] == 0:
                    return data['response']['items'][0]['id']
                else:
                    return data['response']['items'][1]['id']
            except:
                return data['response']['items'][0]['id']
        else:
            raise Exception("Не удалось получить посты")
    else:
        app_close(text=f" {data['error']['error_code']}: {data['error']['error_msg']}\n")
    
def last_post_hook():
    last_post_id = get_last_post_id()
    print(f"Изначально последний пост ID: {last_post_id}")

    while True:
        init.time.sleep(CHECK_INTERVAL)
        try:
            current_post_id = get_last_post_id()
            
            if current_post_id != last_post_id:
                new_post_link = f"https://vk.com/wall-{GROUP_ID}_{current_post_id}"
                print(f"Новый пост обнаружен! Ссылка: {new_post_link}")
                add_link_to_excel(new_post_link)
                last_post_id = current_post_id
                
        except Exception as e:
            print(f"Произошла ошибка: {e}")

def create_empty_excel(columns: list, filename: str, sheet_name: str = 'Лист 1'):
    df = init.pd.DataFrame(columns=columns)

    filepath = init.os.path.join(full_path)
    excel_writer = init.pd.ExcelWriter(filepath, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
    excel_writer._save()

    return filepath

def create_table():
    filepath = create_empty_excel(columns=['Ссылка'], filename=table_file)
    print(f"Файл {table_file} успешно создан")

def add_link_to_excel(post_link):
    new_row = init.pd.DataFrame({'Ссылка': [post_link]})
    df = init.pd.read_excel(full_path)
    df = init.pd.concat([df, new_row], ignore_index=True)
    df.to_excel(full_path, index=False)
    print(f"Ссылка успешно внесена в {table_file}")

def main():
    config_info()
    print("LinkhookVk запущен...")
    if not init.os.path.exists(full_path):
        create_table()
    last_post_hook()

if __name__ == '__main__':
    main()
