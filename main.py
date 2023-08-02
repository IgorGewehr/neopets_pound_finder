from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# One-time initialization

# Configuração do driver do Edge para tentar conectar-se à guia já aberta
driver_options = webdriver.EdgeOptions()
driver_options.use_chromium = True
driver_options.add_argument("--remote-debugging-port=9222")

# Tente conectar-se à guia já aberta usando a porta 9222
driver = webdriver.Edge(options=driver_options)

try:
    # Acessar a página do pound
    driver.get('https://www.neopets.com/pound/adopt.phtml')
    time.sleep(15)

    # Lista para armazenar os nomes dos pets com cores ou pet_price não desejados
    pets_nao_desejados = []
    cores_desejadas = ['Grey', 'Mutant', 'Plushie', 'Maraquan', 'Wraith']

    # Contador de voltas do loop
    contador = 0

    while True:
        # Aguarde alguns segundos para garantir que a página seja carregada completamente
        time.sleep(5)

        # Verifique se os elementos estão presentes na página
        elements_present = driver.find_elements(By.ID, 'pet0_color')
        if not elements_present:
            print("Não foi possível encontrar os elementos na página. Atualizando a página e tentando novamente...")
            try:
                button = driver.find_element(By.ID, 'view_more')
                button.click()
            except Exception as e:
                # Verificar o tipo de erro ocorrido
                if "timeout" in str(e) or "Timed out" in str(e) or "not reachable" in str(e):
                    print(
                        "Erro de timeout ou página não respondendo. Aguardando 10 minutos antes de tentar novamente...")
                    time.sleep(600)  # 10 minutos em segundos
                    driver.refresh()  # Atualizar a página
                else:
                    print("Erro ao encontrar o botão 'View More Pets'. Atualizando a página e tentando novamente...")
                    driver.refresh()  # Atualizar a página
                    time.sleep(15)

        # Verifique se o elemento do pet0 está presente na página
        try:
            pet0_color = driver.find_element(By.ID, 'pet0_color').text
            pet0_name = driver.find_element(By.ID, 'pet0_name').text
            pet0_price = int(driver.find_element(By.ID, 'pet0_price').text.replace(',', ''))
        except:
            pet0_color = None
            pet0_name = None
            pet0_price = 0

        # Verifique se o elemento do pet2 está presente na página
        try:
            pet1_color = driver.find_element(By.ID, 'pet1_color').text
            pet1_name = driver.find_element(By.ID, 'pet1_name').text
            pet1_price = int(driver.find_element(By.ID, 'pet1_price').text.replace(',', ''))
        except:
            pet1_color = None
            pet1_name = None
            pet1_price = 0

        # Verifique se o elemento do pet3 está presente na página
        try:
            pet2_color = driver.find_element(By.ID, 'pet2_color').text
            pet2_name = driver.find_element(By.ID, 'pet2_name').text
            pet2_price = int(driver.find_element(By.ID, 'pet2_price').text.replace(',', ''))
        except:
            pet2_color = None
            pet2_name = None
            pet2_price = 0

        # Verifique a cor de cada pet e adicione o nome à lista, se necessário
        if pet0_color and pet0_color in cores_desejadas:
            pets_nao_desejados.append(pet0_name + " - " + pet0_color)
            print(f"Pet indesejado encontrado: {pet0_name}")


            # Selecionar o pet0 da cor desejada
            driver.execute_script("select_pet(0)")
            time.sleep(1)  # Aguardar para garantir que a seleção seja concluída
            # Clicar no botão de adoção
            driver.find_element(By.ID, 'processAdoptBtn').click()
            time.sleep(1)  # Aguardar para garantir que o popup de adoção seja exibido
            # Clicar no botão "Okay" dentro do popup
            driver.execute_script("PetSlotPopup.processAdoption()")
            print("Pet adotado automaticamente!")

        if pet1_color and pet1_color in cores_desejadas:
            pets_nao_desejados.append(pet1_name + " - " + pet1_color)
            print(f"Pet indesejado encontrado: {pet1_name}")

            # Selecionar o pet1 da cor desejada
            driver.execute_script("select_pet(1)")
            time.sleep(1)  # Aguardar para garantir que a seleção seja concluída
            # Clicar no botão de adoção
            driver.find_element(By.ID, 'processAdoptBtn').click()
            time.sleep(1)  # Aguardar para garantir que o popup de adoção seja exibido
            # Clicar no botão "Okay" dentro do popup
            driver.execute_script("PetSlotPopup.processAdoption()")
            print("Pet adotado automaticamente!")

        if pet2_color and pet2_color in cores_desejadas:
            pets_nao_desejados.append(pet2_name + " - " + pet2_color)
            print(f"Pet indesejado encontrado: {pet2_name}")

            # Selecionar o pet2 da cor desejada
            driver.execute_script("select_pet(2)")
            time.sleep(1)  # Aguardar para garantir que a seleção seja concluída
            # Clicar no botão de adoção
            driver.find_element(By.ID, 'processAdoptBtn').click()
            time.sleep(1)  # Aguardar para garantir que o popup de adoção seja exibido
            # Clicar no botão "Okay" dentro do popup
            driver.execute_script("PetSlotPopup.processAdoption()")
            print("Pet adotado automaticamente!")

        # Verifique o preço de cada pet e adicione o nome à lista, se necessário
        if pet0_price > 20000:
            if pet0_name not in pets_nao_desejados:
                pets_nao_desejados.append(pet0_name + " - BD")
                print(f"Pet com preço maior do que 10000 encontrado: {pet0_name}")

                driver.execute_script("select_pet(0)")
                time.sleep(1)  # Aguardar para garantir que a seleção seja concluída
                # Clicar no botão de adoção
                driver.find_element(By.ID, 'processAdoptBtn').click()
                time.sleep(1)  # Aguardar para garantir que o popup de adoção seja exibido
                # Clicar no botão "Okay" dentro do popup
                driver.execute_script("PetSlotPopup.processAdoption()")
                print("Pet adotado automaticamente!")

        if pet1_price > 20000:
            if pet1_name not in pets_nao_desejados:
                pets_nao_desejados.append(pet1_name + " - BD")
                print(f"Pet com preço maior do que 10000 encontrado: {pet1_name}")

                # Selecionar o pet0 da cor desejada
                driver.execute_script("select_pet(1)")
                time.sleep(1)  # Aguardar para garantir que a seleção seja concluída
                # Clicar no botão de adoção
                driver.find_element(By.ID, 'processAdoptBtn').click()
                time.sleep(1)  # Aguardar para garantir que o popup de adoção seja exibido
                # Clicar no botão "Okay" dentro do popup
                driver.execute_script("PetSlotPopup.processAdoption()")
                print("Pet adotado automaticamente!")

        if pet2_price > 20000:
            if pet2_name not in pets_nao_desejados:
                pets_nao_desejados.append(pet2_name + " - BD")
                print(f"Pet com preço maior do que 10000 encontrado: {pet2_name}")

                driver.execute_script("select_pet(2)")
                time.sleep(1)  # Aguardar para garantir que a seleção seja concluída
                # Clicar no botão de adoção
                driver.find_element(By.ID, 'processAdoptBtn').click()
                time.sleep(1)  # Aguardar para garantir que o popup de adoção seja exibido
                # Clicar no botão "Okay" dentro do popup
                driver.execute_script("PetSlotPopup.processAdoption()")
                print("Pet adotado automaticamente!")


        # Imprima a lista completa de nomes de pets indesejados sempre que um novo pet for encontrado
        print("Lista de pets indesejados atualizada:")
        for pet in pets_nao_desejados:
            print(pet)

        # Verifique se todos os três pets foram encontrados
        if not (pet0_color and pet2_color and pet2_color):
            print("Um ou mais pets não foram encontrados. Atualizando a página e tentando novamente...")
            try:
                button = driver.find_element(By.ID, 'view_more')
                button.click()
            except Exception as e:
                # Verificar o tipo de erro ocorrido
                if "timeout" in str(e) or "Timed out" in str(e) or "not reachable" in str(e):
                    print(
                        "Erro de timeout ou página não respondendo. Aguardando 10 minutos antes de tentar novamente...")
                    time.sleep(600)  # 10 minutos em segundos
                    driver.refresh()  # Atualizar a página
                else:
                    print("Erro ao encontrar o botão 'View More Pets'. Atualizando a página e tentando novamente...")
                    driver.refresh()  # Atualizar a página
                    time.sleep(15)

        else:
            # Clique no botão "View More Pets"
            try:
                button = driver.find_element(By.ID, 'view_more')
                button.click()
            except Exception as e:
                # Verificar o tipo de erro ocorrido
                if "timeout" in str(e) or "Timed out" in str(e) or "not reachable" in str(e):
                    print(
                        "Erro de timeout ou página não respondendo. Aguardando 10 minutos antes de tentar novamente...")
                    time.sleep(600)  # 10 minutos em segundos
                    driver.refresh()  # Atualizar a página
                else:
                    print("Erro ao encontrar o botão 'View More Pets'. Atualizando a página e tentando novamente...")
                    driver.refresh()  # Atualizar a página
                    time.sleep(15)

        # Aguarde alguns segundos após cada clique para a página carregar
        time.sleep(2)

        # Incrementar o contador a cada volta do loop
        contador += 1

        # Imprimir o valor do contador
        print(f"Número de voltas do loop: {contador}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

# O loop continuará infinitamente clicando no botão "View More Pets" e atualizando a lista de pets indesejados
# O programa não fechará o navegador
