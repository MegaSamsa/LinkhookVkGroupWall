import init

with open('config.json', 'r', encoding='utf-8') as json_file:
    config = init.json.load(json_file)

GROUP_ID = config['group_id']
ACCESS_TOKEN = config['access_token']
VERSION = config['version']
CHECK_INTERVAL = config['check_interval']
table_file: str = "links.xlsx"

def get_last_post_id():
    url = 'https://api.vk.com/method/wall.get'
    params = {
        'owner_id': -int(GROUP_ID),
        'count': 1,
        'access_token': ACCESS_TOKEN,
        'v': VERSION
    }
    
    response = init.requests.get(url, params=params)
    data = response.json()
    
    if 'response' in data and 'items' in data['response'] and len(data['response']['items']) > 0:
        return data['response']['items'][0]['id']
    else:
        raise Exception("Не удалось получить посты")

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

    filepath = init.os.path.join('', filename)
    excel_writer = init.pd.ExcelWriter(filepath, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
    excel_writer._save()

    return filepath

def create_table():
    filepath = create_empty_excel(columns=['Ссылка'], filename=table_file)
    print(f"Файл {table_file} успешно создан.")

def add_link_to_excel(post_link):
    new_row = init.pd.DataFrame({'Ссылка': [post_link]})
    df = init.pd.read_excel(table_file)
    df = init.pd.concat([df, new_row], ignore_index=True)
    df.to_excel(table_file, index=False)
    print(f"Ссылка успешно внесена в {table_file}")

def main():
    if not init.os.path.exists(table_file):
        create_table()
    last_post_hook()

if __name__ == '__main__':
    main()