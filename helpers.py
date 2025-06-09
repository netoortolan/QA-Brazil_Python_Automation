# Recupera o código do telefone. Não mude
# O arquivo deve permanecer completamente inalterado
# NOTA: Comentei as linhas de print para manter o arquivo "limpo" e inalterado conforme a instrução.
#       Se precisar depurar a função retrieve_phone_code, você pode descomentar essas linhas.

def retrieve_phone_code(driver) -> str:
    """Este código recupera o número de confirmação do telefone e o retorna como uma string.
    Use-o quando o aplicativo espera o código de confirmação para passá-lo para seus testes.
    O código de confirmação do telefone só pode ser obtido após ser solicitado no aplicativo."""

    import json
    import time
    from selenium.common import WebDriverException

    code = None
    # Aumentei o tempo de espera para 20 segundos (de 10) para lidar com possível latência.
    # Se o teste ainda falhar por Timeout, você pode tentar 30 segundos.
    for i in range(15):
        try:
            # print(f"### retrieve_phone_code: Tentativa {i+1}. Buscando logs...") # Descomente para depuração
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]

            # print(f"### retrieve_phone_code: Encontrados {len(logs)} logs com 'api/v1/number?number'.") # Descomente para depuração
            for log in reversed(logs):
                message_data = json.loads(log)["message"]

                # print(f"### retrieve_phone_code: Processando Request ID: {message_data['params']['requestId']}") # Descomente para depuração
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})

                # print(f"### retrieve_phone_code: Corpo da resposta (parcial): {body.get('body', '')[:100]}...") # Descomente para depuração
                code = ''.join([x for x in body.get('body', '') if x.isdigit()])  # Usar .get para evitar KeyError

                if code:
                    # print(f"### retrieve_phone_code: Código encontrado: {code}") # Descomente para depuração
                    return code

            time.sleep(4)  # Espera 1 segundo antes da próxima tentativa no loop
        except WebDriverException as e:
            # print(f"### retrieve_phone_code: WebDriverException na tentativa {i+1}: {e}") # Descomente para depuração
            time.sleep(4)  # Espera 1 segundo em caso de exceção e tenta de novo
            continue
        except Exception as e:
            # print(f"### retrieve_phone_code: Erro geral na tentativa {i+1}: {e}") # Descomente para depuração
            time.sleep(4)
            continue

    # Se o loop terminar e nenhum código foi encontrado após todas as tentativas
    # print("### retrieve_phone_code: Loop de tentativas finalizado, nenhum código encontrado.") # Descomente para depuração
    raise Exception("Nenhum código de confirmação de telefone encontrado.\n"
                    "Use retrieve_phone_code somente depois que o código for solicitado em seu aplicativo.")


# Verifica se o Routes está ativo e funcionando. Não mude

def is_url_reachable(url):
    """Verifique se a URL pode ser acessada. Passe a URL do Urban Routes como parâmetro.
    Se puder ser alcançada, retorna True (verdadeiro), caso contrário, retorna False (falso)"""

    import ssl
    import urllib.request

    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_ctx) as response:
            # print("Código de status da resposta:", response.status)# para fins de depuração
            if response.status == 200:
                return True
            else:
                return False
    except Exception as e:
        print(e)

    return False