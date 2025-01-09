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
FILE_NAME = config['file_name']
FULL_PATH = f"{FILE_PATH}{FILE_NAME}"
index = 0

def config_info():
    separator = "-" * 56
    print(f"{separator}\nТекущая конфигурация:\nID отслеживаемой группы: {GROUP_ID}\nИнтервал проверок: {CHECK_INTERVAL} сек.\nПуть к файлу: {FULL_PATH}\n{separator}\n")

def get_last_post_info():
    url = 'https://api.vk.com/method/wall.get'
    params = {
        'owner_id': -int(GROUP_ID),
        'count': 2,
        'access_token': ACCESS_TOKEN,
        'v': VERSION
    }
    
    response = init.requests.get(url, params=params)
    data = response.json()
    # print(data)

    if not 'error' in data:
        if 'response' in data and 'items' in data['response'] and len(data['response']['items']) > 0:
            try:
                if data['response']['items'][0]['is_pinned'] == 0:
                    return data['response']['items'][0]['id'], data['response']['items'][0]['date']
                else:
                    return data['response']['items'][1]['id'], data['response']['items'][1]['date']
            except:
                return data['response']['items'][0]['id'], data['response']['items'][0]['date']
        else:
            raise Exception("Не удалось получить посты")
    else:
        app_close(text=f" {data['error']['error_code']}: {data['error']['error_msg']}\n")
    
def last_post_hook():
    last_post_id, last_post_date = get_last_post_info()
    print(f"ID и дата последнего поста: {last_post_id} | {date_normalizer(last_post_date)}")

    while True:
        init.time.sleep(CHECK_INTERVAL)
        try:
            current_post_id, current_post_date = get_last_post_info()
            
            if current_post_id != last_post_id:
                new_post_link = f"https://vk.com/wall-{GROUP_ID}_{current_post_id}"
                print(f"Новый пост обнаружен! Ссылка: {new_post_link}")
                add_info_to_excel(new_post_link, current_post_date)
                last_post_id = current_post_id
                
        except Exception as e:
            print(f"Произошла ошибка: {e}")

def create_empty_excel(columns: list, filename: str, sheet_name: str = 'Лист 1'):
    df = init.pd.DataFrame(columns=columns)

    filepath = init.os.path.join(FULL_PATH)
    excel_writer = init.pd.ExcelWriter(filepath, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
    excel_writer._save()

    return filepath

def create_table():
    filepath = create_empty_excel(columns=['№', 'Ссылка', 'Дата'], filename=FILE_NAME)
    print(f'Файл "{FILE_NAME}" успешно создан')

def add_info_to_excel(post_link, post_date):
    global index
    index += 1
    new_row = init.pd.DataFrame({'№': [index], 'Ссылка': [post_link], 'Дата': [date_normalizer(post_date)]})
    df = init.pd.read_excel(FULL_PATH)
    df = init.pd.concat([df, new_row], ignore_index=True)
    df.to_excel(FULL_PATH, index=False)
    print(f"Ссылка успешно внесена в таблицу")

def date_normalizer(date):
    date_norm = init.time.localtime(date)
    day = date_norm.tm_mday
    month = date_norm.tm_mon
    year = date_norm.tm_year
    hour = date_norm.tm_hour
    minute = date_norm.tm_min
    sec = date_norm.tm_sec
    return f"{date_edit(day)}.{date_edit(month)}.{year} {date_edit(hour)}:{date_edit(minute)}:{date_edit(sec)}"

def date_edit(text):
    if len(str(text)) == 1:
        return f"0{text}"
    else:
        return text

def index_calc():
    global index
    df_existing = init.pd.read_excel(FULL_PATH)
    if not df_existing.empty:
        index = df_existing['№'].max()

def main():
    config_info()
    print("LinkhookVk запущен...")
    if not init.os.path.exists(FULL_PATH):
        create_table()
    index_calc()
    last_post_hook()

if __name__ == '__main__':
    main()
