from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from win10toast import ToastNotifier

# Constantes
NEOPETS_URL = 'https://www.neopets.com/pound/adopt.phtml'
WAIT_TIME = 5
CLICK_WAIT_TIME = 2
REFRESH_WAIT_TIME = 15
MAX_RETRY_ATTEMPTS = 3
MAX_PRICE = 5000
UNDESIRED_PET_COLORS = ['Green', 'Red', 'Blue', 'Yellow', 'Purple', 'White', 'Purple', 'Brown']

# One-time initialization
toaster = ToastNotifier()


def wait_and_click(element, wait_time=CLICK_WAIT_TIME):
    """
    Espera por um elemento e clica nele.
    """
    time.sleep(wait_time)
    element.click()


def get_pet_info(driver, pet_index):
    """
    Obtém as informações (cor, nome e preço) de um pet específico na página.
    """
    pet_info = {}
    try:
        pet_info['color'] = driver.find_element(By.ID, f'pet{pet_index}_color').text
        pet_info['name'] = driver.find_element(By.ID, f'pet{pet_index}_name').text
        pet_info['price'] = int(driver.find_element(By.ID, f'pet{pet_index}_price').text.replace(',', ''))
    except Exception as e:
        print(f"Erro ao obter as informações do pet{pet_index}: {e}")
        pet_info = {'color': None, 'name': None, 'price': 0}
    return pet_info


def check_and_notify_pet(driver, pet_info, pets_nao_desejados):
    """
    Verifica se o pet é indesejado (cor ou preço) e notifica se necessário.
    """
    pet_color = pet_info['color']
    pet_name = pet_info['name']

    if pet_color and pet_color not in UNDESIRED_PET_COLORS:
        if pet_name not in pets_nao_desejados:
            pets_nao_desejados.append(pet_name)
            print(f"Pet indesejado encontrado: {pet_name}")
            toaster.show_toast("Notification!", "Novo Neopet encontrado!", threaded=True,
                               icon_path=None, duration=5)

    pet_price = pet_info['price']
    if pet_price > MAX_PRICE:
        if pet_name not in pets_nao_desejados:
            pets_nao_desejados.append(pet_name)
            print(f"Pet com preço maior do que {MAX_PRICE} encontrado: {pet_name}")
            toaster.show_toast("Notification!", f"Novo Neopet com preço maior do que {MAX_PRICE} encontrado!",
                               threaded=True, icon_path=None, duration=5)


def check_unwanted_pets(driver, pets_nao_desejados):
    """
    Verifica os pets indesejados e notifica se necessário.
    """
    for pet_index in range(3):
        pet_info = get_pet_info(driver, pet_index)
        check_and_notify_pet(driver, pet_info, pets_nao_desejados)


def find_unwanted_pets(driver):
    """
    Encontra pets indesejados e clica no botão 'View More Pets' para obter mais pets.
    """
    retry_attempts = 0
    pets_nao_desejados = []

    while True:
        time.sleep(WAIT_TIME)

        # Verifica se os elementos estão presentes na página
        try:
            driver.find_element(By.ID, 'pet0_color')
        except Exception as e:
            retry_attempts += 1
            print(f"Não foi possível encontrar os elementos na página. Tentativa {retry_attempts} de {MAX_RETRY_ATTEMPTS}.")

            if retry_attempts >= MAX_RETRY_ATTEMPTS:
                print("Número máximo de tentativas excedido. Saindo do programa.")
                break

            wait_and_click(driver.find_element(By.ID, 'view_more'))

        # Verifica os pets indesejados e notifica, se necessário
        check_unwanted_pets(driver, pets_nao_desejados)

        # Verifica se todos os três pets foram encontrados
        try:
            pet0_color = driver.find_element(By.ID, 'pet0_color').text
            pet1_color = driver.find_element(By.ID, 'pet1_color').text
            pet2_color = driver.find_element(By.ID, 'pet2_color').text
        except Exception as e:
            retry_attempts += 1
            print(f"Um ou mais pets não foram encontrados. Tentativa {retry_attempts} de {MAX_RETRY_ATTEMPTS}.")

            if retry_attempts >= MAX_RETRY_ATTEMPTS:
                print("Número máximo de tentativas excedido. Saindo do programa.")
                break

            wait_and_click(driver.find_element(By.ID, 'view_more'))

        # Clique no botão 'View More Pets'
        wait_and_click(driver.find_element(By.ID, 'view_more'))


def main():
    try:
        # Configuração do driver do Edge para a aplicação do Orfanato
        driver_options = webdriver.EdgeOptions()
        driver_options.use_chromium = True
        driver_options.add_argument("--remote-debugging-port=9222")

        # Crie um novo driver para a aplicação do Orfanato
        driver = webdriver.Edge(options=driver_options)

        # Acessar a página do Orfanato
        driver.get(NEOPETS_URL)
        time.sleep(REFRESH_WAIT_TIME)

        contador = 0

        while True:
            find_unwanted_pets(driver)

            # Incrementar o contador a cada volta do loop
            contador += 1

            # Imprimir o valor do contador
            print(f"Número de voltas do loop: {contador}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
