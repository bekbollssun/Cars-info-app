import os
import shutil

# Функция для создания папки "Корзинка" при запуске
def initialize_recycle_bin():
    recycle_bin = "RecycleBin"
    if not os.path.exists(recycle_bin):
        os.makedirs(recycle_bin)
    return recycle_bin

# Функция для выбора или создания папки (бренда автомобиля)
def select_or_create_folder():
    while True:
        print("\n--- Выбор или создание папки бренда автомобиля ---")
        print("1. Создать новую папку")
        print("2. Использовать существующую папку")
        print("b. Вернуться в главное меню")
        choice = input("Введите ваш выбор: ")
        
        if choice == '1':
            # Создание новой папки
            while True:
                folder_name = input("Введите НОВОЕ имя папки для хранения информации об автомобилях (или 'b' для отмены): ")
                if folder_name.lower() == 'b':
                    break
                if os.path.exists(folder_name):
                    print("Неверный ввод: Папка уже существует. Пожалуйста, выберите другое имя.")
                else:
                    os.makedirs(folder_name)
                    print(f"Папка '{folder_name}' создана.")
                    return folder_name
        
        elif choice == '2':
            # Использование существующей папки
            folders = [f for f in os.listdir() if os.path.isdir(f) and f != "RecycleBin"]
            if not folders:
                print("Нет доступных папок. Пожалуйста, создайте новую папку.")
                continue

            print("\nДоступные папки брендов:")
            for i, folder in enumerate(folders, start=1):
                print(f"{i}. {folder}")
            
            try:
                folder_choice = input("Введите номер папки, которую хотите использовать (или 'b' для отмены): ")
                if folder_choice.lower() == 'b':
                    break
                folder_choice = int(folder_choice) - 1
                if 0 <= folder_choice < len(folders):
                    return folders[folder_choice]
                else:
                    print("Неверный выбор. Пожалуйста, попробуйте снова.")
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите число.")
        elif choice.lower() == 'b':
            return None
        else:
            print("Неверный выбор. Пожалуйста, введите 1, 2 или 'b'.")

# Функция для проверки уникальности Car ID и сохранения его
def check_and_save_car_id():
    while True:
        print("\n--- Ввод Car ID ---")
        car_id = input("Введите Car ID (уникальный): ").strip()
        if car_id.lower() == 'b':
            return None
        if not car_id:
            print("Car ID не может быть пустым.")
            continue
        # Создаем файл, если его нет
        if not os.path.exists("CarsID.txt"):
            with open("CarsID.txt", "w") as f:
                pass
        with open("CarsID.txt", "r+") as f:
            existing_ids = f.read().splitlines()
            if car_id in existing_ids:
                print("Неверный ввод: Этот Car ID уже существует. Пожалуйста, используйте уникальный ID.")
            else:
                f.write(car_id + "\n")
                return car_id

# Функция для сохранения информации об автомобиле в указанной папке
def save_car_info(folder_name, car_id, car_info):
    file_path = os.path.join(folder_name, f"{car_id}.txt")
    with open(file_path, "w") as car_file:
        car_file.write(car_info)
    print(f"\nИнформация об автомобиле сохранена в '{file_path}'.\n")

# Функция для просмотра существующих автомобилей
def view_cars():
    print("\n--- Просмотр Существующих Автомобилей ---")
    folders = [f for f in os.listdir() if os.path.isdir(f) and f != "RecycleBin"]
    if not folders:
        print("Нет доступных брендов.")
        return
    
    print("\nДоступные бренды:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    
    try:
        folder_choice = int(input("\nВведите номер бренда, который хотите просмотреть: ")) - 1
        if 0 <= folder_choice < len(folders):
            selected_folder = folders[folder_choice]
            files = [f for f in os.listdir(selected_folder) if f.endswith('.txt')]
            if not files:
                print(f"\nВ бренде '{selected_folder}' нет доступных автомобилей.")
                return
            
            print(f"\nДоступные автомобили в '{selected_folder}':")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")
            
            file_choice = int(input("\nВведите номер автомобиля, который хотите просмотреть: ")) - 1
            if 0 <= file_choice < len(files):
                selected_file = files[file_choice]
                with open(os.path.join(selected_folder, selected_file), "r") as f:
                    print("\n--- Информация об Автомобиле ---")
                    print(f.read())
            else:
                print("Неверный выбор автомобиля.")
        else:
            print("Неверный выбор бренда.")
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите число.")

# Функция для редактирования названия папки (бренда)
def rename_folder():
    folders = [f for f in os.listdir() if os.path.isdir(f) and f != "RecycleBin"]
    if not folders:
        print("Нет доступных папок для переименования.")
        return
    print("\nДоступные бренды:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    try:
        choice = int(input("Введите номер папки, которую хотите переименовать: ")) - 1
        if 0 <= choice < len(folders):
            old_name = folders[choice]
            new_name = input(f"Введите новое имя для папки '{old_name}': ").strip()
            if not new_name:
                print("Новое имя не может быть пустым.")
                return
            if os.path.exists(new_name):
                print("Папка с таким именем уже существует.")
            else:
                os.rename(old_name, new_name)
                print(f"Папка переименована в '{new_name}'.")
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите число.")

# Функция для редактирования информации об автомобиле
def edit_car_info():
    print("\n--- Редактирование Информации об Автомобиле ---")
    folders = [f for f in os.listdir() if os.path.isdir(f) and f != "RecycleBin"]
    if not folders:
        print("Нет доступных брендов.")
        return
    
    print("\nДоступные бренды:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    
    try:
        folder_choice = int(input("Выберите бренд для редактирования автомобиля: ")) - 1
        if 0 <= folder_choice < len(folders):
            selected_folder = folders[folder_choice]
            files = [f for f in os.listdir(selected_folder) if f.endswith('.txt')]
            if not files:
                print(f"В бренде '{selected_folder}' нет доступных автомобилей.")
                return
            print(f"\nДоступные автомобили в '{selected_folder}':")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")
            file_choice = int(input("Выберите автомобиль для редактирования: ")) - 1
            if 0 <= file_choice < len(files):
                selected_file = files[file_choice]
                file_path = os.path.join(selected_folder, selected_file)
                with open(file_path, "r") as f:
                    content = f.read()
                print("\nТекущая информация об автомобиле:")
                print(content)
                
                print("\n--- Введите новую информацию об автомобиле ---")
                car_model = input("Введите модель автомобиля: ").strip()
                car_year = input("Введите год выпуска: ").strip()
                car_price = input("Введите цену автомобиля: ").strip()
                
                if not car_model or not car_year or not car_price:
                    print("Все поля должны быть заполнены.")
                    return
                
                new_content = f"Car ID: {selected_file[:-4]}\nCar Model: {car_model}\nYear of Manufacture: {car_year}\nPrice: {car_price}\n"
                with open(file_path, "w") as f:
                    f.write(new_content)
                print("Информация об автомобиле обновлена.")
            else:
                print("Неверный выбор автомобиля.")
        else:
            print("Неверный выбор бренда.")
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите число.")

# Функция для удаления папки (бренда) с перемещением в "Корзинку"
def delete_folder(recycle_bin):
    folders = [f for f in os.listdir() if os.path.isdir(f) and f != recycle_bin]
    if not folders:
        print("Нет доступных папок для удаления.")
        return
    print("\nДоступные бренды:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    try:
        choice = int(input("Введите номер папки, которую хотите удалить: ")) - 1
        if 0 <= choice < len(folders):
            folder_to_delete = folders[choice]
            confirm = input(f"Вы уверены, что хотите удалить папку '{folder_to_delete}' и все её содержимое? (y/n): ").lower()
            if confirm == 'y':
                destination = os.path.join(recycle_bin, folder_to_delete)
                if os.path.exists(destination):
                    print("Папка с таким именем уже существует в Корзинке.")
                else:
                    shutil.move(folder_to_delete, recycle_bin)
                    print(f"Папка '{folder_to_delete}' перемещена в Корзинку.")
            else:
                print("Удаление отменено.")
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите число.")
    except Exception as e:
        print(f"Ошибка при удалении папки: {e}")

# Функция для удаления автомобиля (перемещение в "Корзинку")
def delete_car(recycle_bin):
    print("\n--- Удаление Автомобиля ---")
    folders = [f for f in os.listdir() if os.path.isdir(f) and f != recycle_bin]
    if not folders:
        print("Нет доступных брендов.")
        return
    
    print("\nДоступные бренды:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    
    try:
        folder_choice = int(input("Выберите бренд для удаления автомобиля: ")) - 1
        if 0 <= folder_choice < len(folders):
            selected_folder = folders[folder_choice]
            files = [f for f in os.listdir(selected_folder) if f.endswith('.txt')]
            if not files:
                print(f"В бренде '{selected_folder}' нет доступных автомобилей для удаления.")
                return
            print(f"\nДоступные автомобили в '{selected_folder}':")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")
            
            file_choice = int(input("Выберите автомобиль для удаления: ")) - 1
            if 0 <= file_choice < len(files):
                selected_file = files[file_choice]
                source_path = os.path.join(selected_folder, selected_file)
                destination_folder = os.path.join(recycle_bin, selected_folder)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                destination_path = os.path.join(destination_folder, selected_file)
                if os.path.exists(destination_path):
                    print("Файл с таким именем уже существует в Корзинке.")
                else:
                    shutil.move(source_path, destination_folder)
                    print(f"Автомобиль '{selected_file}' перемещён в Корзинку.")
                    # Удаление Car ID из CarsID.txt
                    if os.path.exists("CarsID.txt"):
                        with open("CarsID.txt", "r") as f:
                            ids = f.read().splitlines()
                        car_id = selected_file[:-4]
                        if car_id in ids:
                            ids.remove(car_id)
                            with open("CarsID.txt", "w") as f:
                                f.write("\n".join(ids) + "\n")
            else:
                print("Неверный выбор автомобиля.")
        else:
            print("Неверный выбор бренда.")
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите число.")
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")

# Функция для поиска автомобилей по различным критериям
def search_car():
    print("\n--- Поиск Автомобилей ---")
    print("Выберите критерий поиска:")
    print("1. Car ID")
    print("2. Модель автомобиля")
    print("3. Год выпуска")
    print("4. Цена")
    print("5. Поиск по всем полям")
    
    choice = input("Введите номер критерия поиска: ")
    
    if choice == '1':
        search_field = 'Car ID'
    elif choice == '2':
        search_field = 'Car Model'
    elif choice == '3':
        search_field = 'Year of Manufacture'
    elif choice == '4':
        search_field = 'Price'
    elif choice == '5':
        search_field = 'All'
    else:
        print("Неверный выбор критерия поиска.")
        return
    
    search_value = input("Введите значение для поиска: ").strip().lower()
    if not search_value:
        print("Значение для поиска не может быть пустым.")
        return
    
    # Список для хранения найденных автомобилей
    results = []
    
    # Проход по всем папкам (брендам)
    folders = [f for f in os.listdir() if os.path.isdir(f) and f != "RecycleBin"]
    if not folders:
        print("Нет доступных брендов для поиска.")
        return
    
    for folder in folders:
        files = [f for f in os.listdir(folder) if f.endswith('.txt')]
        for file in files:
            file_path = os.path.join(folder, file)
            try:
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                    if search_field == 'All':
                        if search_value in content:
                            results.append((folder, file, content))
                    else:
                        # Поиск конкретного поля
                        lines = content.split('\n')
                        for line in lines:
                            if line.startswith(search_field.lower() + ":"):
                                value = line.split(":", 1)[1].strip()
                                if search_value in value.lower():
                                    results.append((folder, file, content))
                                break  # Переход к следующему файлу после нахождения поля
            except Exception as e:
                print(f"Ошибка при чтении файла '{file_path}': {e}")
    
    # Отображение результатов поиска
    if results:
        print(f"\nНайдено {len(results)} автомобиль(я):\n")
        for idx, (folder, file, content) in enumerate(results, start=1):
            print(f"--- Автомобиль {idx} ---")
            print(f"Бренд: {folder}")
            print(f"Файл: {file}")
            print(content)
            print("-----------------------\n")
    else:
        print("По вашему запросу ничего не найдено.")

# Функция для перемещения автомобиля из одной папки в другую
def move_car_file():
    print("\n--- Перемещение Автомобиля ---")
    folders = [f for f in os.listdir() if os.path.isdir(f) and f != "RecycleBin"]
    if not folders:
        print("Нет доступных брендов для перемещения.")
        return
    
    print("\nДоступные бренды:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    
    try:
        # Выбор исходного бренда
        source_choice = int(input("Выберите бренд, из которого хотите переместить автомобиль: ")) - 1
        if 0 <= source_choice < len(folders):
            source_folder = folders[source_choice]
            files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]
            if not files:
                print(f"В бренде '{source_folder}' нет доступных автомобилей для перемещения.")
                return
            print(f"\nДоступные автомобили в '{source_folder}':")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")
            
            # Выбор автомобиля для перемещения
            file_choice = int(input("Выберите автомобиль для перемещения: ")) - 1
            if 0 <= file_choice < len(files):
                selected_file = files[file_choice]
                source_path = os.path.join(source_folder, selected_file)
                
                # Выбор целевого бренда
                print("\nДоступные бренды для перемещения:")
                for i, folder in enumerate(folders, start=1):
                    print(f"{i}. {folder}")
                target_choice = int(input("Выберите бренд, в который хотите переместить автомобиль: ")) - 1
                if 0 <= target_choice < len(folders):
                    target_folder = folders[target_choice]
                    if target_folder == source_folder:
                        print("Исходный и целевой бренды совпадают. Перемещение не требуется.")
                        return
                    target_path = os.path.join(target_folder, selected_file)
                    if os.path.exists(target_path):
                        print("В целевом бренде уже существует автомобиль с таким же ID.")
                        return
                    # Перемещение файла
                    shutil.move(source_path, target_path)
                    print(f"Автомобиль '{selected_file}' успешно перемещён из '{source_folder}' в '{target_folder}'.")
                else:
                    print("Неверный выбор целевого бренда.")
            else:
                print("Неверный выбор автомобиля.")
        else:
            print("Неверный выбор исходного бренда.")
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите число.")
    except Exception as e:
        print(f"Ошибка при перемещении файла: {e}")

# Функция для просмотра и управления "Корзинкой"
def view_recycle_bin(recycle_bin):
    print("\n--- Корзинка ---")
    if not os.path.exists(recycle_bin):
        print("Корзинка пуста.")
        return
    
    deleted_folders = [f for f in os.listdir(recycle_bin) if os.path.isdir(os.path.join(recycle_bin, f))]
    if not deleted_folders:
        print("Корзинка пуста.")
        return
    
    print("\nУдалённые бренды:")
    for i, folder in enumerate(deleted_folders, start=1):
        print(f"{i}. {folder}")
    
    print(f"{len(deleted_folders)+1}. Окончательно очистить Корзинку")
    
    try:
        choice = int(input("\nВведите номер бренда для просмотра, восстановления или окончательного удаления (0 для выхода): "))
        if choice == 0:
            return
        elif 1 <= choice <= len(deleted_folders):
            selected_folder = deleted_folders[choice - 1]
            folder_path = os.path.join(recycle_bin, selected_folder)
            files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
            print(f"\nУдалённые автомобили в '{selected_folder}':")
            for j, file in enumerate(files, start=1):
                print(f"{j}. {file}")
            
            print(f"{len(files)+1}. Восстановить весь бренд")
            print(f"{len(files)+2}. Окончательно удалить бренд")
            
            sub_choice = int(input("\nВведите действие: "))
            if sub_choice == len(files) + 1:
                # Восстановить весь бренд
                destination = selected_folder
                if os.path.exists(destination):
                    print("Бренд с таким именем уже существует.")
                else:
                    shutil.move(folder_path, ".")
                    print(f"Бренд '{selected_folder}' восстановлен из Корзинки.")
            elif sub_choice == len(files) + 2:
                # Окончательно удалить бренд
                confirm = input(f"Вы уверены, что хотите окончательно удалить бренд '{selected_folder}'? (y/n): ").lower()
                if confirm == 'y':
                    shutil.rmtree(folder_path)
                    print(f"Бренд '{selected_folder}' окончательно удалён из Корзинки.")
            elif 1 <= sub_choice <= len(files):
                selected_file = files[sub_choice - 1]
                action = input(f"Введите 'r' для восстановления или 'd' для окончательного удаления '{selected_file}': ").lower()
                if action == 'r':
                    source_file = os.path.join(folder_path, selected_file)
                    destination_folder = selected_folder
                    destination_path = os.path.join(destination_folder, selected_file)
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    if os.path.exists(destination_path):
                        print("Файл с таким именем уже существует в исходной папке.")
                    else:
                        shutil.move(source_file, destination_folder)
                        print(f"Автомобиль '{selected_file}' восстановлен из Корзинки.")
                elif action == 'd':
                    confirm = input(f"Вы уверены, что хотите окончательно удалить '{selected_file}'? (y/n): ").lower()
                    if confirm == 'y':
                        os.remove(os.path.join(folder_path, selected_file))
                        print(f"Автомобиль '{selected_file}' окончательно удалён из Корзинки.")
                        # Также удалим ID из CarsID.txt
                        if os.path.exists("CarsID.txt"):
                            with open("CarsID.txt", "r") as f:
                                ids = f.read().splitlines()
                            car_id = selected_file[:-4]
                            if car_id in ids:
                                ids.remove(car_id)
                                with open("CarsID.txt", "w") as f:
                                    f.write("\n".join(ids) + "\n")
                else:
                    print("Неверный выбор действия.")
            else:
                print("Неверный выбор.")
        elif choice == len(deleted_folders) + 1:
            # Окончательно очистить Корзинку
            confirm = input("Вы уверены, что хотите окончательно очистить Корзинку? (y/n): ").lower()
            if confirm == 'y':
                shutil.rmtree(recycle_bin)
                os.makedirs(recycle_bin)
                print("Корзинка окончательно очищена.")
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите число.")
    except Exception as e:
        print(f"Ошибка при работе с Корзинкой: {e}")

# Функция для добавления нового автомобиля
def add_new_car(recycle_bin):
    print("\n--- Добавление Нового Автомобиля ---")
    folder_name = select_or_create_folder()
    if folder_name is None:
        print("Возвращение в главное меню.")
        return
    car_id = check_and_save_car_id()
    if car_id is None:
        print("Возвращение в главное меню.")
        return
    
    print("\n--- Ввод Деталей Автомобиля ---")
    car_model = input("Введите модель автомобиля: ").strip()
    car_year = input("Введите год выпуска: ").strip()
    car_price = input("Введите цену автомобиля: ").strip()
    
    if not car_model or not car_year or not car_price:
        print("Все поля должны быть заполнены. Автомобиль не добавлен.")
        return
    
    car_info = f"Car ID: {car_id}\nCar Model: {car_model}\nYear of Manufacture: {car_year}\nPrice: {car_price}\n"
    save_car_info(folder_name, car_id, car_info)

# Функция для окончательной очистки Корзинки (удаление всех содержимых)
def empty_recycle_bin(recycle_bin):
    confirm = input("Вы уверены, что хотите окончательно очистить Корзинку? (y/n): ").lower()
    if confirm == 'y':
        shutil.rmtree(recycle_bin)
        os.makedirs(recycle_bin)
        print("Корзинка окончательно очищена.")
    else:
        print("Очистка Корзинки отменена.")

# Функция для окончательного удаления файла из Корзинки
def permanently_delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Файл '{file_path}' окончательно удалён.")
    except Exception as e:
        print(f"Ошибка при окончательном удалении файла '{file_path}': {e}")

# Функция для окончательного удаления папки из Корзинки
def permanently_delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Папка '{folder_path}' окончательно удалена.")
    except Exception as e:
        print(f"Ошибка при окончательном удалении папки '{folder_path}': {e}")

# Основная функция приложения
def main():
    recycle_bin = initialize_recycle_bin()
    print("Добро пожаловать в приложение Car Dealer App")
    
    while True:
        print("\n--- Главное Меню ---")
        print("1. Добавить новый автомобиль")
        print("2. Просмотреть существующие автомобили")
        print("3. Редактировать автомобиль или бренд")
        print("4. Удалить автомобиль или бренд")
        print("5. Поиск автомобилей")
        print("6. Переместить автомобиль между брендами")
        print("7. Корзинка")
        print("8. Выйти")
        choice = input("Введите ваш выбор: ")
        
        if choice == '1':
            add_new_car(recycle_bin)
        
        elif choice == '2':
            view_cars()
        
        elif choice == '3':
            print("\n--- Редактирование ---")
            print("1. Переименовать бренд")
            print("2. Редактировать информацию об автомобиле")
            print("b. Вернуться в главное меню")
            sub_choice = input("Введите ваш выбор: ")
            if sub_choice == '1':
                rename_folder()
            elif sub_choice == '2':
                edit_car_info()
            elif sub_choice.lower() == 'b':
                continue
            else:
                print("Неверный выбор.")
        
        elif choice == '4':
            print("\n--- Удаление ---")
            print("1. Удалить бренд")
            print("2. Удалить автомобиль")
            print("b. Вернуться в главное меню")
            sub_choice = input("Введите ваш выбор: ")
            if sub_choice == '1':
                delete_folder(recycle_bin)
            elif sub_choice == '2':
                delete_car(recycle_bin)
            elif sub_choice.lower() == 'b':
                continue
            else:
                print("Неверный выбор.")
        
        elif choice == '5':
            search_car()
        
        elif choice == '6':
            move_car_file()
        
        elif choice == '7':
            view_recycle_bin(recycle_bin)
        
        elif choice == '8':
            print("\nВыход из приложения. До свидания!")
            break
        
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 8.")

if __name__ == "__main__":
    main()










